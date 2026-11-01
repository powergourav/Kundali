"""
कुंडली मिलान के सभी विश्लेषण, एक ही फ़ाइल में।

    python kundli_all.py                  # सूची
    python kundli_all.py dashakoot_44     # एक विश्लेषण
    python kundli_all.py all              # सभी (बहुत समय लगता है)

केवल pyswisseph चाहिए (कूट मिलान वाले विश्लेषण उसके बिना भी चलते हैं)।
tools/make_standalone.py से अपने-आप बनाया गया; बदलाव src/ में करें।
"""
# ---- अंदर रखी गई सहायक फ़ाइलें: यह फ़ाइल अकेले चलती है, दूसरी फ़ाइल की ज़रूरत नहीं ----
# (tools/make_standalone.py से अपने-आप बनाया गया; बदलाव src/ में करें)
import sys as _sys, importlib.abc as _iabc, importlib.util as _iutil

_EMBEDDED = {
    'antim_milan': r'''"""
अंतिम संयुक्त जाँच: दिनेश स्थिर, २ लाख रैंडम वधुएँ, सभी मुख्य कसौटियाँ एक ही वधुओं पर।
"""
import random, collections
import swisseph as swe
from kundli_sim import place, sign, nak, ashtakoot
from durlabh_yog import chart as chart_r
from sanyog_sim import DINESH, P
from dashakoot_44 import score44
import var_vadhu_suchi as vv, rinanubandh as rn, jaimini_dinesh as jm, bb_sree_dinesh as bs, matrix_lock as ml

D_JD = swe.julday(1989, 9, 30, 7.2)
def S(g, rg):
    s = {}
    a = ashtakoot(DINESH["Moon"], g["Moon"]); s["अष्टकूट"] = sum(a.values())
    s["_nadi"] = a["nadi"] > 0
    s["दशकूट ४४"] = score44(DINESH["Moon"], nak(DINESH["Moon"]), sign(DINESH["Moon"]), g["Moon"], nak(g["Moon"]), sign(g["Moon"]))
    s["वर-वधू सूची"] = sum(vv.checks(DINESH, g).values())
    s["ऋणानुबंध सूची"] = sum(bool(v) for v in rn.checks(DINESH, {"Mercury"}, g, rg).values())
    s["जैमिनी १२"] = sum(jm.checks(DINESH, g).values())
    b = bs.score(DINESH, g); s["भृगु-श्री"] = (b["राशि संबंध"], b["१°"], b["२°"])
    c = ml.conds(DINESH, g); s["मैट्रिक्स लॉक"] = all(c[x] for x in (1, 2, 3, "4", 5))
    return s

def ok(s, me, k):
    if k == "भृगु-श्री": return all(x >= y for x, y in zip(s[k], me[k]))
    if k == "अष्टकूट": return s[k] >= me[k] and s["_nadi"]
    return s[k] >= me[k]

me = S(P, {"Jupiter"}); print("पी:", me)
KEYS = ["अष्टकूट", "दशकूट ४४", "वर-वधू सूची", "ऋणानुबंध सूची", "जैमिनी १२", "भृगु-श्री", "मैट्रिक्स लॉक"]
GROUPS = {
    "दशकूट + वर-वधू": ["दशकूट ४४", "वर-वधू सूची"],
    "वर-वधू + जैमिनी": ["वर-वधू सूची", "जैमिनी १२"],
    "दशकूट + वर-वधू + जैमिनी": ["दशकूट ४४", "वर-वधू सूची", "जैमिनी १२"],
    "दशकूट + वर-वधू + जैमिनी + भृगु-श्री": ["दशकूट ४४", "वर-वधू सूची", "जैमिनी १२", "भृगु-श्री"],
    "मैट्रिक्स लॉक छोड़कर सभी": KEYS[:-1],
}
random.seed(31031); N = 200_000
one = collections.Counter(); grp = collections.Counter()
for _ in range(N):
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    g, rg = chart_r(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place())
    s = S(g, rg); r = {k: ok(s, me, k) for k in KEYS}
    for k in KEYS: one[k] += r[k]
    for n, ks in GROUPS.items(): grp[n] += all(r[k] for k in ks)
print(f"N = {N:,} वधुएँ")
for k in KEYS: v = one[k]; print(f"{k:20s} {100*v/N:7.3f}%  " + (f"~1 in {N/v:,.0f}" if v else "0"))
for k, v in grp.items(): print(f"{k:40s} {v:6d} {100*v/N:7.4f}%  " + (f"~1 in {N/v:,.0f}" if v else "0"))
''',
    'ashtakoot_10lakh': r'''"""
अष्टकूट: १० लाख रैंडम वर-वधू जोड़े (केवल चंद्र पर निर्भर)।
"""
import random, collections
import swisseph as swe
from kundli_sim import ashtakoot, random_birth

swe.set_sid_mode(swe.SIDM_LAHIRI)
moon = lambda jd: swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
DINESH_M, P_M = 150 + 17 + 42.7 / 60, 270 + 8.0 / 60
me = ashtakoot(DINESH_M, P_M); my = sum(me.values())
print("दिनेश-पी:", me, "कुल", my)

random.seed(2000); N = 1_000_000
dist = collections.Counter(); kut = collections.Counter(); c = collections.Counter()
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    k = ashtakoot(moon(jb), moon(jb + gap * 365.25)); s = sum(k.values())
    dist[int(s)] += 1
    for n, v in k.items(): kut[n] += v == me[n] or v >= me[n]
    c["≥18"] += s >= 18; c["≥my"] += s >= my; c["≥28"] += s >= 28; c["≥32"] += s >= 32
    c["≥my नाड़ी ठीक"] += s >= my and k["nadi"] > 0
    c["≥my नाड़ी-भकूट दोनों ठीक"] += s >= my and k["nadi"] > 0 and k["bhakoot"] > 0
    c["नाड़ी दोष"] += k["nadi"] == 0; c["भकूट दोष"] += k["bhakoot"] == 0
print(f"N = {N:,}")
cum = 0
for s in sorted(dist, reverse=True):
    cum += dist[s]; print(f"  {s:2d}: {100*dist[s]/N:5.2f}%   इतना या ज़्यादा: {100*cum/N:6.2f}%")
for n, v in c.items(): print(f"{n}: {100*v/N:.2f}%  (~1 in {N/v:.1f})")
print("हर कूट में दिनेश-पी जितना या ज़्यादा:")
for n, v in kut.items(): print(f"  {n}: {100*v/N:.1f}%")
''',
    'bb_sree_dinesh': r'''"""
भृगु बिंदु और श्री लग्न मिलान: दिनेश स्थिर, वधू रैंडम (२ लाख)।
एक के चंद्र, लग्नेश, सप्तमेश को दूसरे के भृगु बिंदु और श्री लग्न से (दोनों दिशाएँ),
और बिंदु-से-बिंदु।
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign
from sanyog_sim import DINESH, P
from sabhi_bindu import dist

LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
NAK = 40 / 3

def bb(c): return (c["Rahu"] + ((c["Moon"] - c["Rahu"]) % 360) / 2) % 360
def sree(c): return (c["Lagna"] + ((c["Moon"] % NAK) / NAK) * 360) % 360
def pts(c):
    L = sign(c["Lagna"])
    return {"चंद्र": c["Moon"], "लग्नेश": c[LORD[L]], "सप्तमेश": c[LORD[(L + 6) % 12]]}
def good_sign(a, b): return (sign(a) - sign(b)) % 12 in (0, 4, 6, 8)
def close(a, b, orb): return dist(a, b) <= orb or dist(a, (b + 180) % 360) <= orb  # युति या समसप्तक

def score(b, g):
    tb = {"भृगु": bb(b), "श्री": sree(b)}; tg = {"भृगु": bb(g), "श्री": sree(g)}
    s = collections.Counter()
    for X, TY in ((pts(b), tg), (pts(g), tb)):
        for x in X.values():
            for t in TY.values():
                s["राशि संबंध"] += good_sign(x, t)
                s["१°"] += close(x, t, 1); s["२°"] += close(x, t, 2)
    for a in tb.values():
        for c in tg.values():
            s["राशि संबंध"] += good_sign(a, c)
            s["१°"] += close(a, c, 1); s["२°"] += close(a, c, 2)
    s["वधू सप्तमेश वर के भृगु पर १°"] = close(pts(g)["सप्तमेश"], tb["भृगु"], 1)
    return s

if __name__ == "__main__":
    print("जाँच: श्री लग्न दिनेश", divmod(sree(DINESH), 30), "पी", divmod(sree(P), 30))
    me = score(DINESH, P); print("पी:", dict(me))
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(5151); N = 200_000
    ge = collections.Counter(); tot = collections.Counter(); allthree = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        s = score(DINESH, chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place()))
        for k in ("राशि संबंध", "१°", "२°", "वधू सप्तमेश वर के भृगु पर १°"):
            tot[k] += s[k]; ge[k] += s[k] >= me[k]
        allthree += all(s[k] >= me[k] for k in ("राशि संबंध", "१°", "२°"))
    print(f"N = {N:,}")
    for k in tot: print(f"{k}: औसत {tot[k]/N:.2f}, पी जितने या ज़्यादा {100*ge[k]/N:.2f}%")
    print(f"राशि संबंध + १° + २° तीनों में पी जितना या बेहतर: {100*allthree/N:.2f}%")
''',
    'bhrigu_saham': r'''"""
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
''',
    'bindu45_dinesh': r'''"""
४५ बिंदु मिलान: दिनेश के सभी ४५ बिंदु (जगन्नाथ होरा तालिका) स्थिर,
वधू के वे २६ बिंदु जिनका सूत्र केवल ग्रह-अंशों और लग्न से बनता है।
(गुलिक, मांदि, होरा/घटी/भाव/वर्णद/श्री/प्राणपद लग्न, काल-मृत्यु आदि उपग्रह
 सूर्योदय के समय पर टिके हैं, वे रैंडम वधुओं में नहीं गिने गए।)
"""
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
''',
    'dashakoot_10lakh': r'''"""
दशकूट: १० लाख रैंडम वर-वधू जोड़े (Swiss Ephemeris, लाहिड़ी)।
दशकूट केवल चंद्र पर निर्भर है, इसलिए केवल चंद्र की गणना।
"""
import random, collections
import swisseph as swe
from kundli_sim import sign, nak, ashtakoot, random_birth
from dashakoot_enum import dashakoot

swe.set_sid_mode(swe.SIDM_LAHIRI)
moon = lambda jd: swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]

ME = 7.5  # दिनेश-पी
random.seed(1000); N = 1_000_000
dist = collections.Counter(); ge = clean = clean_ak = 0
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    bm, gm = moon(jb), moon(jb + gap * 365.25)
    k = dashakoot(nak(bm), sign(bm), nak(gm), sign(gm))
    s = sum(k.values()); dist[s] += 1
    if s >= ME:
        ge += 1
        if k["रज्जु"] and k["वेध"]:
            clean += 1
            a = ashtakoot(bm, gm)
            if a["nadi"] > 0 and sum(a.values()) >= 25: clean_ak += 1
print(f"N = {N:,}")
cum = 0
for s in sorted(dist, reverse=True):
    cum += dist[s]; print(f"  {s:4.1f}/10 : {100*dist[s]/N:6.2f}%   इतना या ज़्यादा: {100*cum/N:6.2f}%")
for n, v in [("७.५ या ज़्यादा", ge), ("+ रज्जु-वेध साफ़", clean), ("+ अष्टकूट >=२५ और नाड़ी दोष नहीं", clean_ak)]:
    print(f"{n}: {v:,} ({100*v/N:.2f}%, ~1 in {N/v:.1f})")
''',
    'dashakoot_44': r'''"""
Parashara's Light का दशकूट (कालप्रकाशिका विधि, ४४ अंक) - पूरी गणना।
अधिकतम अंक (रिपोर्ट के कुल से निकाले गए): दिन ३, गण ६, माहेंद्र २, स्त्री-दीर्घ २,
योनि ४, राशि ७, राशीश ५, वश्य २, रज्जु ८, वेध २ = ४१; लिंग १, गोत्र १, वर्ण १ = ३।
गोत्र (नक्षत्र-गोत्र) की तालिका उपलब्ध नहीं, इसलिए हमेशा १ माना गया।
"""
import collections
from kundli_sim import ashtakoot
from dashakoot_enum import dashakoot, pada_info

def score44(Lb, bn, bs, Lg, gn, gs):
    # dashakoot() हर कूट को शुभ/मध्यम/अशुभ (१/०.५/०) में देता है। योनि (०-४),
    # राशीश (०-५) और वर्ण के क्रमिक अंक उसमें नहीं हैं, इसलिए वे ashtakoot() से लिए जाते हैं।
    k = dashakoot(bn, bs, gn, gs); a = ashtakoot(Lb, Lg)
    s = (3 * k["दिन"] + 6 * k["गण"] + 2 * k["माहेंद्र"] + 2 * k["स्त्री-दीर्घ"] + a["yoni"]
         + 7 * k["राशि"] + a["maitri"] + 2 * k["वश्य"] + 8 * k["रज्जु"] + 2 * k["वेध"])
    return s + 1 + 1 + a["varna"]   # लिंग, गोत्र, वर्ण

if __name__ == "__main__":
    DB, DG = 12 * 4 + 2, 20 * 4 + 1          # हस्त ३, उत्तराषाढ़ा २
    me = score44(*pada_info(DB), *pada_info(DG))
    print("दिनेश-पी:", me, "/ ४४")
    both = collections.Counter(); fixed = collections.Counter()
    for pb in range(108):
        for pg in range(108):
            s = score44(*pada_info(pb), *pada_info(pg))
            both[s] += 1
            if pb == DB: fixed[s] += 1
    for name, d, n in (("दोनों रैंडम", both, 108 * 108), ("दिनेश स्थिर", fixed, 108)):
        ge = sum(v for s, v in d.items() if s >= me)
        print(f"\n{name}: {me}+ पाने वाले {100*ge/n:.2f}%  (~1 in {n/ge:.1f})")
        cum = 0
        for s in sorted(d, reverse=True):
            cum += d[s]
            if s >= 30 or s == me: print(f"   {s:4.1f}: इतना या ज़्यादा {100*cum/n:6.2f}%")
''',
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
    'dinesh_fixed': r'''"""
दिनेश (वर) की कुंडली स्थिर, वधू की कुंडली रैंडम।
वधू का जन्म: दिनेश (३० सितंबर १९८९) से औसतन ३.५ वर्ष बाद, भारत में रैंडम स्थान।
"""
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
''',
    'double_lock': r'''"""
"दोहरा लॉक": राशि कुंडली में राहु-केतु विपरीत, नवांश में एक ही क्रम।
भाव के आधार पर और राशि के आधार पर, दोनों तरह से जाँच।
"""
import random
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from rinanubandh import saptamesh

def h(pl, lg): return (pl - lg) % 12  # भाव (0 = पहला)

def info(b, g):
    r = {}
    r["d1_house_rev"] = (h(sign(b["Rahu"]), sign(b["Lagna"])) - h(sign(g["Rahu"]), sign(g["Lagna"]))) % 12 == 6
    r["d9_house_same"] = h(nav(b["Rahu"]), nav(b["Lagna"])) == h(nav(g["Rahu"]), nav(g["Lagna"]))
    r["d1_sign_rev"] = (sign(b["Rahu"]) - sign(g["Rahu"])) % 12 == 6
    r["d9_sign_same"] = nav(b["Rahu"]) == nav(g["Rahu"])
    def touch(x, y):
        axis = {sign(y["Rahu"]), sign(y["Ketu"])}
        return bool(axis & {sign(x["Moon"]), sign(x["Venus"]), sign(x["Lagna"]), sign(saptamesh(x))})
    r["touch"] = touch(b, g) or touch(g, b)
    return r

if __name__ == "__main__":
    me = info(DINESH, P)
    print("दिनेश-पी:", me)
    random.seed(4); N = 200_000
    keys = ["d1_house_rev", "d9_house_same", "house_lock", "house_lock_touch", "d1_sign_rev", "d9_sign_same", "sign_lock", "touch"]
    c = dict.fromkeys(keys, 0)
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        r = info(b, g)
        r["house_lock"] = r["d1_house_rev"] and r["d9_house_same"]
        r["house_lock_touch"] = r["house_lock"] and r["touch"]
        r["sign_lock"] = r["d1_sign_rev"] and r["d9_sign_same"]
        for k in keys: c[k] += r[k]
    for k in keys:
        v = c[k]; print(f"{k:18s} {100*v/N:7.3f}%  " + (f"(~1 in {N/v:,.0f})" if v else ""))
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
    'jaimini_dashakoot_paas': r'''"""
दिनेश स्थिर। केवल वे रैंडम वधुएँ जो दशकूट (४४ अंक) पास करती हैं,
उन्हीं में जैमिनी मिलान (१२ जाँचें) की तुलना।
"पास" के तीन स्तर: रज्जु-वेध साफ़ और ५०% (२२/४४) या ज़्यादा; ३०/४४ या ज़्यादा; ३७/४४ (पी का स्तर)।
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign, nak
from sanyog_sim import DINESH, P
from dashakoot_enum import dashakoot
from dashakoot_44 import score44
from jaimini_dinesh import checks

def dk44(g):
    m = g["Moon"]
    k = dashakoot(nak(DINESH["Moon"]), sign(DINESH["Moon"]), nak(m), sign(m))
    s = score44(DINESH["Moon"], nak(DINESH["Moon"]), sign(DINESH["Moon"]), m, nak(m), sign(m))
    return s, bool(k["रज्जु"] and k["वेध"])

LEVELS = {"दशकूट पास (रज्जु-वेध साफ़, २२/४४+)": lambda s, c: c and s >= 22,
          "दशकूट ३०/४४+ (रज्जु-वेध साफ़)": lambda s, c: c and s >= 30,
          "दशकूट ३७/४४ (पी का स्तर)": lambda s, c: c and s >= 37}

if __name__ == "__main__":
    ps, pc = dk44(P); pj = sum(checks(DINESH, P).values())
    print(f"पी: दशकूट {ps}/४४ (रज्जु-वेध साफ़: {pc}), जैमिनी {pj}/१२")
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(3737); N = 200_000
    dist = {n: collections.Counter() for n in LEVELS}
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        g = chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place())
        s, c = dk44(g)
        passed = [n for n, f in LEVELS.items() if f(s, c)]
        if not passed: continue
        j = sum(checks(DINESH, g).values())
        for n in passed: dist[n][j] += 1
    print(f"N = {N:,} रैंडम वधुएँ\n")
    for n, d in dist.items():
        tot = sum(d.values()); ge = sum(v for k, v in d.items() if k >= pj)
        mean = sum(k * v for k, v in d.items()) / tot
        print(f"{n}: {tot:,} वधुएँ ({100*tot/N:.2f}%), जैमिनी औसत {mean:.2f}")
        print(f"   इनमें जैमिनी {pj}+ : {ge} ({100*ge/tot:.2f}%, ~1 in {tot/ge:,.0f})" if ge else "   इनमें जैमिनी {pj}+ : 0")
        cum = 0
        for k in sorted(d, reverse=True):
            cum += d[k]; print(f"     {k:2d}: इतने या ज़्यादा {100*cum/tot:6.2f}%")
        print()
''',
    'jaimini_dinesh': r'''"""
जैमिनी गहरा मिलान: दिनेश स्थिर, वधू रैंडम (२ लाख)।
१२ जाँचें, दोनों दिशाओं में बराबर।
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign, rel
from sanyog_sim import nav, DINESH, P
from rinanubandh import ak_link

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
CODE = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa"}
def K(c): return sorted(SEVEN, key=lambda p: -(c[p] % 30))
def good(a, b): return (a - b) % 12 in (0, 4, 6, 8)   # १-१, १-७, त्रिकोण
def friends(p, q): return p == q or (rel(CODE[p], CODE[q]) == 2 and rel(CODE[q], CODE[p]) == 2)

def checks(b, g):
    kb, kg = K(b), K(g)
    akb, akg, dkb, dkg = kb[0], kg[0], kb[6], kg[6]
    KKb, KKg = nav(b[akb]), nav(g[akg])
    f = collections.OrderedDict()
    f["१ आत्मकारक एक ग्रह या परस्पर मित्र"] = friends(akb, akg)
    f["२ आत्मकारक राशियाँ १-१/१-७/त्रिकोण"] = good(sign(b[akb]), sign(g[akg]))
    f["३ आत्मकारकों में युति या जैमिनी राशि दृष्टि"] = ak_link(b[akb], g[akg])
    f["४ दारकारक राशियाँ १-१/१-७/त्रिकोण"] = good(sign(b[dkb]), sign(g[dkg]))
    f["५ कारकांश एक ही"] = KKb == KKg
    f["६ दारकारक का नवांश एक ही"] = nav(b[dkb]) == nav(g[dkg])
    f["७ वधू के कारकांश से सप्तम = वर का लग्न"] = (KKg + 6) % 12 == sign(b["Lagna"])
    f["८ वर के कारकांश से सप्तम = वधू का लग्न"] = (KKb + 6) % 12 == sign(g["Lagna"])
    f["९ वर के दारकारक से १/७/त्रिकोण में वधू का लग्न"] = good(sign(g["Lagna"]), sign(b[dkb]))
    f["१० वधू के दारकारक से १/७/त्रिकोण में वर का लग्न"] = good(sign(b["Lagna"]), sign(g[dkg]))
    f["११ वर का दारकारक (नवांश) = वधू का नवांश लग्न/चंद्र"] = nav(b[dkb]) in (nav(g["Lagna"]), nav(g["Moon"]))
    f["१२ वधू का दारकारक (नवांश) = वर का नवांश लग्न/चंद्र"] = nav(g[dkg]) in (nav(b["Lagna"]), nav(b["Moon"]))
    return f

if __name__ == "__main__":
    me = checks(DINESH, P); my = sum(me.values())
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(909); N = 200_000
    single = collections.Counter(); tot = collections.Counter(); trio = core = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        g = chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place())
        f = checks(DINESH, g)
        for n, v in f.items(): single[n] += v
        tot[sum(f.values())] += 1
        k = list(f.values())
        trio += k[4] and k[5] and k[6]
        core += k[0] and k[1] and k[3] and k[4] and k[5]
    print(f"पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:50s} {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in tot.items())/N:.2f}")
    cum = 0
    for c in sorted(tot, reverse=True):
        cum += tot[c]; print(f"  {c:2d}: इतने या ज़्यादा {100*cum/N:7.3f}%")
    print(f"५+६+७ (कारकांश, दारकारक नवांश, कारकांश-सप्तम = वर लग्न): {trio} ({100*trio/N:.3f}%)")
    print(f"१+२+४+५+६ (आत्मकारक-दारकारक का मूल मेल): {core} ({100*core/N:.3f}%)")
''',
    'karak_sim': r'''"""
चर कारक (7 कारक) का रैंडम जोड़ों में मिलान।
"""
import random, collections
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]

def karakas(c):  # AK, AmK, BK, MK, PK, GK, DK
    return sorted(SEVEN, key=lambda p: -(c[p] % 30))

random.seed(5)
N = 100_000
same = collections.Counter(); inv3 = 0; same_kk = 0; ak_trine = 0; dk_trine = 0; all4 = 0
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
    kb, kg = karakas(b), karakas(g)
    s = sum(x == y for x, y in zip(kb, kg)); same[s] += 1
    # बाकी सभी कारक आपस में अदला-बदली (जैसे AK<->MK)
    pos_g = {p: i for i, p in enumerate(kg)}
    invol = all(kb[pos_g[kb[i]]] == kg[i] for i in range(7))
    inv3 += invol and s >= 3
    kk = nav(b[kb[0]]) == nav(g[kg[0]]); same_kk += kk
    at = (sign(b[kb[0]]) - sign(g[kg[0]])) % 12 in (0, 4, 8); ak_trine += at
    dt = (sign(b[kb[6]]) - sign(g[kg[6]])) % 12 in (0, 4, 8); dk_trine += dt
    dk_nav = nav(b[kb[6]]) == nav(g[kg[6]])
    all4 += kk and at and dt and dk_nav
print("एक ही ग्रह कितने कारक पदों पर:")
cum = 0
for k in sorted(same, reverse=True):
    cum += same[k]; print(f"  {k}: {100*same[k]/N:6.2f}%  इतने या ज़्यादा: {100*cum/N:6.2f}%")
print(f"3+ समान और बाकी सब अदला-बदली: {100*inv3/N:.3f}%")
print(f"कारकांश एक: {100*same_kk/N:.2f}%")
print(f"आत्मकारक त्रिकोण/एक राशि: {100*ak_trine/N:.2f}%   दारकारक त्रिकोण/एक राशि: {100*dk_trine/N:.2f}%")
print(f"कारकांश एक + दोनों त्रिकोण + दारकारक नवांश एक: {100*all4/N:.3f}%")
''',
    'kul_milan': r'''"""
सभी तय सूचियाँ एक ही रैंडम जोड़ों पर, ताकि संयुक्त स्थान निकले।
"""
import random
from kundli_sim import random_birth, place, sign, nak, ashtakoot
from durlabh_yog import chart
from sanyog_sim import DINESH, P
import var_vadhu_suchi as vv, rinanubandh as rn, niyam_suchi as ns, purva_janm as pj, double_lock as dl
from dashakoot_enum import dashakoot

def scores(b, rb, g, rg):
    s = {}
    s["vv"] = sum(vv.checks(b, g).values())
    s["rn"] = sum(bool(v) for v in rn.checks(b, rb, g, rg).values())
    s["ns"] = sum(ns.features(b, g).values())
    s["pj"] = sum(pj.checks(b, g).values())
    s["ak"] = sum(ashtakoot(b["Moon"], g["Moon"]).values())
    k = dashakoot(nak(b["Moon"]), sign(b["Moon"]), nak(g["Moon"]), sign(g["Moon"]))
    s["dk"] = sum(k.values()) if (k["रज्जु"] and k["वेध"]) else 0
    i = dl.info(b, g); s["lock"] = int(i["d1_house_rev"] and i["d9_house_same"])
    return s

me = scores(DINESH, {"Mercury"}, P, {"Jupiter"})
print("दिनेश-पी:", me)
groups = {
    "वर-वधू सूची (मेरी)": ["vv"],
    "ऋणानुबंध सूची (आपकी)": ["rn"],
    "दोहरा लॉक (आपका)": ["lock"],
    "मेरी + आपकी सूची": ["vv", "rn"],
    "मेरी + आपकी सूची + दोहरा लॉक": ["vv", "rn", "lock"],
    "सभी कसौटियाँ एक साथ": ["vv", "rn", "lock", "ns", "pj", "ak", "dk"],
}
random.seed(31); N = 150_000
cnt = dict.fromkeys(groups, 0)
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    (b, rb), (g, rg) = chart(jb, *place()), chart(jb + gap * 365.25, *place())
    s = scores(b, rb, g, rg)
    for n, ks in groups.items():
        cnt[n] += all(s[k] >= me[k] for k in ks)
for n, v in cnt.items():
    print(f"{n:32s} {100*v/N:7.3f}%  " + (f"(~1 in {N/v:,.0f})" if v else "(0)"))
''',
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
    'niyam_suchi': r'''"""
तय नियम से बनी सूची: केवल 1-1 और 1-7 संबंध।
क. एक ही बिंदु (राशि कुंडली): लग्न, सूर्य, चंद्र, मंगल, बुध, गुरु, शुक्र, शनि  -> 8
ख. अलग-अलग बिंदुओं का आपसी (दोनों दिशाओं में): लग्न, सूर्य, चंद्र, मंगल, शुक्र के सभी जोड़े -> 10
ग. एक ही बिंदु (नवांश): लग्न, चंद्र, मंगल, गुरु, शुक्र -> 5
कुल 23
"""
import random, collections, itertools
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import DINESH, P, nav

NAME = {"Lagna": "लग्न", "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
        "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि"}
A = ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
B = list(itertools.combinations(["Lagna", "Sun", "Moon", "Mars", "Venus"], 2))
C = ["Lagna", "Moon", "Mars", "Jupiter", "Venus"]

def ok(x, y): return (x - y) % 12 in (0, 6)

def features(b, g):
    f = collections.OrderedDict()
    for p in A:
        f[f"क. {NAME[p]}-{NAME[p]}"] = ok(sign(b[p]), sign(g[p]))
    for x, y in B:
        f[f"ख. {NAME[x]}-{NAME[y]}"] = ok(sign(b[x]), sign(g[y])) or ok(sign(b[y]), sign(g[x]))
    for p in C:
        f[f"ग. नवांश {NAME[p]}-{NAME[p]}"] = ok(nav(b[p]), nav(g[p]))
    return f

if __name__ == "__main__":
    me = features(DINESH, P); my = sum(me.values())
    print(f"इस जोड़े में {my}/{len(me)}")
    random.seed(23); N = 200_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = features(b, g)
        for k, v in f.items(): single[k] += v
        total[sum(f.values())] += 1
    for k, v in me.items():
        print(f"  {'✓' if v else '✗'} {k:25s} रैंडम में {100*single[k]/N:5.1f}%")
    mean = sum(c * n for c, n in total.items()) / N
    print(f"औसत संयोग: {mean:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]
        print(f"  {c:2d}: {100*total[c]/N:6.3f}%  इतने या ज़्यादा: {100*cum/N:6.3f}%")
''',
    'purva_janm': r'''"""
पूर्वजन्म संबंध के पारंपरिक/लोकप्रिय संकेत: तय सूची, दोनों दिशाएँ एक ही जाँच में।
"""
import random, collections
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from var_vadhu_suchi import karakas

def same(a, b): return sign(a) == sign(b)
def hs(c_planet_long, c_other): return (sign(c_planet_long) - sign(c_other["Lagna"])) % 12 + 1

def either(fn, b, g): return fn(b, g) or fn(g, b)

def checks(b, g):
    f = collections.OrderedDict()
    for node, nn in (("Ketu", "केतु"), ("Rahu", "राहु"), ("Saturn", "शनि")):
        for tgt, tn in (("Moon", "चंद्र"), ("Venus", "शुक्र"), ("Lagna", "लग्न"), ("Sun", "सूर्य")):
            f[f"एक का {nn} दूसरे के {tn} की राशि में"] = either(lambda x, y: same(x[node], y[tgt]), b, g)
    f["राहु-केतु अक्ष एक ही या उलटा"] = (sign(b["Rahu"]) - sign(g["Rahu"])) % 12 in (0, 6)
    f["एक का चंद्र दूसरे के बारहवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) == 12, b, g)
    f["एक का शुक्र दूसरे के बारहवें भाव में"] = either(lambda x, y: hs(x["Venus"], y) == 12, b, g)
    f["एक का चंद्र दूसरे के आठवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) == 8, b, g)
    f["एक का चंद्र दूसरे के पाँचवें/नौवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) in (5, 9), b, g)
    f["एक का आत्मकारक ग्रह दूसरे का दारकारक"] = either(lambda x, y: karakas(x)[0] == karakas(y)[6], b, g)
    f["एक का दारकारक दूसरे के लग्न/चंद्र की राशि में"] = either(
        lambda x, y: sign(x[karakas(x)[6]]) in (sign(y["Lagna"]), sign(y["Moon"])), b, g)
    f["नवांश: एक का केतु दूसरे के नवांश लग्न/चंद्र पर"] = either(
        lambda x, y: nav(x["Ketu"]) in (nav(y["Lagna"]), nav(y["Moon"])), b, g)
    return f

if __name__ == "__main__":
    me = checks(DINESH, P); my = sum(me.values())
    random.seed(77); N = 200_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = checks(b, g)
        for n, v in f.items(): single[n] += v
        total[sum(f.values())] += 1
    print(f"दिनेश-पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:48s} रैंडम में {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in total.items())/N:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]; print(f"  {c:2d}: {100*total[c]/N:6.3f}%   इतने या ज़्यादा: {100*cum/N:6.3f}%")
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
    # नियम: "सटीक अंशों में हो या त्रिकोण संबंध बनाए"। त्रिकोण (राशि से) ऊपर नियम ३ में है;
    # यहाँ केवल सटीक अंश वाली युति।
    f["३क भृगु बिंदु: इनमें से कोई युति में, १° के भीतर"] = E(lambda x, y: any(dist(fn(y), bb(x)) <= 1 for fn in tg.values()), b, g)
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
        lambda x, y: bool({S(x["Lagna"]), S(x["Moon"]), S(x["Venus"]), S(saptamesh(x))} & {nav(y["Lagna"]), nav(y["Moon"])}), b, g)
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
    'sabhi_bindu': r'''"""
जगन्नाथ होरा की दोनों तालिकाओं के सभी बिंदुओं में से कितने जोड़े आपस में १° (और २० कला) के भीतर हैं,
और संयोग से कितने अपेक्षित हैं।

अपेक्षा का तरीका (ज्यामितीय): दिनेश के सारे ४५ बिंदुओं को एक साथ एक रैंडम कोण से घुमाया जाता है।
इससे दोनों बिंदु-समूहों का आपसी संरेखण रैंडम हो जाता है, पर घुमाई गई कुंडली ज्योतिषीय रूप से
संभव कुंडली नहीं है (जैसे योग स्फुट = सूर्य + चंद्र, असली कुंडली में २ गुना खिसकता)।
ज्योतिषीय रूप से सही तुलना, जिसमें वधू के स्फुट सूत्र से बनते हैं, bindu45_dinesh.py में है।
"""
import math, random
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
    # ज्यामितीय अपेक्षा: दिनेश के बिंदुओं को एक साथ रैंडम घुमाकर (ऊपर docstring देखें)
    random.seed(1)
    shifts = [random.uniform(0, 360) for _ in range(2000)]
    pct = lambda xs, p: xs[max(0, math.ceil(p * len(xs)) - 1)]   # nearest-rank परसेंटाइल
    for lim in (1, 1/3):
        cnt = sorted(sum(dist(P[a], D[b] + sh) <= lim for a in P for b in D) for sh in shifts)
        print(f"\nरैंडम घुमाव पर {lim*60:.0f} कला के भीतर जोड़े: औसत {sum(cnt)/len(cnt):.1f}, "
              f"5%-95%: {pct(cnt, 0.05)}-{pct(cnt, 0.95)}")
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
    'saptam_4graha': r'''"""
वधू का सप्तम भाव खाली (सूर्य से शनि और राहु-केतु, कोई ग्रह नहीं)
और वर के राहु-केतु छोड़कर 4 ग्रह उसी राशि में।
"""
import random
from kundli_sim import chart, random_birth, place, sign

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
ALL = SEVEN + ["Rahu", "Ketu"]

random.seed(47)
N = 500_000
c = dict(empty=0, cluster4_any=0, ex4=0, ge4=0, either_ge4=0, ex4_in7_noempty=0)
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
    g7 = (sign(g["Lagna"]) + 6) % 12
    b7 = (sign(b["Lagna"]) + 6) % 12
    g_empty = all(sign(g[p]) != g7 for p in ALL)
    b_empty = all(sign(b[p]) != b7 for p in ALL)
    nb = sum(sign(b[p]) == g7 for p in SEVEN)  # वर के ग्रह वधू के सप्तम में
    ng = sum(sign(g[p]) == b7 for p in SEVEN)  # वधू के ग्रह वर के सप्तम में
    counts = [sum(sign(b[p]) == s for p in SEVEN) for s in range(12)]
    c["empty"] += g_empty
    c["cluster4_any"] += max(counts) >= 4
    c["ex4_in7_noempty"] += nb == 4
    c["ex4"] += g_empty and nb == 4
    c["ge4"] += g_empty and nb >= 4
    c["either_ge4"] += (g_empty and nb >= 4) or (b_empty and ng >= 4)
for k, v in c.items():
    print(f"{k:18s} {v:7d}  {100*v/N:7.3f}%  " + (f"(~1 in {N/v:,.0f})" if v else ""))
''',
    'teen_milan_dinesh': r'''"""
दिनेश स्थिर, २ लाख रैंडम वधुएँ। तीन कसौटियाँ अलग-अलग और एक साथ:
  १. दशकूट (४४ अंक, रज्जु-वेध साफ़)
  २. जैमिनी (१२ जाँचें)
  ३. राहु-केतु: भाव चार्ट (D1) में विपरीत भाव, नवांश (D9) में एक ही भाव
     - सामान्य लॉक: D1 में राहु के भाव ठीक ६ भाव अलग, D9 में राहु एक ही भाव में
     - सख्त लॉक (पी जैसा): D1 में वधू का राहु २/८ और वर का उलटा, D9 में दोनों ४ या दोनों १०
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign
from sanyog_sim import nav, DINESH, P
from jaimini_dinesh import checks
from jaimini_dashakoot_paas import dk44

def h(x, lg): return (x - lg) % 12 + 1

def lock(b, g):
    hb, hg = h(sign(b["Rahu"]), sign(b["Lagna"])), h(sign(g["Rahu"]), sign(g["Lagna"]))
    hb9, hg9 = h(nav(b["Rahu"]), nav(b["Lagna"])), h(nav(g["Rahu"]), nav(g["Lagna"]))
    gen = (hb - hg) % 12 == 6 and hb9 == hg9
    strict = hg in (2, 8) and hb == 10 - hg and hb9 == hg9 and hb9 in (4, 10)
    return gen, strict

def crit(g):
    s, clean = dk44(g)
    j = sum(checks(DINESH, g).values())
    gen, strict = lock(DINESH, g)
    return {"दशकूट पास (२२+)": clean and s >= 22, "दशकूट ३७": clean and s >= 37,
            "जैमिनी ९+": j >= 9, "जैमिनी ७+": j >= 7,
            "राहु-केतु लॉक (सामान्य)": gen, "राहु-केतु लॉक (सख्त)": strict}

COMBOS = [
    ["दशकूट ३७", "जैमिनी ९+"],
    ["दशकूट ३७", "राहु-केतु लॉक (सामान्य)"],
    ["जैमिनी ९+", "राहु-केतु लॉक (सामान्य)"],
    ["दशकूट ३७", "जैमिनी ९+", "राहु-केतु लॉक (सामान्य)"],
    ["दशकूट ३७", "जैमिनी ९+", "राहु-केतु लॉक (सख्त)"],
    ["दशकूट पास (२२+)", "जैमिनी ७+", "राहु-केतु लॉक (सामान्य)"],
    ["दशकूट ३७", "जैमिनी ७+", "राहु-केतु लॉक (सामान्य)"],
]

if __name__ == "__main__":
    me = crit(P); print("पी:", me)
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(4949); N = 200_000
    one = collections.Counter(); both = collections.Counter()
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        c = crit(chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place()))
        for k, v in c.items(): one[k] += v
        for cb in COMBOS: both[" + ".join(cb)] += all(c[k] for k in cb)
    print(f"N = {N:,} वधुएँ\n")
    for k, v in one.items(): print(f"{k:28s} {v:7,}  {100*v/N:7.3f}%  ~1 in {N/v:,.0f}")
    print()
    for k, v in both.items(): print(f"{k:58s} {v:6,}  {100*v/N:8.4f}%  " + (f"~1 in {N/v:,.0f}" if v else "(0)"))
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



def _run(name):
    print(f"\n========== {name} ==========", flush=True)
    code = compile(_EMBEDDED[name], name + ".py", "exec")
    exec(code, {"__name__": "__main__", "__file__": name + ".py"})


if __name__ == "__main__":
    args = _sys.argv[1:]
    if not args:
        print("उपयोग: python kundli_all.py <नाम> [<नाम> ...]   या   python kundli_all.py all")
        print("उपलब्ध विश्लेषण:")
        for n in sorted(_EMBEDDED):
            print("   ", n)
        _sys.exit(0)
    names = sorted(_EMBEDDED) if args == ["all"] else args
    bad = [n for n in names if n not in _EMBEDDED]
    if bad:
        _sys.exit(f"ये नाम नहीं मिले: {', '.join(bad)}. सूची देखने के लिए बिना नाम के चलाएँ।")
    for n in names:
        _run(n)
