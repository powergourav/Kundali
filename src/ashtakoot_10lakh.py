"""
अष्टकूट: १० लाख रैंडम वर-वधू जोड़े (केवल चंद्र पर निर्भर)।
"""
import random, collections
import swisseph as swe
from kundli_sim import ashtakoot, random_birth

swe.set_sid_mode(swe.SIDM_LAHIRI)
moon = lambda jd: swe.calc_ut(jd, swe.MOON, swe.FLG_SIDEREAL)[0][0]
DINESH_M, P_M = 150 + 17 + 42.7 / 60, 270 + 8.0 / 60
me = ashtakoot(DINESH_M, P_M); my = sum(me.values())
print("दिनेश-पी:", me, "कुल", my)

random.seed(2000); N = 1_000_000
dist = collections.Counter(); kut = collections.Counter(); c = collections.Counter()
for _ in range(N):
    jb = random_birth(1980, 2001)
    gap = min(12, max(-3, random.gauss(3.5, 2.5)))
    k = ashtakoot(moon(jb), moon(jb + gap * 365.25)); s = sum(k.values())
    dist[int(s)] += 1
    for n, v in k.items(): kut[n] += v == me[n] or v >= me[n]
    c["≥18"] += s >= 18; c["≥my"] += s >= my; c["≥28"] += s >= 28; c["≥32"] += s >= 32
    c["≥my नाड़ी ठीक"] += s >= my and k["nadi"] > 0
    c["≥my नाड़ी-भकूट दोनों ठीक"] += s >= my and k["nadi"] > 0 and k["bhakoot"] > 0
    c["नाड़ी दोष"] += k["nadi"] == 0; c["भकूट दोष"] += k["bhakoot"] == 0
print(f"N = {N:,}")
cum = 0
for s in sorted(dist, reverse=True):
    cum += dist[s]; print(f"  {s:2d}: {100*dist[s]/N:5.2f}%   इतना या ज़्यादा: {100*cum/N:6.2f}%")
for n, v in c.items(): print(f"{n}: {100*v/N:.2f}%  (~1 in {N/v:.1f})")
print("हर कूट में दिनेश-पी जितना या ज़्यादा:")
for n, v in kut.items(): print(f"  {n}: {100*v/N:.1f}%")
