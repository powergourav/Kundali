"""
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
