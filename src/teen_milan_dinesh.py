"""
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
