"""
पूर्वजन्म संबंध के पारंपरिक/लोकप्रिय संकेत: तय सूची, दोनों दिशाएँ एक ही जाँच में।
"""
import random, collections
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from var_vadhu_suchi import karakas

def same(a, b): return sign(a) == sign(b)
def hs(c_planet_long, c_other): return (sign(c_planet_long) - sign(c_other["Lagna"])) % 12 + 1

def either(fn, b, g): return fn(b, g) or fn(g, b)

def checks(b, g):
    f = collections.OrderedDict()
    for node, nn in (("Ketu", "केतु"), ("Rahu", "राहु"), ("Saturn", "शनि")):
        for tgt, tn in (("Moon", "चंद्र"), ("Venus", "शुक्र"), ("Lagna", "लग्न"), ("Sun", "सूर्य")):
            f[f"एक का {nn} दूसरे के {tn} की राशि में"] = either(lambda x, y: same(x[node], y[tgt]), b, g)
    f["राहु-केतु अक्ष एक ही या उलटा"] = (sign(b["Rahu"]) - sign(g["Rahu"])) % 12 in (0, 6)
    f["एक का चंद्र दूसरे के बारहवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) == 12, b, g)
    f["एक का शुक्र दूसरे के बारहवें भाव में"] = either(lambda x, y: hs(x["Venus"], y) == 12, b, g)
    f["एक का चंद्र दूसरे के आठवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) == 8, b, g)
    f["एक का चंद्र दूसरे के पाँचवें/नौवें भाव में"] = either(lambda x, y: hs(x["Moon"], y) in (5, 9), b, g)
    f["एक का आत्मकारक ग्रह दूसरे का दारकारक"] = either(lambda x, y: karakas(x)[0] == karakas(y)[6], b, g)
    f["एक का दारकारक दूसरे के लग्न/चंद्र की राशि में"] = either(
        lambda x, y: sign(x[karakas(x)[6]]) in (sign(y["Lagna"]), sign(y["Moon"])), b, g)
    f["नवांश: एक का केतु दूसरे के नवांश लग्न/चंद्र पर"] = either(
        lambda x, y: nav(x["Ketu"]) in (nav(y["Lagna"]), nav(y["Moon"])), b, g)
    return f

if __name__ == "__main__":
    me = checks(DINESH, P); my = sum(me.values())
    random.seed(77); N = 200_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = checks(b, g)
        for n, v in f.items(): single[n] += v
        total[sum(f.values())] += 1
    print(f"दिनेश-पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:48s} रैंडम में {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in total.items())/N:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]; print(f"  {c:2d}: {100*total[c]/N:6.3f}%   इतने या ज़्यादा: {100*cum/N:6.3f}%")
