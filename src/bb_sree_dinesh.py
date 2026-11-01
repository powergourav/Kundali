"""
भृगु बिंदु और श्री लग्न मिलान: दिनेश स्थिर, वधू रैंडम (२ लाख)।
एक के चंद्र, लग्नेश, सप्तमेश को दूसरे के भृगु बिंदु और श्री लग्न से (दोनों दिशाएँ),
और बिंदु-से-बिंदु।
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign
from sanyog_sim import DINESH, P
from sabhi_bindu import dist

LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
NAK = 40 / 3

def bb(c): return (c["Rahu"] + ((c["Moon"] - c["Rahu"]) % 360) / 2) % 360
def sree(c): return (c["Lagna"] + ((c["Moon"] % NAK) / NAK) * 360) % 360
def pts(c):
    L = sign(c["Lagna"])
    return {"चंद्र": c["Moon"], "लग्नेश": c[LORD[L]], "सप्तमेश": c[LORD[(L + 6) % 12]]}
def good_sign(a, b): return (sign(a) - sign(b)) % 12 in (0, 4, 6, 8)
def close(a, b, orb): return dist(a, b) <= orb or dist(a, (b + 180) % 360) <= orb  # युति या समसप्तक

def score(b, g):
    tb = {"भृगु": bb(b), "श्री": sree(b)}; tg = {"भृगु": bb(g), "श्री": sree(g)}
    s = collections.Counter()
    for X, TY in ((pts(b), tg), (pts(g), tb)):
        for x in X.values():
            for t in TY.values():
                s["राशि संबंध"] += good_sign(x, t)
                s["१°"] += close(x, t, 1); s["२°"] += close(x, t, 2)
    for a in tb.values():
        for c in tg.values():
            s["राशि संबंध"] += good_sign(a, c)
            s["१°"] += close(a, c, 1); s["२°"] += close(a, c, 2)
    s["वधू सप्तमेश वर के भृगु पर १°"] = close(pts(g)["सप्तमेश"], tb["भृगु"], 1)
    return s

if __name__ == "__main__":
    print("जाँच: श्री लग्न दिनेश", divmod(sree(DINESH), 30), "पी", divmod(sree(P), 30))
    me = score(DINESH, P); print("पी:", dict(me))
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(5151); N = 200_000
    ge = collections.Counter(); tot = collections.Counter(); allthree = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        s = score(DINESH, chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place()))
        for k in ("राशि संबंध", "१°", "२°", "वधू सप्तमेश वर के भृगु पर १°"):
            tot[k] += s[k]; ge[k] += s[k] >= me[k]
        allthree += all(s[k] >= me[k] for k in ("राशि संबंध", "१°", "२°"))
    print(f"N = {N:,}")
    for k in tot: print(f"{k}: औसत {tot[k]/N:.2f}, पी जितने या ज़्यादा {100*ge[k]/N:.2f}%")
    print(f"राशि संबंध + १° + २° तीनों में पी जितना या बेहतर: {100*allthree/N:.2f}%")
