"""
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
