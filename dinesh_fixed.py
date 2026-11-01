"""
दिनेश (वर) की कुंडली स्थिर, वधू की कुंडली रैंडम।
वधू का जन्म: दिनेश (३० सितंबर १९८९) से औसतन ३.५ वर्ष बाद, भारत में रैंडम स्थान।
"""

# ---- अंदर रखी गई सहायक फ़ाइलें: यह फ़ाइल अकेले चलती है, दूसरी फ़ाइल की ज़रूरत नहीं ----
# (tools/make_standalone.py से अपने-आप बनाया गया; बदलाव src/ में करें)
import sys as _sys, importlib.abc as _iabc, importlib.util as _iutil

_EMBEDDED = {
    'dashakoot_enum': r'''"""
दशकूट: वर और वधू के चंद्र के सभी 108 x 108 नक्षत्र-चरण जोड़ों की पूरी गणना।
हर कूट: शुभ = 1, मध्यम = 0.5, अशुभ = 0।
"""
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
            if s >= my and clean and ak >= 25 and ashtakoot(Lb, Lg)["nadi"] > 0: ge_and_ak += 1
    print(f"कुल जोड़े (चरण-संयोग): {total}")
    cum = 0
    for s in sorted(dist, reverse=True):
        cum += dist[s]
        print(f"  {s:4.1f}/10 : {100*dist[s]/total:6.2f}%   इतना या ज़्यादा: {100*cum/total:6.2f}%")
    print(f"{my}/10 या ज़्यादा: {100*ge/total:.2f}%")
    print(f"{my}/10 या ज़्यादा + रज्जु-वेध साफ़: {100*clean_ge/total:.2f}%")
    print(f"ऊपर वाला + अष्टकूट >=25 + नाड़ी दोष नहीं: {100*ge_and_ak/total:.2f}%")
''',
    'durlabh_yog': r'''"""
एक अकेली कुंडली में "दुर्लभ" (5% या कम) योग कितने मिलते हैं।
पहले सभी उम्मीदवार योग गिने जाते हैं, फिर केवल वही रखे जाते हैं जो
रैंडम कुंडलियों में 5% या कम मिलते हैं।
"""
import random, collections, itertools
import swisseph as swe
from kundli_sim import random_birth, place, sign, nak
from sanyog_sim import nav

swe.set_sid_mode(swe.SIDM_LAHIRI)
FLG = swe.FLG_SIDEREAL | swe.FLG_SPEED
PL = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
      "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}
NM = {"Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध", "Jupiter": "गुरु",
      "Venus": "शुक्र", "Saturn": "शनि"}
SEVEN = list(NM)
EXALT = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}
OWN = {"Sun": {4}, "Moon": {3}, "Mars": {0, 7}, "Mercury": {2, 5}, "Jupiter": {8, 11},
       "Venus": {1, 6}, "Saturn": {9, 10}}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
MAHA = {"Mars": "रुचक", "Mercury": "भद्र", "Jupiter": "हंस", "Venus": "मालव्य", "Saturn": "शश"}

def chart(jd, lat, lon):
    c, r = {}, set()
    for n, p in PL.items():
        x = swe.calc_ut(jd, p, FLG)[0]
        c[n] = x[0]
        if n in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") and x[3] < 0: r.add(n)
    c["Ketu"] = (c["Rahu"] + 180) % 360
    c["Lagna"] = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)[1][0]
    return c, r

def dist(a, b): return abs((a - b + 180) % 360 - 180)

def features(c, retro):
    f = {}
    L = sign(c["Lagna"]); H = lambda p: (sign(c[p]) - L) % 12 + 1
    for p in SEVEN:
        f[f"{NM[p]} परम उच्च (±३°)"] = dist(c[p], EXALT[p]) <= 3
        f[f"{NM[p]} परम नीच (±३°)"] = dist(c[p], EXALT[p] + 180) <= 3
        f[f"{NM[p]} लग्न-अंश से १° के भीतर"] = dist(c[p], c["Lagna"]) <= 1
        f[f"{NM[p]} वर्गोत्तम और उच्च"] = sign(c[p]) == nav(c[p]) and sign(c[p]) == EXALT[p] // 30
        f[f"{NM[p]} उच्च होकर लग्न में"] = sign(c[p]) == EXALT[p] // 30 and H(p) == 1
    for p, nm in MAHA.items():
        f[f"{nm} महापुरुष योग"] = (sign(c[p]) in OWN[p] or sign(c[p]) == EXALT[p] // 30) and H(p) in (1, 4, 7, 10)
    cnt = collections.Counter(sign(c[p]) for p in SEVEN)
    f["एक राशि में ४+ ग्रह"] = max(cnt.values()) >= 4
    f["एक राशि में ५+ ग्रह"] = max(cnt.values()) >= 5
    rh = c["Rahu"]
    side = [((c[p] - rh) % 360) < 180 for p in SEVEN]
    f["कालसर्प (सातों ग्रह राहु-केतु के एक ओर)"] = all(side) or not any(side)
    el = (c["Moon"] - c["Sun"]) % 360
    f["अमावस्या के पास जन्म (±६°)"] = min(el, 360 - el) <= 6
    f["पूर्णिमा के पास जन्म (±६°)"] = dist(el, 180) <= 6
    gand = lambda x: (x % 120) >= 116.667 or (x % 120) <= 3.333
    f["चंद्र गंडांत"] = gand(c["Moon"])
    f["लग्न गंडांत"] = gand(c["Lagna"])
    f["लग्न और चंद्र एक नक्षत्र"] = nak(c["Lagna"]) == nak(c["Moon"])
    f["लग्न और चंद्र दोनों वर्गोत्तम"] = sign(c["Lagna"]) == nav(c["Lagna"]) and sign(c["Moon"]) == nav(c["Moon"])
    f["४ या ज़्यादा ग्रह वक्री"] = len(retro) >= 4
    f["ग्रह युद्ध (मंगल-शनि में किन्हीं दो की दूरी <१°)"] = any(
        dist(c[a], c[b]) < 1 for a, b in itertools.combinations(["Mars", "Mercury", "Jupiter", "Venus", "Saturn"], 2))
    f["लग्नेश-सप्तमेश परिवर्तन"] = (sign(c[LORD[L]]) == (L + 6) % 12 and sign(c[LORD[(L + 6) % 12]]) == L)
    f["४+ ग्रह उच्च या स्वराशि में"] = sum(sign(c[p]) in OWN[p] or sign(c[p]) == EXALT[p] // 30 for p in SEVEN) >= 4
    f["सातों ग्रह केंद्र-त्रिकोण में"] = all(H(p) in (1, 4, 5, 7, 9, 10) for p in SEVEN)
    f["गुरु-चंद्र १° के भीतर"] = dist(c["Jupiter"], c["Moon"]) <= 1
    f["आत्मकारक २९° से ऊपर"] = max(c[p] % 30 for p in SEVEN) >= 29
    return f

def deg(s, d, m): return s * 30 + d + m / 60

if __name__ == "__main__":
    random.seed(3); N = 60_000
    rows = []
    for _ in range(N):
        c, r = chart(random_birth(1960, 2011), *place())
        rows.append(features(c, r))
    names = list(rows[0])
    p = {n: sum(r[n] for r in rows) / N for n in names}
    rare = [n for n in names if 0 < p[n] <= 0.05]
    counts = collections.Counter(sum(r[n] for n in rare) for r in rows)
    print(f"कुल उम्मीदवार योग: {len(names)}, जिनमें दुर्लभ (≤५%): {len(rare)}")
    for n in sorted(rare, key=lambda n: p[n]): print(f"  {100*p[n]:5.2f}%  {n}")
    mean = sum(k * v for k, v in counts.items()) / N
    print(f"\nएक कुंडली में औसत दुर्लभ योग: {mean:.2f}")
    cum = 0
    for k in sorted(counts, reverse=True):
        cum += counts[k]; print(f"  {k}: {100*counts[k]/N:6.2f}%  इतने या ज़्यादा: {100*cum/N:6.2f}%")

    D = {"Lagna": deg(8, 8, 34.6), "Sun": deg(5, 13, 24.8), "Moon": deg(5, 17, 42.7), "Mars": deg(5, 13, 15.0),
         "Mercury": deg(5, 3, 12.4), "Jupiter": deg(2, 15, 51.3), "Venus": deg(6, 26, 50.0),
         "Saturn": deg(8, 13, 53.8), "Rahu": deg(9, 29, 40.1), "Ketu": deg(3, 29, 40.1)}
    P = {"Lagna": deg(11, 11, 11.2), "Sun": deg(1, 3, 41.8), "Moon": deg(9, 0, 8.0), "Mars": deg(4, 3, 15.3),
         "Mercury": deg(1, 23, 23.3), "Jupiter": deg(7, 18, 25.5), "Venus": deg(0, 8, 33.7),
         "Saturn": deg(10, 29, 5.6), "Rahu": deg(6, 10, 41.1), "Ketu": deg(0, 10, 41.1)}
    for nm, c, r in (("दिनेश", D, {"Mercury"}), ("पी", P, {"Jupiter"})):
        f = features(c, r)
        hit = [n for n in rare if f[n]]
        print(f"\n{nm}: {len(hit)} दुर्लभ योग -> {hit}")
''',
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
def gana_pts(b, g):  # b = वर का गण, g = वधू का गण (0 देव, 1 मनुष्य, 2 राक्षस)
    if b == g: return 6
    if (b, g) == (0, 1): return 6   # वर देव, वधू मनुष्य (Parashara's Light से मेल)
    if (b, g) == (1, 0): return 5   # वर मनुष्य, वधू देव
    if {b, g} == {0, 2}: return 1
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
    'matrix_lock': r'''"""
D1-D9 मैट्रिक्स लॉक: ५ शर्तें, २ लाख रैंडम जोड़े (वर = b, वधू = g)।
"""
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
''',
    'rinanubandh': r'''"""
ऋणानुबंध जाँच: उपयोगकर्ता की दी हुई सूची के हर नियम को गणना-योग्य रूप में।
दोनों दिशाओं वाली जाँच = किसी भी एक दिशा में सच हो तो पास।
षष्ट्यंश (D60) छोड़ा गया, क्योंकि उसके लिए सटीक जन्म-समय चाहिए।
"""
import random, collections
from kundli_sim import random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from durlabh_yog import chart
from var_vadhu_suchi import karakas

LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def S(x): return sign(x)
def rel(a, b): return (S(a) - S(b)) % 12
def trine(a, b): return rel(a, b) in (0, 4, 8)
def trine7(a, b): return rel(a, b) in (0, 4, 8, 6)
def house(c, L): return (S(L) - S(c["Lagna"])) % 12 + 1
def dist(a, b): return abs((a - b + 180) % 360 - 180)
def bb(c): return (c["Rahu"] + ((c["Moon"] - c["Rahu"]) % 360) / 2) % 360
def lagnesh(c): return c[LORD[S(c["Lagna"])]]
def saptamesh_name(c): return LORD[(S(c["Lagna"]) + 6) % 12]
def saptamesh(c): return c[saptamesh_name(c)]

def rashi_drishti(a, b):  # जैमिनी राशि दृष्टि (राशि अंक 0..11)
    ma = a % 3; mb = b % 3  # 0 चर, 1 स्थिर, 2 द्विस्वभाव
    if ma == 2: return mb == 2 and a != b
    if ma == 0: return mb == 1 and (b - a) % 12 != 1
    return mb == 0 and (a - b) % 12 != 1

def ak_link(x, y):
    a, b = S(x), S(y)
    return a == b or rashi_drishti(a, b) or rashi_drishti(b, a)

def E(fn, b, g): return fn(b, g) or fn(g, b)

def checks(b, rb, g, rg):
    f = collections.OrderedDict()
    for t, n in (("Lagna", "लग्न"), ("Moon", "चंद्र"), ("Sun", "सूर्य"), ("Venus", "शुक्र")):
        f[f"१ केतु: एक का केतु दूसरे के {n} की राशि में"] = E(lambda x, y: S(x["Ketu"]) == S(y[t]), b, g)
    for t, n in (("Moon", "चंद्र"), ("Venus", "शुक्र"), ("Mars", "मंगल"), ("Lagna", "लग्न")):
        f[f"२ राहु: एक का राहु दूसरे के {n} की राशि में"] = E(lambda x, y: S(x["Rahu"]) == S(y[t]), b, g)
    tg = {"लग्नेश": lagnesh, "सप्तमेश": saptamesh, "शुक्र": lambda c: c["Venus"], "गुरु": lambda c: c["Jupiter"]}
    for n, fn in tg.items():
        f[f"३ भृगु बिंदु: दूसरे का {n} एक राशि या त्रिकोण में"] = E(lambda x, y: trine(fn(y), bb(x)), b, g)
    f["३क भृगु बिंदु: इनमें से कोई १° के भीतर"] = E(lambda x, y: any(dist(fn(y), bb(x)) <= 1 for fn in tg.values()), b, g)
    for p, pn in (("Venus", "शुक्र"), ("Mars", "मंगल")):
        for q, qn in (("Saturn", "शनि"), ("Ketu", "केतु")):
            f[f"४ नाड़ी: एक का {pn}, दूसरे के {qn} से त्रिकोण/सप्तम"] = E(lambda x, y: trine7(x[p], y[q]), b, g)
    f["५ वर: सप्तमेश या शुक्र ५/९ में"] = house(b, saptamesh(b)) in (5, 9) or house(b, b["Venus"]) in (5, 9)
    f["५ वधू: सप्तमेश या शुक्र ५/९ में"] = house(g, saptamesh(g)) in (5, 9) or house(g, g["Venus"]) in (5, 9)
    f["५क एक का सप्तमेश/शुक्र दूसरे के ५/९ में"] = E(lambda x, y: house(y, saptamesh(x)) in (5, 9) or house(y, x["Venus"]) in (5, 9), b, g)
    f["६ वर: सप्तमेश या शुक्र ८/१२ में"] = house(b, saptamesh(b)) in (8, 12) or house(b, b["Venus"]) in (8, 12)
    f["६ वधू: सप्तमेश या शुक्र ८/१२ में"] = house(g, saptamesh(g)) in (8, 12) or house(g, g["Venus"]) in (8, 12)
    f["६क एक का सप्तमेश/शुक्र दूसरे के ८/१२ में"] = E(lambda x, y: house(y, saptamesh(x)) in (8, 12) or house(y, x["Venus"]) in (8, 12), b, g)
    f["७ वर: शुक्र, मंगल या सप्तमेश वक्री"] = bool(rb & {"Venus", "Mars", saptamesh_name(b)})
    f["७ वधू: शुक्र, मंगल या सप्तमेश वक्री"] = bool(rg & {"Venus", "Mars", saptamesh_name(g)})
    f["८ जैमिनी: आत्मकारक-आत्मकारक युति या राशि दृष्टि"] = ak_link(b[karakas(b)[0]], g[karakas(g)[0]])
    f["८ जैमिनी: एक का आत्मकारक, दूसरे के दारकारक से युति या राशि दृष्टि"] = E(
        lambda x, y: ak_link(x[karakas(x)[0]], y[karakas(y)[6]]), b, g)
    f["९ नवांश: एक के लग्न/चंद्र/शुक्र/सप्तमेश की राशि = दूसरे का नवांश लग्न या चंद्र"] = E(
        lambda x, y: {S(x["Lagna"]), S(x["Moon"]), S(x["Venus"]), S(saptamesh(x))} & {nav(y["Lagna"]), nav(y["Moon"])}, b, g)
    return f

if __name__ == "__main__":
    print("भृगु बिंदु: दिनेश", divmod(bb(DINESH), 30), " पी", divmod(bb(P), 30))
    me = checks(DINESH, {"Mercury"}, P, {"Jupiter"}); my = sum(bool(v) for v in me.values())
    random.seed(2026); N = 150_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        (b, rb), (g, rg) = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = checks(b, rb, g, rg)
        for n, v in f.items(): single[n] += bool(v)
        total[sum(bool(v) for v in f.values())] += 1
    print(f"दिनेश-पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:70s} {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in total.items())/N:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]; print(f"  {c:2d}: {100*total[c]/N:6.3f}%   इतने या ज़्यादा: {100*cum/N:6.3f}%")
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
            if kk["nadi"] > 0 and sum(kk.values()) >= 25: exact_plus += 1
    print(f"\nN = {N}")
    print("हर संयोग अलग-अलग:")
    for n in fc: print(f"   {100*single[n]/N:5.1f}%  {n}")
    print("संयोगों की गिनती का वितरण:")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]
        print(f"   {c:2d}: {100*total[c]/N:6.3f}%   (इतने या ज़्यादा: {100*cum/N:6.3f}%)")
    print(f"इस जोड़े के सारे {my_n} संयोग एक साथ: {exact} ({100*exact/N:.4f}%)")
    print(f"  + नाड़ी दोष नहीं और गुण >= 25: {exact_plus} ({100*exact_plus/N:.4f}%)")
''',
    'var_vadhu_suchi': r'''"""
वर-वधू मिलान की तय सूची (२१ जाँचें), पहले से तय नियमों से।
रैंडम जोड़ों से तुलना और दिनेश-पी का स्थान।
"""
import random, collections
from kundli_sim import chart, random_birth, place, sign, nak, ashtakoot, manglik, rel
from sanyog_sim import nav, DINESH, P
from dashakoot_enum import RAJJU, VEDHA

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
CODE = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa"}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
DEBIL = {"Venus": 5, "Jupiter": 9}

def good_rel(a, b):  # 1-1, 1-7, 5-9
    return (a - b) % 12 in (0, 6, 4, 8)

def friends(p, q):  # एक ही ग्रह या दोनों ओर से मित्र
    if p == q: return True
    return rel(CODE[p], CODE[q]) == 2 and rel(CODE[q], CODE[p]) == 2

def house(c, p): return (sign(c[p]) - sign(c["Lagna"])) % 12 + 1

def karakas(c): return sorted(SEVEN, key=lambda p: -(c[p] % 30))

def checks(b, g):
    k = ashtakoot(b["Moon"], g["Moon"]); s = sum(k.values())
    bn, gn = nak(b["Moon"]), nak(g["Moon"])
    kb, kg = karakas(b), karakas(g)
    f = collections.OrderedDict()
    # क. कूट मिलान
    f["क१ अष्टकूट १८ या ज़्यादा"] = s >= 18
    f["क२ अष्टकूट २८ या ज़्यादा"] = s >= 28
    f["क३ नाड़ी दोष नहीं"] = k["nadi"] > 0
    f["क४ भकूट दोष नहीं"] = k["bhakoot"] > 0
    f["क५ गण दोष नहीं"] = k["gana"] >= 5
    f["क६ ग्रह मैत्री ४ या ज़्यादा"] = k["maitri"] >= 4
    f["क७ रज्जु दोष नहीं"] = RAJJU[bn] != RAJJU[gn]
    f["क८ वेध दोष नहीं"] = frozenset((bn, gn)) not in VEDHA
    f["क९ मांगलिक संतुलित (लग्न से)"] = manglik(b) == manglik(g)
    # ख. पाराशरी
    f["ख१ दोनों के लग्नेश एक या परस्पर मित्र"] = friends(LORD[sign(b["Lagna"])], LORD[sign(g["Lagna"])])
    f["ख२ वर का शुक्र ६/८/१२ में नहीं, नीच नहीं"] = house(b, "Venus") not in (6, 8, 12) and sign(b["Venus"]) != DEBIL["Venus"]
    f["ख३ वधू का गुरु ६/८/१२ में नहीं, नीच नहीं"] = house(g, "Jupiter") not in (6, 8, 12) and sign(g["Jupiter"]) != DEBIL["Jupiter"]
    f["ख४ वर का सप्तमेश ६/८/१२ में नहीं"] = house(b, LORD[(sign(b["Lagna"]) + 6) % 12]) not in (6, 8, 12)
    f["ख५ वधू का सप्तमेश ६/८/१२ में नहीं"] = house(g, LORD[(sign(g["Lagna"]) + 6) % 12]) not in (6, 8, 12)
    f["ख६ एक का चंद्र दूसरे के लग्न से केंद्र/त्रिकोण में"] = (
        (sign(b["Moon"]) - sign(g["Lagna"])) % 12 + 1 in (1, 4, 5, 7, 9, 10) or
        (sign(g["Moon"]) - sign(b["Lagna"])) % 12 + 1 in (1, 4, 5, 7, 9, 10))
    # ग. जैमिनी
    f["ग१ आत्मकारक एक या परस्पर मित्र"] = friends(kb[0], kg[0])
    f["ग२ आत्मकारक राशि १-१/१-७/त्रिकोण"] = good_rel(sign(b[kb[0]]), sign(g[kg[0]]))
    f["ग३ दारकारक राशि १-१/१-७/त्रिकोण"] = good_rel(sign(b[kb[6]]), sign(g[kg[6]]))
    f["ग४ कारकांश १-१/१-७/त्रिकोण"] = good_rel(nav(b[kb[0]]), nav(g[kg[0]]))
    # घ. नवांश
    f["घ१ नवांश लग्न १-१/१-७/त्रिकोण"] = good_rel(nav(b["Lagna"]), nav(g["Lagna"]))
    f["घ२ नवांश चंद्र १-१/१-७/त्रिकोण"] = good_rel(nav(b["Moon"]), nav(g["Moon"]))
    return f

if __name__ == "__main__":
    me = checks(DINESH, P); my = sum(me.values())
    random.seed(101); N = 200_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = checks(b, g)
        for n, v in f.items(): single[n] += v
        total[sum(f.values())] += 1
    print(f"दिनेश-पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:45s} रैंडम में {100*single[n]/N:5.1f}%")
    mean = sum(c * n for c, n in total.items()) / N
    print(f"औसत: {mean:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]; print(f"  {c:2d}: {100*total[c]/N:6.3f}%   इतने या ज़्यादा: {100*cum/N:6.3f}%")
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

import random, collections
import swisseph as swe
from kundli_sim import place, sign, nak, ashtakoot
from durlabh_yog import chart
from sanyog_sim import DINESH, P
from dashakoot_enum import dashakoot
import var_vadhu_suchi as vv, rinanubandh as rn, matrix_lock as ml

D_JD = swe.julday(1989, 9, 30, 7.2)
D_R = {"Mercury"}

def score(g, rg):
    s = {}
    a = ashtakoot(DINESH["Moon"], g["Moon"]); s["ak"] = sum(a.values()); s["nadi"] = a["nadi"] > 0
    k = dashakoot(nak(DINESH["Moon"]), sign(DINESH["Moon"]), nak(g["Moon"]), sign(g["Moon"]))
    s["dk"] = sum(k.values()) if (k["रज्जु"] and k["वेध"]) else 0
    s["vv"] = sum(vv.checks(DINESH, g).values())
    s["rn"] = sum(bool(v) for v in rn.checks(DINESH, D_R, g, rg).values())
    c = ml.conds(DINESH, g); s["ml"] = all(c[x] for x in (1, 2, 3, "4", 5))
    return s

me = score(P, {"Jupiter"})
print("पी:", me)
random.seed(777); N = 200_000
cnt = collections.Counter(); vvd = collections.Counter()
for _ in range(N):
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    g, rg = chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place())
    s = score(g, rg); vvd[s["vv"]] += 1
    ak = s["ak"] >= me["ak"] and s["nadi"]
    cnt["अष्टकूट (२५+, नाड़ी ठीक)"] += ak
    cnt["दशकूट (७.५+, रज्जु-वेध साफ़)"] += s["dk"] >= me["dk"]
    cnt["वर-वधू सूची (१८+/२१)"] += s["vv"] >= me["vv"]
    cnt["ऋणानुबंध सूची (१२+/२८)"] += s["rn"] >= me["rn"]
    cnt["वर-वधू + ऋणानुबंध"] += s["vv"] >= me["vv"] and s["rn"] >= me["rn"]
    cnt["मैट्रिक्स लॉक (५ शर्तें)"] += s["ml"]
print(f"N = {N:,} वधुएँ")
for n, v in cnt.items(): print(f"{n:32s} {v:7,}  {100*v/N:7.3f}%  " + (f"~1 in {N/v:,.0f}" if v else ""))
print("वर-वधू सूची वितरण (इतने या ज़्यादा):")
cum = 0
for k in sorted(vvd, reverse=True):
    cum += vvd[k]; print(f"  {k:2d}: {100*cum/N:6.3f}%")
