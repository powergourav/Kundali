"""
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
