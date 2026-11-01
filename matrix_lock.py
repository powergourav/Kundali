"""
D1-D9 मैट्रिक्स लॉक: ५ शर्तें, २ लाख रैंडम जोड़े (वर = b, वधू = g)।
"""

# ---- अंदर रखी गई सहायक फ़ाइलें: यह फ़ाइल अकेले चलती है, दूसरी फ़ाइल की ज़रूरत नहीं ----
# (tools/make_standalone.py से अपने-आप बनाया गया; बदलाव src/ में करें)
import sys as _sys, importlib.abc as _iabc, importlib.util as _iutil

_EMBEDDED = {
    'kundli_sim': r'''"""
रैंडम वर-वधू जोड़ों का Monte Carlo सिमुलेशन (Swiss Ephemeris, लाहिड़ी अयनांश)।
अष्टकूट गुण मिलान + मांगलिक + ग्रहों के 1-1 / 1-7 योग।
"""
import random, collections
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
FLG = swe.FLG_SIDEREAL
PL = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
      "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}

def chart(jd, lat, lon):
    c = {}
    for n, p in PL.items():
        c[n] = swe.calc_ut(jd, p, FLG)[0][0]
    c["Ketu"] = (c["Rahu"] + 180) % 360
    c["Lagna"] = swe.houses_ex(jd, lat, lon, b"W", FLG)[1][0]
    return c

def random_birth(y0, y1):
    jd0, jd1 = swe.julday(y0, 1, 1), swe.julday(y1, 1, 1)
    return random.uniform(jd0, jd1)

def place():  # भारत के भीतर रैंडम स्थान
    return random.uniform(9, 31), random.uniform(70, 90)

sign = lambda L: int(L // 30) % 12
nak = lambda L: int(L // (360 / 27)) % 27

# ---------- अष्टकूट ----------
VARNA = {3: 4, 7: 4, 11: 4, 0: 3, 4: 3, 8: 3, 1: 2, 5: 2, 9: 2, 2: 1, 6: 1, 10: 1}

def vashya_cat(L):
    s, d = sign(L), L % 30
    if s in (0, 1): return 0
    if s == 8: return 1 if d < 15 else 0
    if s == 9: return 0 if d < 15 else 2
    if s in (2, 5, 6, 10): return 1
    if s in (3, 11): return 2
    if s == 4: return 3
    return 4  # वृश्चिक
VASHYA = [[2, 1, 1, 0.5, 1], [1, 2, 0.5, 0, 1], [1, 0.5, 2, 1, 1], [0.5, 0, 1, 2, 0], [1, 1, 1, 0, 2]]

YONI = [0, 1, 2, 3, 3, 4, 5, 2, 5, 6, 6, 7, 8, 9, 8, 9, 10, 10, 4, 11, 12, 11, 13, 0, 13, 7, 1]
YONI_ENEMY = {frozenset(p) for p in [(0, 8), (1, 13), (2, 11), (3, 12), (4, 10), (5, 6), (7, 9)]}

LORD = ["Ma", "Ve", "Me", "Mo", "Su", "Me", "Ve", "Ma", "Ju", "Sa", "Sa", "Ju"]
FR = {"Su": ({"Mo", "Ma", "Ju"}, {"Ve", "Sa"}), "Mo": ({"Su", "Me"}, set()),
      "Ma": ({"Su", "Mo", "Ju"}, {"Me"}), "Me": ({"Su", "Ve"}, {"Mo"}),
      "Ju": ({"Su", "Mo", "Ma"}, {"Me", "Ve"}), "Ve": ({"Me", "Sa"}, {"Su", "Mo"}),
      "Sa": ({"Me", "Ve"}, {"Su", "Mo", "Ma"})}
def rel(a, b):  # a की दृष्टि में b: 2 मित्र, 1 सम, 0 शत्रु
    if a == b: return 2
    f, e = FR[a]
    return 2 if b in f else 0 if b in e else 1
MAITRI = {(2, 2): 5, (2, 1): 4, (1, 2): 4, (1, 1): 3, (2, 0): 1, (0, 2): 1, (1, 0): 0.5, (0, 1): 0.5, (0, 0): 0}

GANA = [0, 1, 2, 1, 0, 1, 0, 0, 2, 2, 1, 1, 0, 2, 0, 2, 0, 2, 2, 1, 1, 0, 2, 2, 1, 1, 0]  # 0 देव 1 मनुष्य 2 राक्षस
def gana_pts(b, g):
    if b == g: return 6
    s = {b, g}
    if s == {0, 1}: return 5
    if s == {0, 2}: return 1
    return 0

NADI = [0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2, 2, 1, 0, 0, 1, 2]

def ashtakoot(bm, gm):
    bs, gs, bn, gn = sign(bm), sign(gm), nak(bm), nak(gm)
    k = {}
    k["varna"] = 1 if VARNA[bs] >= VARNA[gs] else 0
    k["vashya"] = VASHYA[vashya_cat(bm)][vashya_cat(gm)]
    t = 0
    for a, b in ((gn, bn), (bn, gn)):
        if (((b - a) % 27) + 1) % 9 not in (3, 5, 7): t += 1.5
    k["tara"] = t
    yb, yg = YONI[bn], YONI[gn]
    k["yoni"] = 4 if yb == yg else 0 if frozenset((yb, yg)) in YONI_ENEMY else 2
    lb, lg = LORD[bs], LORD[gs]
    k["maitri"] = 5 if lb == lg else MAITRI[(rel(lb, lg), rel(lg, lb))]
    k["gana"] = gana_pts(GANA[bn], GANA[gn])
    d = (bs - gs) % 12 + 1
    k["bhakoot"] = 0 if d in (2, 12, 5, 9, 6, 8) else 7
    k["nadi"] = 0 if NADI[bn] == NADI[gn] else 8
    return k

def manglik(c):
    h = (sign(c["Mars"]) - sign(c["Lagna"])) % 12 + 1
    return h in (1, 2, 4, 7, 8, 12)

def rel_type(a, b):
    d = (sign(a) - sign(b)) % 12
    return "1-1" if d == 0 else "1-7" if d == 6 else None

# ---------- सिमुलेशन ----------
def run(N=200_000, seed=7):
    random.seed(seed)
    cnt = collections.Counter()
    scores = collections.Counter()
    planets = ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu"]
    prel = {p: collections.Counter() for p in planets}
    nmatch = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))  # वर कितने वर्ष बड़ा
        jg = jb + gap * 365.25
        b, g = chart(jb, *place()), chart(jg, *place())
        k = ashtakoot(b["Moon"], g["Moon"])
        s = sum(k.values())
        scores[int(s)] += 1
        no_dosha = k["nadi"] > 0 and k["bhakoot"] > 0
        mg_ok = manglik(b) == manglik(g)
        m = 0
        for p in planets:
            r = rel_type(b[p], g[p])
            if r: prel[p][r] += 1; m += p != "Lagna"
        nmatch[m] += 1
        lag = rel_type(b["Lagna"], g["Lagna"]) is not None
        ven = rel_type(b["Venus"], g["Venus"]) is not None
        # वर का शुक्र वधू के मंगल से 1-1/1-7 या उल्टा (पारंपरिक आकर्षण योग)
        vm = rel_type(b["Venus"], g["Mars"]) or rel_type(g["Venus"], b["Mars"])
        # एक का शुक्र दूसरे के लग्न या सप्तम में
        v7 = rel_type(b["Venus"], g["Lagna"]) or rel_type(g["Venus"], b["Lagna"])

        cnt["T1 गुण>=18"] += s >= 18
        t2 = s >= 18 and no_dosha and mg_ok
        cnt["T2 +नाड़ी/भकूट दोष नहीं +मांगलिक मेल"] += t2
        t3 = t2 and s >= 28
        cnt["T3 +गुण>=28"] += t3
        t4 = t3 and lag and ven
        cnt["T4 +लग्न 1-1/1-7 +शुक्र 1-1/1-7"] += t4
        t5 = t4 and bool(vm) and bool(v7)
        cnt["T5 +शुक्र-मंगल योग +शुक्र दूसरे के लग्न/सप्तम में"] += t5
        cnt["T5' (T4 + गुण>=32)"] += t4 and s >= 32
        cnt["_nadi_dosha"] += k["nadi"] == 0
        cnt["_bhakoot_dosha"] += k["bhakoot"] == 0
        cnt["_manglik_ok"] += mg_ok
        cnt["_gte28"] += s >= 28
        cnt["_gte32"] += s >= 32
    return N, cnt, scores, prel, nmatch

if __name__ == "__main__":
    N, cnt, scores, prel, nmatch = run()
    print(f"N = {N} जोड़े\n")
    for key, v in cnt.items():
        print(f"{key:55s} {v:7d}  {100*v/N:7.3f}%   (~1 in {N/v:,.0f})" if v else f"{key:55s} 0")
    print("\nगुण वितरण:")
    for s in sorted(scores):
        print(f"{s:2d}: {100*scores[s]/N:5.2f}%")
    print("\nग्रह-वार 1-1 / 1-7:")
    for p, c in prel.items():
        print(f"{p:8s} 1-1 {100*c['1-1']/N:5.1f}%   1-7 {100*c['1-7']/N:5.1f}%")
    print("\nकितने ग्रह (लग्न छोड़कर, 8 में से) 1-1 या 1-7 में:")
    for m in sorted(nmatch):
        print(f"{m}: {100*nmatch[m]/N:5.2f}%")
''',
    'sanyog_sim': r'''"""
दिनेश-पी जोड़े के संयोग रैंडम जोड़ों में कितने आम हैं, इसकी जाँच।
"""
import random, collections
from kundli_sim import chart, random_birth, place, sign, nak, ashtakoot

def nav(L):
    return int(L * 3 / 10) % 12

def d(a, b):  # राशि-अंतर 0..11
    return (a - b) % 12

LORD = ["Ma", "Ve", "Me", "Mo", "Su", "Me", "Ve", "Ma", "Ju", "Sa", "Sa", "Ju"]

def features(b, g):
    S = {k: sign(v) for k, v in b.items()}
    T = {k: sign(v) for k, v in g.items()}
    one7 = lambda x, y: d(x, y) in (0, 6)
    trine = lambda x, y: d(x, y) in (0, 4, 8)
    house = lambda planet_sign, lagna_sign: d(planet_sign, lagna_sign) + 1
    jup_asp = lambda j, x: d(x, j) in (0, 4, 6, 8)  # युति या 5/7/9 दृष्टि
    f = collections.OrderedDict()
    f["शुक्र 1-1/1-7"] = one7(S["Venus"], T["Venus"])
    f["मंगल 1-1/1-7"] = one7(S["Mars"], T["Mars"])
    f["चंद्र 1-1/1-7"] = one7(S["Moon"], T["Moon"])
    f["लग्न 1-1/1-7"] = one7(S["Lagna"], T["Lagna"])
    f["लग्नेश एक"] = LORD[S["Lagna"]] == LORD[T["Lagna"]]
    f["चंद्र-राशीश एक"] = LORD[S["Moon"]] == LORD[T["Moon"]]
    f["सूर्य-चंद्र-बुध एक तत्व"] = all(trine(S[p], T[p]) for p in ("Sun", "Moon", "Mercury"))
    f["एक का चंद्र दूसरे के सप्तम में"] = house(S["Moon"], T["Lagna"]) == 7 or house(T["Moon"], S["Lagna"]) == 7
    f["एक का शुक्र दूसरे के 5/7 में"] = house(S["Venus"], T["Lagna"]) in (5, 7) or house(T["Venus"], S["Lagna"]) in (5, 7)
    f["शुक्र-मंगल आपसी 1-1/1-7"] = one7(S["Venus"], T["Mars"]) or one7(T["Venus"], S["Mars"])
    f["नवांश शुक्र 1-1/1-7"] = one7(nav(b["Venus"]), nav(g["Venus"]))
    f["नवांश मंगल 1-1/1-7"] = one7(nav(b["Mars"]), nav(g["Mars"]))
    f["नवांश लग्न त्रिकोण/1-7"] = trine(nav(b["Lagna"]), nav(g["Lagna"])) or one7(nav(b["Lagna"]), nav(g["Lagna"]))
    f["एक का गुरु दूसरे के लग्न/चंद्र पर"] = any(jup_asp(X["Jupiter"], Y[k]) for X, Y in ((S, T), (T, S)) for k in ("Lagna", "Moon"))
    return f

def deg(sign_idx, d_, m_):
    return sign_idx * 30 + d_ + m_ / 60

# दिनेश (वर) और पी (वधू) - जगन्नाथ होरा के मान
DINESH = {"Lagna": deg(8, 8, 34.6), "Sun": deg(5, 13, 24.8), "Moon": deg(5, 17, 42.7), "Mars": deg(5, 13, 15.0),
          "Mercury": deg(5, 3, 12.4), "Jupiter": deg(2, 15, 51.3), "Venus": deg(6, 26, 50.0),
          "Saturn": deg(8, 13, 53.8), "Rahu": deg(9, 29, 40.1), "Ketu": deg(3, 29, 40.1)}
P = {"Lagna": deg(11, 11, 11.2), "Sun": deg(1, 3, 41.8), "Moon": deg(9, 0, 8.0), "Mars": deg(4, 3, 15.3),
     "Mercury": deg(1, 23, 23.3), "Jupiter": deg(7, 18, 25.5), "Venus": deg(0, 8, 33.7),
     "Saturn": deg(10, 29, 5.6), "Rahu": deg(6, 10, 41.1), "Ketu": deg(0, 10, 41.1)}

if __name__ == "__main__":
    fc = features(DINESH, P)
    k = ashtakoot(DINESH["Moon"], P["Moon"])
    my_n = sum(fc.values())
    print("इस जोड़े में:", my_n, "/", len(fc))
    for n, v in fc.items(): print("  ", "✓" if v else "✗", n)

    random.seed(11)
    N = 200_000
    single = collections.Counter(); total = collections.Counter()
    exact = 0; exact_plus = 0
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = features(b, g)
        for n, v in f.items(): single[n] += v
        c = sum(f.values()); total[c] += 1
        # इस जोड़े के सारे संयोग एक साथ
        if all(f[n] for n, v in fc.items() if v):
            exact += 1
            kk = ashtakoot(b["Moon"], g["Moon"])
            if kk["nadi"] > 0 and sum(kk.values()) >= 24: exact_plus += 1
    print(f"\nN = {N}")
    print("हर संयोग अलग-अलग:")
    for n in fc: print(f"   {100*single[n]/N:5.1f}%  {n}")
    print("संयोगों की गिनती का वितरण:")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]
        print(f"   {c:2d}: {100*total[c]/N:6.3f}%   (इतने या ज़्यादा: {100*cum/N:6.3f}%)")
    print(f"इस जोड़े के सारे {my_n} संयोग एक साथ: {exact} ({100*exact/N:.4f}%)")
    print(f"  + नाड़ी दोष नहीं और गुण >= 24: {exact_plus} ({100*exact_plus/N:.4f}%)")
''',
}


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

import random
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav, DINESH, P

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
ALL = SEVEN + ["Rahu", "Ketu"]
def karakas(c): return sorted(SEVEN, key=lambda p: -(c[p] % 30))
def hs(x, lg): return (x - lg) % 12 + 1   # भाव संख्या

def conds(b, g):
    bL, gL = sign(b["Lagna"]), sign(g["Lagna"])
    bL9, gL9 = nav(b["Lagna"]), nav(g["Lagna"])
    bR, gR = sign(b["Rahu"]), sign(g["Rahu"])
    bR9, gR9 = nav(b["Rahu"]), nav(g["Rahu"])
    c = {}
    # १. वधू का D1 लग्न-सप्तम अक्ष = वर का D9 राहु-केतु अक्ष, वर के D9 में ४-१० भाव
    c[1] = gL % 6 == bR9 % 6 and hs(bR9, bL9) in (4, 10)
    # २. वर का D1 राहु = वधू का D9 राहु (एक ही क्रम), वधू के D9 में ४-१० भाव
    c[2] = bR == gR9 and hs(gR9, gL9) in (4, 10)
    # ३. D1 में राहु २-८ विपरीत क्रम, D9 में राहु ४-१० एक ही क्रम
    hb, hg = hs(bR, bL), hs(gR, gL)
    c[3] = hg in (2, 8) and hb == (10 - hg) and hs(bR9, bL9) == hs(gR9, gL9) in (4, 10)
    # ४. कारकांश एक, दारकारक का नवांश एक
    kb, kg = karakas(b), karakas(g)
    c["4"] = nav(b[kb[0]]) == nav(g[kg[0]]) and nav(b[kb[6]]) == nav(g[kg[6]])
    c["4x"] = c["4"] and nav(b[kb[0]]) == 2 and nav(b[kb[6]]) == 9   # ठीक मिथुन और मकर
    # ५. वधू का सप्तम खाली, वहाँ वर के ठीक ४ ग्रह
    g7 = (gL + 6) % 12
    c[5] = all(sign(g[p]) != g7 for p in ALL) and sum(sign(b[p]) == g7 for p in SEVEN) == 4
    return c

if __name__ == "__main__":
    print("दिनेश(वर)-पी(वधू) जाँच:", conds(DINESH, P))
    random.seed(55); N = 200_000
    single = {k: 0 for k in (1, 2, 3, "4", "4x", 5)}
    cum = {"1": 0, "1+2": 0, "1+2+3": 0, "1-4": 0, "1-5": 0, "1-5 (मिथुन/मकर)": 0}
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        c = conds(b, g)
        for k in single: single[k] += c[k]
        a = c[1]; cum["1"] += a
        a = a and c[2]; cum["1+2"] += a
        a = a and c[3]; cum["1+2+3"] += a
        a = a and c["4"]; cum["1-4"] += a
        cum["1-5"] += a and c[5]
        cum["1-5 (मिथुन/मकर)"] += a and c["4x"] and c[5]
    print(f"\nN = {N}")
    for k, v in single.items(): print(f"शर्त {k}: {v} ({100*v/N:.3f}%)")
    for k, v in cum.items(): print(f"साथ में {k}: {v} ({100*v/N:.4f}%)")
