"""
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
