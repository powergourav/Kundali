"""
४५ बिंदु मिलान: दिनेश के सभी ४५ बिंदु (जगन्नाथ होरा तालिका) स्थिर,
वधू के वे २६ बिंदु जिनका सूत्र केवल ग्रह-अंशों और लग्न से बनता है।
(गुलिक, मांदि, होरा/घटी/भाव/वर्णद/श्री/प्राणपद लग्न, काल-मृत्यु आदि उपग्रह
 सूर्योदय के समय पर टिके हैं, वे रैंडम वधुओं में नहीं गिने गए।)
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

# swisseph केवल ग्रह-स्थिति (chart, random_birth) के लिए चाहिए।
# कूट मिलान की गणना (अष्टकूट, दशकूट) इसके बिना भी चलती है।
try:
    import swisseph as swe
except ImportError:
    swe = None

if swe is not None:
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    FLG = swe.FLG_SIDEREAL
    PL = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
          "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}

def need_swe():
    if swe is None:
        raise ImportError("ग्रह-स्थिति के लिए pyswisseph चाहिए: pip install pyswisseph")

def chart(jd, lat, lon):
    need_swe()
    c = {}
    for n, p in PL.items():
        c[n] = swe.calc_ut(jd, p, FLG)[0][0]
    c["Ketu"] = (c["Rahu"] + 180) % 360
    c["Lagna"] = swe.houses_ex(jd, lat, lon, b"W", FLG)[1][0]
    return c

def random_birth(y0, y1):
    need_swe()
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
# योनि अंक (४ समान, ३ मित्र, २ सम, १ शत्रु, ० महाशत्रु)। क्रम:
# अश्व, गज, मेष, सर्प, श्वान, मार्जार, मूषक, गौ, महिष, व्याघ्र, मृग, वानर, नकुल, सिंह
YONI_PTS = [
    [4, 2, 2, 3, 2, 2, 2, 1, 0, 1, 3, 3, 2, 1],
    [2, 4, 3, 3, 2, 2, 2, 2, 3, 1, 2, 3, 2, 0],
    [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 3, 1],
    [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 0, 2],
    [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 2, 1, 1],
    [2, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 3, 2, 1],
    [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 2, 1, 2],
    [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 1],
    [0, 3, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 1],
    [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 1, 2, 1],
    [3, 2, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 2, 1],
    [3, 3, 0, 2, 2, 3, 2, 2, 2, 1, 2, 4, 3, 2],
    [2, 2, 3, 0, 1, 2, 1, 2, 2, 2, 2, 3, 4, 2],
    [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 4],
]

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
    k["yoni"] = YONI_PTS[yb][yg]
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
    'sabhi_bindu': r'''"""
जगन्नाथ होरा की दोनों तालिकाओं के सभी बिंदुओं में से कितने जोड़े आपस में १° के भीतर हैं,
और रैंडम अपेक्षा कितनी है।
"""
import random
S = {s: i for i, s in enumerate("Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi".split())}

P_TXT = """Lagna 11 Pi 11 14.87|Sun 3 Ta 41 49.80|Moon 0 Cp 08 00.48|Mars 3 Le 15 18.18|Mercury 23 Ta 23 16.67|Jupiter 18 Sc 25 27.38|Venus 8 Ar 33 40.41|Saturn 29 Aq 05 36.30|Rahu 10 Li 41 08.30|Ketu 10 Ar 41 08.30|Maandi 1 Pi 46 04.28|Gulika 18 Aq 39 13.72|BhavaL 18 Pi 01 35.25|HoraL 3 Aq 11 55.50|GhatiL 18 Vi 42 56.23|VighatiL 6 Sc 17 59.90|VarnadaL 11 Ge 11 14.87|SreeL 14 Ge 47 27.73|PranapadaL 7 Cn 08 34.69|InduL 0 Aq 08 00.48|BhriguB 20 Sc 24 34.39|Dhooma 17 Vi 01 49.80|Vyatipata 12 Li 58 10.20|Parivesha 12 Ar 58 10.20|IndraChapa 17 Pi 01 49.80|Upaketu 3 Ar 41 49.80|Kaala 22 Ar 31 01.27|Mrityu 1 Sg 29 10.43|ArthaPrahara 21 Sg 00 37.43|YamaGhantaka 12 Cp 14 40.75|PranaSph 14 Sc 35 28.07|DehaSph 19 Aq 43 17.53|MrityuSph 14 Cn 16 25.82|SookTri 18 Cp 35 11.42|TithiSph 26 Sc 26 10.68|YogaSphSM 3 Aq 49 50.28|RahuTithi 6 Vi 59 18.50|Kshetra 21 Sg 48 46.04|Beeja 0 Cp 40 57.60|TriSph 29 Li 58 29.06|Chatus 3 Sg 40 18.86|Pancha 14 Ge 21 27.17|Kunda 6 Cp 11 04.56|YogaSph 7 Ta 09 50.28|Avayoga 13 Sc 49 50.28"""
D_TXT = """Lagna 8 Sg 34 33.06|Sun 13 Vi 24 50.94|Moon 17 Vi 42 42.68|Mars 13 Vi 14 57.35|Mercury 3 Vi 12 22.87|Jupiter 15 Ge 51 15.63|Venus 26 Li 49 57.49|Saturn 13 Sg 53 46.03|Rahu 29 Cp 40 07.06|Ketu 29 Cn 40 07.06|Maandi 23 Vi 13 30.68|Gulika 13 Vi 09 24.38|BhavaL 19 Sg 15 57.94|HoraL 25 Pi 22 49.80|GhatiL 13 Cp 43 25.38|VighatiL 15 Cp 26 23.29|VarnadaL 8 Sc 34 33.06|SreeL 6 Cn 47 45.53|PranapadaL 15 Ta 42 08.15|InduL 17 Aq 42 42.68|BhriguB 23 Ta 41 24.87|Dhooma 26 Cp 44 50.94|Vyatipata 3 Ge 15 09.06|Parivesha 3 Sg 15 09.06|IndraChapa 26 Cn 44 50.94|Upaketu 13 Le 24 50.94|Kaala 2 Sc 30 38.66|Mrityu 11 Sg 59 48.24|ArthaPrahara 4 Cp 07 31.33|YamaGhantaka 29 Cp 34 51.50|PranaSph 26 Aq 02 09.67|DehaSph 4 Ge 51 05.86|MrityuSph 15 Sc 30 41.63|SookTri 16 Sg 23 57.16|TithiSph 4 Ar 17 51.75|YogaSphSM 1 Pi 07 33.62|RahuTithi 16 Le 15 16.13|Kshetra 16 Ta 48 55.66|Beeja 26 Ge 06 04.05|TriSph 9 Sc 26 40.13|Chatus 22 Ar 51 31.06|Pancha 22 Aq 31 38.12|Kunda 4 Pi 38 37.69|YogaSph 4 Ge 27 33.62|Avayoga 11 Sg 07 33.62"""

def parse(t):
    out = {}
    for row in t.split("|"):
        n, d, s, m, sec = row.split()
        out[n] = S[s] * 30 + int(d) + int(m) / 60 + float(sec) / 3600
    return out

def dist(a, b): return abs((a - b + 180) % 360 - 180)

P, D = parse(P_TXT), parse(D_TXT)
if __name__ == "__main__":
    pairs = [(a, b, dist(P[a], D[b])) for a in P for b in D]
    for lim in (1, 1/3):
        hits = sorted([x for x in pairs if x[2] <= lim], key=lambda x: x[2])
        exp = len(pairs) * 2 * lim / 360
        print(f"\n{lim*60:.0f} कला के भीतर: {len(hits)} जोड़े (रैंडम अपेक्षा ~{exp:.1f}), कुल तुलनाएँ {len(pairs)}")
        for a, b, d in hits: print(f"   पी {a:12s} - दिनेश {b:12s} {d*60:5.1f}'")
    # सटीक अनुमान: दिनेश के बिंदुओं को रैंडम घुमाकर
    random.seed(1); cnt = []
    for _ in range(2000):
        sh = random.uniform(0, 360)
        cnt.append(sum(dist(P[a], D[b] + sh) <= 1 for a in P for b in D))
    cnt.sort()
    print(f"\nरैंडम घुमाव पर १° के भीतर जोड़े: औसत {sum(cnt)/len(cnt):.1f}, 5%-95%: {cnt[100]}-{cnt[1900]}")
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
import swisseph as swe
from kundli_sim import chart, place, sign
from sabhi_bindu import parse, P_TXT, D_TXT, dist

KALA = {"Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8, "Jupiter": 10, "Venus": 12, "Saturn": 1}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def derived(c):
    p = {k: c[k] for k in ("Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")}
    su, mo = c["Sun"], c["Moon"]
    p["Dhooma"] = (su + 133 + 1 / 3) % 360
    p["Vyatipata"] = (360 - p["Dhooma"]) % 360
    p["Parivesha"] = (p["Vyatipata"] + 180) % 360
    p["IndraChapa"] = (360 - p["Parivesha"]) % 360
    p["Upaketu"] = (p["IndraChapa"] + 16 + 2 / 3) % 360
    p["BhriguB"] = (c["Rahu"] + ((mo - c["Rahu"]) % 360) / 2) % 360
    p["YogaSphSM"] = (su + mo) % 360
    p["YogaSph"] = (su + mo + 93 + 1 / 3) % 360
    p["Avayoga"] = (p["YogaSph"] + 186 + 2 / 3) % 360
    p["TithiSph"] = (mo - su) % 360
    p["RahuTithi"] = (c["Rahu"] - su) % 360
    p["Beeja"] = (su + c["Venus"] + c["Jupiter"]) % 360
    p["Kshetra"] = (mo + c["Mars"] + c["Jupiter"]) % 360
    p["Kunda"] = (c["Lagna"] * 81) % 360
    L, M = sign(c["Lagna"]), sign(mo)
    r = (KALA[LORD[(L + 8) % 12]] + KALA[LORD[(M + 8) % 12]]) % 12 or 12
    p["InduL"] = ((M + r - 1) % 12) * 30 + mo % 30
    return p

def hits(dpts, bpts, orb):
    return sum(dist(a, b) <= orb for a in dpts.values() for b in bpts.values())

if __name__ == "__main__":
    D, PT = parse(D_TXT), parse(P_TXT)
    mine = derived(PT)
    err = max(dist(mine[k], PT[k]) for k in mine)
    print(f"सूत्र जाँच: पी के २६ बिंदु जगन्नाथ होरा से अधिकतम {err*60:.1f} कला अलग")
    Pb = {k: PT[k] for k in mine}
    me1, me20 = hits(D, Pb, 1), hits(D, Pb, 1 / 3)
    print(f"पी: १° के भीतर {me1}, २० कला के भीतर {me20}")
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(4545); N = 200_000
    t1 = t20 = ge1 = ge20 = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        g = derived(chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place()))
        a, b = hits(D, g, 1), hits(D, g, 1 / 3)
        t1 += a; t20 += b; ge1 += a >= me1; ge20 += b >= me20
    print(f"N = {N:,} वधुएँ, तुलनाएँ प्रति वधू: {45*26}")
    print(f"१° के भीतर: औसत {t1/N:.2f}, पी जितने या ज़्यादा: {100*ge1/N:.1f}%")
    print(f"२० कला के भीतर: औसत {t20/N:.2f}, पी जितने या ज़्यादा: {100*ge20/N:.1f}%")
