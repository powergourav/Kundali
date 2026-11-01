"""
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
            if a["nadi"] > 0 and sum(a.values()) >= 24: clean_ak += 1
print(f"N = {N:,}")
cum = 0
for s in sorted(dist, reverse=True):
    cum += dist[s]; print(f"  {s:4.1f}/10 : {100*dist[s]/N:6.2f}%   इतना या ज़्यादा: {100*cum/N:6.2f}%")
for n, v in [("७.५ या ज़्यादा", ge), ("+ रज्जु-वेध साफ़", clean), ("+ अष्टकूट >=२४ और नाड़ी दोष नहीं", clean_ak)]:
    print(f"{n}: {v:,} ({100*v/N:.2f}%, ~1 in {N/v:.1f})")
