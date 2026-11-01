"""
एक अकेली कुंडली में "दुर्लभ" (5% या कम) योग कितने मिलते हैं।
पहले सभी उम्मीदवार योग गिने जाते हैं, फिर केवल वही रखे जाते हैं जो
रैंडम कुंडलियों में 5% या कम मिलते हैं।
"""
import random, collections, itertools
import swisseph as swe
from kundli_sim import random_birth, place, sign, nak
from sanyog_sim import nav

swe.set_sid_mode(swe.SIDM_LAHIRI)
FLG = swe.FLG_SIDEREAL | swe.FLG_SPEED
PL = {"Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS, "Mercury": swe.MERCURY,
      "Jupiter": swe.JUPITER, "Venus": swe.VENUS, "Saturn": swe.SATURN, "Rahu": swe.MEAN_NODE}
NM = {"Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध", "Jupiter": "गुरु",
      "Venus": "शुक्र", "Saturn": "शनि"}
SEVEN = list(NM)
EXALT = {"Sun": 10, "Moon": 33, "Mars": 298, "Mercury": 165, "Jupiter": 95, "Venus": 357, "Saturn": 200}
OWN = {"Sun": {4}, "Moon": {3}, "Mars": {0, 7}, "Mercury": {2, 5}, "Jupiter": {8, 11},
       "Venus": {1, 6}, "Saturn": {9, 10}}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]
MAHA = {"Mars": "रुचक", "Mercury": "भद्र", "Jupiter": "हंस", "Venus": "मालव्य", "Saturn": "शश"}

def chart(jd, lat, lon):
    c, r = {}, set()
    for n, p in PL.items():
        x = swe.calc_ut(jd, p, FLG)[0]
        c[n] = x[0]
        if n in ("Mars", "Mercury", "Jupiter", "Venus", "Saturn") and x[3] < 0: r.add(n)
    c["Ketu"] = (c["Rahu"] + 180) % 360
    c["Lagna"] = swe.houses_ex(jd, lat, lon, b"W", swe.FLG_SIDEREAL)[1][0]
    return c, r

def dist(a, b): return abs((a - b + 180) % 360 - 180)

def features(c, retro):
    f = {}
    L = sign(c["Lagna"]); H = lambda p: (sign(c[p]) - L) % 12 + 1
    for p in SEVEN:
        f[f"{NM[p]} परम उच्च (±३°)"] = dist(c[p], EXALT[p]) <= 3
        f[f"{NM[p]} परम नीच (±३°)"] = dist(c[p], EXALT[p] + 180) <= 3
        f[f"{NM[p]} लग्न-अंश से १° के भीतर"] = dist(c[p], c["Lagna"]) <= 1
        f[f"{NM[p]} वर्गोत्तम और उच्च"] = sign(c[p]) == nav(c[p]) and sign(c[p]) == EXALT[p] // 30
        f[f"{NM[p]} उच्च होकर लग्न में"] = sign(c[p]) == EXALT[p] // 30 and H(p) == 1
    for p, nm in MAHA.items():
        f[f"{nm} महापुरुष योग"] = (sign(c[p]) in OWN[p] or sign(c[p]) == EXALT[p] // 30) and H(p) in (1, 4, 7, 10)
    cnt = collections.Counter(sign(c[p]) for p in SEVEN)
    f["एक राशि में ४+ ग्रह"] = max(cnt.values()) >= 4
    f["एक राशि में ५+ ग्रह"] = max(cnt.values()) >= 5
    rh = c["Rahu"]
    side = [((c[p] - rh) % 360) < 180 for p in SEVEN]
    f["कालसर्प (सातों ग्रह राहु-केतु के एक ओर)"] = all(side) or not any(side)
    el = (c["Moon"] - c["Sun"]) % 360
    f["अमावस्या के पास जन्म (±६°)"] = min(el, 360 - el) <= 6
    f["पूर्णिमा के पास जन्म (±६°)"] = dist(el, 180) <= 6
    gand = lambda x: (x % 120) >= 116.667 or (x % 120) <= 3.333
    f["चंद्र गंडांत"] = gand(c["Moon"])
    f["लग्न गंडांत"] = gand(c["Lagna"])
    f["लग्न और चंद्र एक नक्षत्र"] = nak(c["Lagna"]) == nak(c["Moon"])
    f["लग्न और चंद्र दोनों वर्गोत्तम"] = sign(c["Lagna"]) == nav(c["Lagna"]) and sign(c["Moon"]) == nav(c["Moon"])
    f["४ या ज़्यादा ग्रह वक्री"] = len(retro) >= 4
    f["ग्रह युद्ध (मंगल-शनि में किन्हीं दो की दूरी <१°)"] = any(
        dist(c[a], c[b]) < 1 for a, b in itertools.combinations(["Mars", "Mercury", "Jupiter", "Venus", "Saturn"], 2))
    f["लग्नेश-सप्तमेश परिवर्तन"] = (sign(c[LORD[L]]) == (L + 6) % 12 and sign(c[LORD[(L + 6) % 12]]) == L)
    f["४+ ग्रह उच्च या स्वराशि में"] = sum(sign(c[p]) in OWN[p] or sign(c[p]) == EXALT[p] // 30 for p in SEVEN) >= 4
    f["सातों ग्रह केंद्र-त्रिकोण में"] = all(H(p) in (1, 4, 5, 7, 9, 10) for p in SEVEN)
    f["गुरु-चंद्र १° के भीतर"] = dist(c["Jupiter"], c["Moon"]) <= 1
    f["आत्मकारक २९° से ऊपर"] = max(c[p] % 30 for p in SEVEN) >= 29
    return f

def deg(s, d, m): return s * 30 + d + m / 60

if __name__ == "__main__":
    random.seed(3); N = 60_000
    rows = []
    for _ in range(N):
        c, r = chart(random_birth(1960, 2011), *place())
        rows.append(features(c, r))
    names = list(rows[0])
    p = {n: sum(r[n] for r in rows) / N for n in names}
    rare = [n for n in names if 0 < p[n] <= 0.05]
    counts = collections.Counter(sum(r[n] for n in rare) for r in rows)
    print(f"कुल उम्मीदवार योग: {len(names)}, जिनमें दुर्लभ (≤५%): {len(rare)}")
    for n in sorted(rare, key=lambda n: p[n]): print(f"  {100*p[n]:5.2f}%  {n}")
    mean = sum(k * v for k, v in counts.items()) / N
    print(f"\nएक कुंडली में औसत दुर्लभ योग: {mean:.2f}")
    cum = 0
    for k in sorted(counts, reverse=True):
        cum += counts[k]; print(f"  {k}: {100*counts[k]/N:6.2f}%  इतने या ज़्यादा: {100*cum/N:6.2f}%")

    D = {"Lagna": deg(8, 8, 34.6), "Sun": deg(5, 13, 24.8), "Moon": deg(5, 17, 42.7), "Mars": deg(5, 13, 15.0),
         "Mercury": deg(5, 3, 12.4), "Jupiter": deg(2, 15, 51.3), "Venus": deg(6, 26, 50.0),
         "Saturn": deg(8, 13, 53.8), "Rahu": deg(9, 29, 40.1), "Ketu": deg(3, 29, 40.1)}
    P = {"Lagna": deg(11, 11, 11.2), "Sun": deg(1, 3, 41.8), "Moon": deg(9, 0, 8.0), "Mars": deg(4, 3, 15.3),
         "Mercury": deg(1, 23, 23.3), "Jupiter": deg(7, 18, 25.5), "Venus": deg(0, 8, 33.7),
         "Saturn": deg(10, 29, 5.6), "Rahu": deg(6, 10, 41.1), "Ketu": deg(0, 10, 41.1)}
    for nm, c, r in (("दिनेश", D, {"Mercury"}), ("पी", P, {"Jupiter"})):
        f = features(c, r)
        hit = [n for n in rare if f[n]]
        print(f"\n{nm}: {len(hit)} दुर्लभ योग -> {hit}")
