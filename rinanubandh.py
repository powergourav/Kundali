"""
ऋणानुबंध जाँच: उपयोगकर्ता की दी हुई सूची के हर नियम को गणना-योग्य रूप में।
दोनों दिशाओं वाली जाँच = किसी भी एक दिशा में सच हो तो पास।
षष्ट्यंश (D60) छोड़ा गया, क्योंकि उसके लिए सटीक जन्म-समय चाहिए।
"""
import random, collections
from kundli_sim import random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from durlabh_yog import chart
from var_vadhu_suchi import karakas

LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def S(x): return sign(x)
def rel(a, b): return (S(a) - S(b)) % 12
def trine(a, b): return rel(a, b) in (0, 4, 8)
def trine7(a, b): return rel(a, b) in (0, 4, 8, 6)
def house(c, L): return (S(L) - S(c["Lagna"])) % 12 + 1
def dist(a, b): return abs((a - b + 180) % 360 - 180)
def bb(c): return (c["Rahu"] + ((c["Moon"] - c["Rahu"]) % 360) / 2) % 360
def lagnesh(c): return c[LORD[S(c["Lagna"])]]
def saptamesh_name(c): return LORD[(S(c["Lagna"]) + 6) % 12]
def saptamesh(c): return c[saptamesh_name(c)]

def rashi_drishti(a, b):  # जैमिनी राशि दृष्टि (राशि अंक 0..11)
    ma = a % 3; mb = b % 3  # 0 चर, 1 स्थिर, 2 द्विस्वभाव
    if ma == 2: return mb == 2 and a != b
    if ma == 0: return mb == 1 and (b - a) % 12 != 1
    return mb == 0 and (a - b) % 12 != 1

def ak_link(x, y):
    a, b = S(x), S(y)
    return a == b or rashi_drishti(a, b) or rashi_drishti(b, a)

def E(fn, b, g): return fn(b, g) or fn(g, b)

def checks(b, rb, g, rg):
    f = collections.OrderedDict()
    for t, n in (("Lagna", "लग्न"), ("Moon", "चंद्र"), ("Sun", "सूर्य"), ("Venus", "शुक्र")):
        f[f"१ केतु: एक का केतु दूसरे के {n} की राशि में"] = E(lambda x, y: S(x["Ketu"]) == S(y[t]), b, g)
    for t, n in (("Moon", "चंद्र"), ("Venus", "शुक्र"), ("Mars", "मंगल"), ("Lagna", "लग्न")):
        f[f"२ राहु: एक का राहु दूसरे के {n} की राशि में"] = E(lambda x, y: S(x["Rahu"]) == S(y[t]), b, g)
    tg = {"लग्नेश": lagnesh, "सप्तमेश": saptamesh, "शुक्र": lambda c: c["Venus"], "गुरु": lambda c: c["Jupiter"]}
    for n, fn in tg.items():
        f[f"३ भृगु बिंदु: दूसरे का {n} एक राशि या त्रिकोण में"] = E(lambda x, y: trine(fn(y), bb(x)), b, g)
    f["३क भृगु बिंदु: इनमें से कोई १° के भीतर"] = E(lambda x, y: any(dist(fn(y), bb(x)) <= 1 for fn in tg.values()), b, g)
    for p, pn in (("Venus", "शुक्र"), ("Mars", "मंगल")):
        for q, qn in (("Saturn", "शनि"), ("Ketu", "केतु")):
            f[f"४ नाड़ी: एक का {pn}, दूसरे के {qn} से त्रिकोण/सप्तम"] = E(lambda x, y: trine7(x[p], y[q]), b, g)
    f["५ वर: सप्तमेश या शुक्र ५/९ में"] = house(b, saptamesh(b)) in (5, 9) or house(b, b["Venus"]) in (5, 9)
    f["५ वधू: सप्तमेश या शुक्र ५/९ में"] = house(g, saptamesh(g)) in (5, 9) or house(g, g["Venus"]) in (5, 9)
    f["५क एक का सप्तमेश/शुक्र दूसरे के ५/९ में"] = E(lambda x, y: house(y, saptamesh(x)) in (5, 9) or house(y, x["Venus"]) in (5, 9), b, g)
    f["६ वर: सप्तमेश या शुक्र ८/१२ में"] = house(b, saptamesh(b)) in (8, 12) or house(b, b["Venus"]) in (8, 12)
    f["६ वधू: सप्तमेश या शुक्र ८/१२ में"] = house(g, saptamesh(g)) in (8, 12) or house(g, g["Venus"]) in (8, 12)
    f["६क एक का सप्तमेश/शुक्र दूसरे के ८/१२ में"] = E(lambda x, y: house(y, saptamesh(x)) in (8, 12) or house(y, x["Venus"]) in (8, 12), b, g)
    f["७ वर: शुक्र, मंगल या सप्तमेश वक्री"] = bool(rb & {"Venus", "Mars", saptamesh_name(b)})
    f["७ वधू: शुक्र, मंगल या सप्तमेश वक्री"] = bool(rg & {"Venus", "Mars", saptamesh_name(g)})
    f["८ जैमिनी: आत्मकारक-आत्मकारक युति या राशि दृष्टि"] = ak_link(b[karakas(b)[0]], g[karakas(g)[0]])
    f["८ जैमिनी: एक का आत्मकारक, दूसरे के दारकारक से युति या राशि दृष्टि"] = E(
        lambda x, y: ak_link(x[karakas(x)[0]], y[karakas(y)[6]]), b, g)
    f["९ नवांश: एक के लग्न/चंद्र/शुक्र/सप्तमेश की राशि = दूसरे का नवांश लग्न या चंद्र"] = E(
        lambda x, y: {S(x["Lagna"]), S(x["Moon"]), S(x["Venus"]), S(saptamesh(x))} & {nav(y["Lagna"]), nav(y["Moon"])}, b, g)
    return f

if __name__ == "__main__":
    print("भृगु बिंदु: दिनेश", divmod(bb(DINESH), 30), " पी", divmod(bb(P), 30))
    me = checks(DINESH, {"Mercury"}, P, {"Jupiter"}); my = sum(bool(v) for v in me.values())
    random.seed(2026); N = 150_000
    single = collections.Counter(); total = collections.Counter()
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        (b, rb), (g, rg) = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        f = checks(b, rb, g, rg)
        for n, v in f.items(): single[n] += bool(v)
        total[sum(bool(v) for v in f.values())] += 1
    print(f"दिनेश-पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:70s} {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in total.items())/N:.2f}")
    cum = 0
    for c in sorted(total, reverse=True):
        cum += total[c]; print(f"  {c:2d}: {100*total[c]/N:6.3f}%   इतने या ज़्यादा: {100*cum/N:6.3f}%")
