"""
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
    cnt["अष्टकूट (२४+, नाड़ी ठीक)"] += ak
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
