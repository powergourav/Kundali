"""
दशकूट: वर और वधू के चंद्र के सभी 108 x 108 नक्षत्र-चरण जोड़ों की पूरी गणना।
हर कूट: शुभ = 1, मध्यम = 0.5, अशुभ = 0।
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

import collections
from kundli_sim import ashtakoot, rel, LORD, GANA, YONI, YONI_ENEMY

RAJJU = {}
for grp, naks in enumerate([(0, 8, 9, 17, 18, 26), (1, 7, 10, 16, 19, 25), (2, 6, 11, 15, 20, 24),
                            (3, 5, 12, 14, 21, 23), (4, 13, 22)]):
    for n in naks: RAJJU[n] = grp
VEDHA = [(0, 17), (1, 16), (2, 15), (3, 14), (5, 21), (6, 20), (7, 19), (8, 18), (9, 26), (10, 25),
         (11, 24), (12, 23), (4, 13), (4, 22), (13, 22)]
VEDHA = {frozenset(p) for p in VEDHA}
VASHYA_R = {0: {4, 7}, 1: {3, 6}, 2: {5}, 3: {7, 8}, 4: {6}, 5: {11, 2}, 6: {5, 9}, 7: {3},
            8: {11}, 9: {0, 10}, 10: {0}, 11: {9}}

def dashakoot(bn, bs, gn, gs):
    n = (bn - gn) % 27 + 1
    k = {}
    k["दिन"] = 1 if n % 9 in (0, 2, 4, 6, 8) else 0
    gb, gg = GANA[bn], GANA[gn]
    if gb == gg or {gb, gg} == {0, 1}: k["गण"] = 1
    elif gb == 2 and gg == 1: k["गण"] = 0.5
    else: k["गण"] = 0
    k["माहेंद्र"] = 1 if n in (4, 7, 10, 13, 16, 19, 22, 25) else 0
    k["स्त्री-दीर्घ"] = 1 if n > 13 else 0.5 if n > 7 else 0
    yb, yg = YONI[bn], YONI[gn]
    k["योनि"] = 1 if yb == yg else 0 if frozenset((yb, yg)) in YONI_ENEMY else 0.5
    r = (bs - gs) % 12 + 1
    k["राशि"] = 1 if r in (1, 7, 9, 10, 11) else 0
    lb, lg = LORD[bs], LORD[gs]
    s = 4 if lb == lg else {(2, 2): 5, (2, 1): 4, (1, 2): 4, (1, 1): 3}.get((rel(lb, lg), rel(lg, lb)), 0)
    k["राशि-स्वामी"] = 1 if s >= 4 else 0.5 if s == 3 else 0
    k["वश्य"] = 1 if (bs in VASHYA_R[gs] or gs in VASHYA_R[bs]) else 0
    k["रज्जु"] = 0 if RAJJU[bn] == RAJJU[gn] else 1
    k["वेध"] = 0 if frozenset((bn, gn)) in VEDHA else 1
    return k

def pada_info(p):
    L = p * 10 / 3 + 5 / 3
    return L, p // 4, int(L // 30)

if __name__ == "__main__":
    # दिनेश: हस्त 3 = चरण 12*4+2 ; पी: उत्तराषाढ़ा 2 = चरण 20*4+1
    Lb, bn, bs = pada_info(12 * 4 + 2)
    Lg, gn, gs = pada_info(20 * 4 + 1)
    me = dashakoot(bn, bs, gn, gs)
    my = sum(me.values())
    print("इस जोड़े का दशकूट:", me, "कुल", my)
    dist = collections.Counter(); joint = collections.Counter()
    clean_ge = 0; ge = 0; total = 0; ge_and_ak = 0
    for pb in range(108):
        Lb, bn, bs = pada_info(pb)
        for pg in range(108):
            Lg, gn, gs = pada_info(pg)
            k = dashakoot(bn, bs, gn, gs)
            s = sum(k.values()); total += 1
            dist[s] += 1
            clean = k["रज्जु"] == 1 and k["वेध"] == 1
            if s >= my: ge += 1
            if s >= my and clean: clean_ge += 1
            ak = sum(ashtakoot(Lb, Lg).values())
            if s >= my and clean and ak >= 24 and ashtakoot(Lb, Lg)["nadi"] > 0: ge_and_ak += 1
    print(f"कुल जोड़े (चरण-संयोग): {total}")
    cum = 0
    for s in sorted(dist, reverse=True):
        cum += dist[s]
        print(f"  {s:4.1f}/10 : {100*dist[s]/total:6.2f}%   इतना या ज़्यादा: {100*cum/total:6.2f}%")
    print(f"{my}/10 या ज़्यादा: {100*ge/total:.2f}%")
    print(f"{my}/10 या ज़्यादा + रज्जु-वेध साफ़: {100*clean_ge/total:.2f}%")
    print(f"ऊपर वाला + अष्टकूट >=24 + नाड़ी दोष नहीं: {100*ge_and_ak/total:.2f}%")
