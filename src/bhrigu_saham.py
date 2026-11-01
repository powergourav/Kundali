"""
भृगु बिंदु (दो विधियाँ), विवाह सहम (ताजिक), लग्नेश-सप्तमेश का आपसी मिलान।
"""
import random
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import DINESH, P, nav

SN = "मेष वृषभ मिथुन कर्क सिंह कन्या तुला वृश्चिक धनु मकर कुंभ मीन".split()
NK = ("अश्विनी भरणी कृत्तिका रोहिणी मृगशिरा आर्द्रा पुनर्वसु पुष्य आश्लेषा मघा पूर्वाफाल्गुनी उत्तराफाल्गुनी "
      "हस्त चित्रा स्वाति विशाखा अनुराधा ज्येष्ठा मूल पूर्वाषाढ़ा उत्तराषाढ़ा श्रवण धनिष्ठा शतभिषा पूर्वाभाद्रपद "
      "उत्तराभाद्रपद रेवती").split()
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def fmt(x):
    x %= 360; s = int(x // 30); d = x % 30
    n = int(x // (40 / 3)); pada = int((x % (40 / 3)) // (10 / 3)) + 1
    return f"{SN[s]} {int(d)}°{int(round((d % 1) * 60)):02d}' ({NK[n]} {pada}, नवांश {SN[nav(x)]})"

def dist(a, b): return abs((a - b + 180) % 360 - 180)

def bb_a(c):  # विधि १: राहु से चंद्र तक राशि-क्रम में दूरी का आधा, राहु में जोड़ें
    return (c["Rahu"] + ((c["Moon"] - c["Rahu"]) % 360) / 2) % 360
def bb_b(c):  # विधि २: (चंद्र + राहु) / २ सीधा औसत
    return ((c["Moon"] + c["Rahu"]) / 2) % 360

def between(x, a, b):  # क्या x, a से b की ओर राशि-क्रम में बीच में है
    return (x - a) % 360 < (b - a) % 360

def saham(c, night=False):
    ve, sa, lg = c["Venus"], c["Saturn"], c["Lagna"]
    a, b = (sa, ve) if not night else (ve, sa)   # दिन: शुक्र − शनि + लग्न
    s = (b - a + lg) % 360
    s_raw = s
    if not between(lg, a, b): s = (s + 30) % 360  # नीलकंठी नियम
    return s_raw, s

def points(c, night):
    L = sign(c["Lagna"])
    p = {"लग्न": c["Lagna"], "चंद्र": c["Moon"], "शुक्र": c["Venus"],
         "लग्नेश": c[LORD[L]], "सप्तमेश": c[LORD[(L + 6) % 12]],
         "सप्तम भाव मध्य": (c["Lagna"] + 180) % 360,
         "भृगु बिंदु (१)": bb_a(c), "भृगु बिंदु (२)": bb_b(c),
         "विवाह सहम": saham(c, night)[1]}
    return p

def contacts(x, y, orb=2.0):
    out = []
    for a, va in x.items():
        for b, vb in y.items():
            for asp, ang in (("युति", 0), ("समसप्तक", 180), ("त्रिकोण", 120)):
                d = dist(dist(va, vb), ang) if ang else dist(va, vb)
                if ang == 120: d = min(abs(dist(va, vb) - 120), 999)
                if d <= orb: out.append((a, b, asp, d))
    return out

if __name__ == "__main__":
    for nm, c, night in (("दिनेश (दिन का जन्म)", DINESH, False), ("पी (रात का जन्म)", P, True)):
        print(f"\n== {nm} ==")
        print("  भृगु बिंदु विधि १:", fmt(bb_a(c)))
        print("  भृगु बिंदु विधि २:", fmt(bb_b(c)))
        for n in (False, True):
            raw, s = saham(c, n)
            print(f"  विवाह सहम ({'रात्रि सूत्र' if n else 'दिन सूत्र'}): बिना सुधार {fmt(raw)} | नीलकंठी सुधार {fmt(s)}")
        L = sign(c["Lagna"])
        print("  लग्नेश", LORD[L], fmt(c[LORD[L]]), " सप्तमेश", LORD[(L + 6) % 12], fmt(c[LORD[(L + 6) % 12]]))
    D, Pp = points(DINESH, False), points(P, True)
    print("\n== आपसी संपर्क (२° के भीतर) ==")
    for a, b, asp, d in contacts(D, Pp) + [("(पी) " + b, "(दिनेश) " + a, asp, d) for a, b, asp, d in []]:
        print(f"  दिनेश {a:16s} - पी {b:16s} {asp:8s} {d*60:5.1f}'")
    # रैंडम अपेक्षा
    random.seed(8); N = 40000; tot = 0
    for _ in range(N):
        jb = random_birth(1980, 2001); gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        tot += len(contacts(points(b, random.random() < .5), points(g, random.random() < .5)))
    print(f"\nरैंडम जोड़ों में २° के भीतर औसत संपर्क: {tot/N:.2f}  (इस जोड़े में {len(contacts(D, Pp))})")
