"""
तय नियम से बनी सूची: केवल 1-1 और 1-7 संबंध।
क. एक ही बिंदु (राशि कुंडली): लग्न, सूर्य, चंद्र, मंगल, बुध, गुरु, शुक्र, शनि  -> 8
ख. अलग-अलग बिंदुओं का आपसी (दोनों दिशाओं में): लग्न, सूर्य, चंद्र, मंगल, शुक्र के सभी जोड़े -> 10
ग. एक ही बिंदु (नवांश): लग्न, चंद्र, मंगल, गुरु, शुक्र -> 5
कुल 23
"""
import random, collections, itertools
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import DINESH, P, nav

NAME = {"Lagna": "लग्न", "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
        "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि"}
A = ["Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
B = list(itertools.combinations(["Lagna", "Sun", "Moon", "Mars", "Venus"], 2))
C = ["Lagna", "Moon", "Mars", "Jupiter", "Venus"]

def ok(x, y): return (x - y) % 12 in (0, 6)

def features(b, g):
    f = collections.OrderedDict()
    for p in A:
        f[f"क. {NAME[p]}-{NAME[p]}"] = ok(sign(b[p]), sign(g[p]))
    for x, y in B:
        f[f"ख. {NAME[x]}-{NAME[y]}"] = ok(sign(b[x]), sign(g[y])) or ok(sign(b[y]), sign(g[x]))
    for p in C:
        f[f"ग. नवांश {NAME[p]}-{NAME[p]}"] = ok(nav(b[p]), nav(g[p]))
    return f

if __name__ == "__main__":
    me = features(DINESH, P); my = sum(me.values())
    print(f"इस जोड़े में {my}/{len(me)}")
    random.seed(23); N = 200_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = features(b, g)
        for k, v in f.items(): single[k] += v
        total[sum(f.values())] += 1
    for k, v in me.items():
        print(f"  {'✓' if v else '✗'} {k:25s} रैंडम में {100*single[k]/N:5.1f}%")
    mean = sum(c * n for c, n in total.items()) / N
    print(f"औसत संयोग: {mean:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]
        print(f"  {c:2d}: {100*total[c]/N:6.3f}%  इतने या ज़्यादा: {100*cum/N:6.3f}%")
