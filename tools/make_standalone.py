"""
src/ की हर फ़ाइल से एक अकेली चलने वाली (standalone) फ़ाइल बनाता है।

हर फ़ाइल जिन दूसरी फ़ाइलों को import करती है, उनका पूरा कोड उसी फ़ाइल के ऊपर
जोड़ दिया जाता है। मूल import पंक्तियाँ वैसी ही रहती हैं; एक छोटा loader उन्हें
फ़ाइल के अंदर रखे कोड से पूरा करता है। इससे नाम आपस में नहीं टकराते
(जैसे दो अलग-अलग `chart` फ़ंक्शन)।

चलाने का तरीका (रिपॉज़िटरी की जड़ से):
    python tools/make_standalone.py
"""
import ast
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
LOCAL = {p.stem for p in SRC.glob("*.py")}

LOADER = '''# ---- अंदर रखी गई सहायक फ़ाइलें: यह फ़ाइल अकेले चलती है, दूसरी फ़ाइल की ज़रूरत नहीं ----
# (tools/make_standalone.py से अपने-आप बनाया गया; बदलाव src/ में करें)
import sys as _sys, importlib.abc as _iabc, importlib.util as _iutil

_EMBEDDED = {
%s}


class _EmbeddedFinder(_iabc.MetaPathFinder, _iabc.Loader):
    def find_spec(self, name, path=None, target=None):
        if name in _EMBEDDED:
            return _iutil.spec_from_loader(name, self)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        exec(compile(_EMBEDDED[module.__name__], module.__name__ + ".py", "exec"), module.__dict__)


_sys.meta_path.insert(0, _EmbeddedFinder())
# ---- सहायक फ़ाइलें समाप्त ----

'''


def local_imports(path):
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
    return names & LOCAL


def closure(stem):
    seen, todo = [], [stem]
    while todo:
        cur = todo.pop()
        for dep in sorted(local_imports(SRC / f"{cur}.py")):
            if dep != stem and dep not in seen:
                seen.append(dep)
                todo.append(dep)
    return sorted(seen)


def literal(src):
    if "'''" not in src and not src.endswith("\\"):
        return "r'''" + src + "'''"
    return repr(src)


def build(stem):
    text = (SRC / f"{stem}.py").read_text(encoding="utf-8")
    deps = closure(stem)
    if not deps:
        return text
    body = "".join(f"    {d!r}: {literal((SRC / f'{d}.py').read_text(encoding='utf-8'))},\n" for d in deps)
    block = LOADER % body
    tree = ast.parse(text)
    first = tree.body[0]
    if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
            and isinstance(first.value.value, str):
        lines = text.splitlines(keepends=True)
        head, rest = "".join(lines[:first.end_lineno]), "".join(lines[first.end_lineno:])
        return head + "\n" + block + rest.lstrip("\n")
    return block + text


if __name__ == "__main__":
    for path in sorted(SRC.glob("*.py")):
        out = ROOT / path.name
        out.write_text(build(path.stem), encoding="utf-8")
        print(f"{path.name:24s} <- {', '.join(closure(path.stem)) or '(कोई निर्भरता नहीं)'}")
