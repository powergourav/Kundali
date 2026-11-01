"""
४५ बिंदु मिलान: दिनेश के सभी ४५ बिंदु (जगन्नाथ होरा तालिका) स्थिर,
वधू के वे २६ बिंदु जिनका सूत्र केवल ग्रह-अंशों और लग्न से बनता है।
(गुलिक, मांदि, होरा/घटी/भाव/वर्णद/श्री/प्राणपद लग्न, काल-मृत्यु आदि उपग्रह
 सूर्योदय के समय पर टिके हैं, वे रैंडम वधुओं में नहीं गिने गए।)
"""
import random
import swisseph as swe
from kundli_sim import chart, place, sign
from sabhi_bindu import parse, P_TXT, D_TXT, dist

KALA = {"Sun": 30, "Moon": 16, "Mars": 6, "Mercury": 8, "Jupiter": 10, "Venus": 12, "Saturn": 1}
LORD = ["Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter"]

def derived(c):
    p = {k: c[k] for k in ("Lagna", "Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu")}
    su, mo = c["Sun"], c["Moon"]
    p["Dhooma"] = (su + 133 + 1 / 3) % 360
    p["Vyatipata"] = (360 - p["Dhooma"]) % 360
    p["Parivesha"] = (p["Vyatipata"] + 180) % 360
    p["IndraChapa"] = (360 - p["Parivesha"]) % 360
    p["Upaketu"] = (p["IndraChapa"] + 16 + 2 / 3) % 360
    p["BhriguB"] = (c["Rahu"] + ((mo - c["Rahu"]) % 360) / 2) % 360
    p["YogaSphSM"] = (su + mo) % 360
    p["YogaSph"] = (su + mo + 93 + 1 / 3) % 360
    p["Avayoga"] = (p["YogaSph"] + 186 + 2 / 3) % 360
    p["TithiSph"] = (mo - su) % 360
    p["RahuTithi"] = (c["Rahu"] - su) % 360
    p["Beeja"] = (su + c["Venus"] + c["Jupiter"]) % 360
    p["Kshetra"] = (mo + c["Mars"] + c["Jupiter"]) % 360
    p["Kunda"] = (c["Lagna"] * 81) % 360
    L, M = sign(c["Lagna"]), sign(mo)
    r = (KALA[LORD[(L + 8) % 12]] + KALA[LORD[(M + 8) % 12]]) % 12 or 12
    p["InduL"] = ((M + r - 1) % 12) * 30 + mo % 30
    return p

def hits(dpts, bpts, orb):
    return sum(dist(a, b) <= orb for a in dpts.values() for b in bpts.values())

if __name__ == "__main__":
    D, PT = parse(D_TXT), parse(P_TXT)
    mine = derived(PT)
    err = max(dist(mine[k], PT[k]) for k in mine)
    print(f"सूत्र जाँच: पी के २६ बिंदु जगन्नाथ होरा से अधिकतम {err*60:.1f} कला अलग")
    Pb = {k: PT[k] for k in mine}
    me1, me20 = hits(D, Pb, 1), hits(D, Pb, 1 / 3)
    print(f"पी: १° के भीतर {me1}, २० कला के भीतर {me20}")
    D_JD = swe.julday(1989, 9, 30, 7.2)
    random.seed(4545); N = 200_000
    t1 = t20 = ge1 = ge20 = 0
    for _ in range(N):
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        g = derived(chart(D_JD + gap * 365.25 + random.uniform(-0.5, 0.5), *place()))
        a, b = hits(D, g, 1), hits(D, g, 1 / 3)
        t1 += a; t20 += b; ge1 += a >= me1; ge20 += b >= me20
    print(f"N = {N:,} वधुएँ, तुलनाएँ प्रति वधू: {45*26}")
    print(f"१° के भीतर: औसत {t1/N:.2f}, पी जितने या ज़्यादा: {100*ge1/N:.1f}%")
    print(f"२० कला के भीतर: औसत {t20/N:.2f}, पी जितने या ज़्यादा: {100*ge20/N:.1f}%")
