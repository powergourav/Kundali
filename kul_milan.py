"""
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
