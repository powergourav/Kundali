"""
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
