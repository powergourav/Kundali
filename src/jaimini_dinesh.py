"""
जैमिनी गहरा मिलान: दिनेश स्थिर, वधू रैंडम (२ लाख)।
१२ जाँचें, दोनों दिशाओं में बराबर।
"""
import random, collections
import swisseph as swe
from kundli_sim import chart, place, sign, rel
from sanyog_sim import nav, DINESH, P
from rinanubandh import ak_link

SEVEN = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
CODE = {"Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa"}
def K(c): return sorted(SEVEN, key=lambda p: -(c[p] % 30))
def good(a, b): return (a - b) % 12 in (0, 4, 6, 8)   # १-१, १-७, त्रिकोण
def friends(p, q): return p == q or (rel(CODE[p], CODE[q]) == 2 and rel(CODE[q], CODE[p]) == 2)

def checks(b, g):
    kb, kg = K(b), K(g)
    akb, akg, dkb, dkg = kb[0], kg[0], kb[6], kg[6]
    KKb, KKg = nav(b[akb]), nav(g[akg])
    f = collections.OrderedDict()
    f["१ आत्मकारक एक ग्रह या परस्पर मित्र"] = friends(akb, akg)
    f["२ आत्मकारक राशियाँ १-१/१-७/त्रिकोण"] = good(sign(b[akb]), sign(g[akg]))
    f["३ आत्मकारकों में युति या जैमिनी राशि दृष्टि"] = ak_link(b[akb], g[akg])
    f["४ दारकारक राशियाँ १-१/१-७/त्रिकोण"] = good(sign(b[dkb]), sign(g[dkg]))
    f["५ कारकांश एक ही"] = KKb == KKg
    f["६ दारकारक का नवांश एक ही"] = nav(b[dkb]) == nav(g[dkg])
    f["७ वधू के कारकांश से सप्तम = वर का लग्न"] = (KKg + 6) % 12 == sign(b["Lagna"])
    f["८ वर के कारकांश से सप्तम = वधू का लग्न"] = (KKb + 6) % 12 == sign(g["Lagna"])
    f["९ वर के दारकारक से १/७/त्रिकोण में वधू का लग्न"] = good(sign(g["Lagna"]), sign(b[dkb]))
    f["१० वधू के दारकारक से १/७/त्रिकोण में वर का लग्न"] = good(sign(b["Lagna"]), sign(g[dkg]))
    f["११ वर का दारकारक (नवांश) = वधू का नवांश लग्न/चंद्र"] = nav(b[dkb]) in (nav(g["Lagna"]), nav(g["Moon"]))
    f["१२ वधू का दारकारक (नवांश) = वर का नवांश लग्न/चंद्र"] = nav(g[dkg]) in (nav(b["Lagna"]), nav(b["Moon"]))
    return f

if __name__ == "__main__":
    me = checks(DINESH, P); my = sum(me.values())
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(909); N = 200_000
    single = collections.Counter(); tot = collections.Counter(); trio = core = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        g = chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place())
        f = checks(DINESH, g)
        for n, v in f.items(): single[n] += v
        tot[sum(f.values())] += 1
        k = list(f.values())
        trio += k[4] and k[5] and k[6]
        core += k[0] and k[1] and k[3] and k[4] and k[5]
    print(f"पी: {my}/{len(me)}")
    for n, v in me.items(): print(f"  {'✓' if v else '✗'} {n:50s} {100*single[n]/N:5.1f}%")
    print(f"औसत: {sum(c*n for c,n in tot.items())/N:.2f}")
    cum = 0
    for c in sorted(tot, reverse=True):
        cum += tot[c]; print(f"  {c:2d}: इतने या ज़्यादा {100*cum/N:7.3f}%")
    print(f"५+६+७ (कारकांश, दारकारक नवांश, कारकांश-सप्तम = वर लग्न): {trio} ({100*trio/N:.3f}%)")
    print(f"१+२+४+५+६ (आत्मकारक-दारकारक का मूल मेल): {core} ({100*core/N:.3f}%)")
