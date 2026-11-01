"""
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
