"""
जगन्नाथ होरा की दोनों तालिकाओं के सभी बिंदुओं में से कितने जोड़े आपस में १° (और २० कला) के भीतर हैं,
और संयोग से कितने अपेक्षित हैं।

अपेक्षा का तरीका (ज्यामितीय): दिनेश के सारे ४५ बिंदुओं को एक साथ एक रैंडम कोण से घुमाया जाता है।
इससे दोनों बिंदु-समूहों का आपसी संरेखण रैंडम हो जाता है, पर घुमाई गई कुंडली ज्योतिषीय रूप से
संभव कुंडली नहीं है (जैसे योग स्फुट = सूर्य + चंद्र, असली कुंडली में २ गुना खिसकता)।
ज्योतिषीय रूप से सही तुलना, जिसमें वधू के स्फुट सूत्र से बनते हैं, bindu45_dinesh.py में है।
"""
import math, random
S = {s: i for i, s in enumerate("Ar Ta Ge Cn Le Vi Li Sc Sg Cp Aq Pi".split())}

P_TXT = """Lagna 11 Pi 11 14.87|Sun 3 Ta 41 49.80|Moon 0 Cp 08 00.48|Mars 3 Le 15 18.18|Mercury 23 Ta 23 16.67|Jupiter 18 Sc 25 27.38|Venus 8 Ar 33 40.41|Saturn 29 Aq 05 36.30|Rahu 10 Li 41 08.30|Ketu 10 Ar 41 08.30|Maandi 1 Pi 46 04.28|Gulika 18 Aq 39 13.72|BhavaL 18 Pi 01 35.25|HoraL 3 Aq 11 55.50|GhatiL 18 Vi 42 56.23|VighatiL 6 Sc 17 59.90|VarnadaL 11 Ge 11 14.87|SreeL 14 Ge 47 27.73|PranapadaL 7 Cn 08 34.69|InduL 0 Aq 08 00.48|BhriguB 20 Sc 24 34.39|Dhooma 17 Vi 01 49.80|Vyatipata 12 Li 58 10.20|Parivesha 12 Ar 58 10.20|IndraChapa 17 Pi 01 49.80|Upaketu 3 Ar 41 49.80|Kaala 22 Ar 31 01.27|Mrityu 1 Sg 29 10.43|ArthaPrahara 21 Sg 00 37.43|YamaGhantaka 12 Cp 14 40.75|PranaSph 14 Sc 35 28.07|DehaSph 19 Aq 43 17.53|MrityuSph 14 Cn 16 25.82|SookTri 18 Cp 35 11.42|TithiSph 26 Sc 26 10.68|YogaSphSM 3 Aq 49 50.28|RahuTithi 6 Vi 59 18.50|Kshetra 21 Sg 48 46.04|Beeja 0 Cp 40 57.60|TriSph 29 Li 58 29.06|Chatus 3 Sg 40 18.86|Pancha 14 Ge 21 27.17|Kunda 6 Cp 11 04.56|YogaSph 7 Ta 09 50.28|Avayoga 13 Sc 49 50.28"""
D_TXT = """Lagna 8 Sg 34 33.06|Sun 13 Vi 24 50.94|Moon 17 Vi 42 42.68|Mars 13 Vi 14 57.35|Mercury 3 Vi 12 22.87|Jupiter 15 Ge 51 15.63|Venus 26 Li 49 57.49|Saturn 13 Sg 53 46.03|Rahu 29 Cp 40 07.06|Ketu 29 Cn 40 07.06|Maandi 23 Vi 13 30.68|Gulika 13 Vi 09 24.38|BhavaL 19 Sg 15 57.94|HoraL 25 Pi 22 49.80|GhatiL 13 Cp 43 25.38|VighatiL 15 Cp 26 23.29|VarnadaL 8 Sc 34 33.06|SreeL 6 Cn 47 45.53|PranapadaL 15 Ta 42 08.15|InduL 17 Aq 42 42.68|BhriguB 23 Ta 41 24.87|Dhooma 26 Cp 44 50.94|Vyatipata 3 Ge 15 09.06|Parivesha 3 Sg 15 09.06|IndraChapa 26 Cn 44 50.94|Upaketu 13 Le 24 50.94|Kaala 2 Sc 30 38.66|Mrityu 11 Sg 59 48.24|ArthaPrahara 4 Cp 07 31.33|YamaGhantaka 29 Cp 34 51.50|PranaSph 26 Aq 02 09.67|DehaSph 4 Ge 51 05.86|MrityuSph 15 Sc 30 41.63|SookTri 16 Sg 23 57.16|TithiSph 4 Ar 17 51.75|YogaSphSM 1 Pi 07 33.62|RahuTithi 16 Le 15 16.13|Kshetra 16 Ta 48 55.66|Beeja 26 Ge 06 04.05|TriSph 9 Sc 26 40.13|Chatus 22 Ar 51 31.06|Pancha 22 Aq 31 38.12|Kunda 4 Pi 38 37.69|YogaSph 4 Ge 27 33.62|Avayoga 11 Sg 07 33.62"""

def parse(t):
    out = {}
    for row in t.split("|"):
        n, d, s, m, sec = row.split()
        out[n] = S[s] * 30 + int(d) + int(m) / 60 + float(sec) / 3600
    return out

def dist(a, b): return abs((a - b + 180) % 360 - 180)

P, D = parse(P_TXT), parse(D_TXT)
if __name__ == "__main__":
    pairs = [(a, b, dist(P[a], D[b])) for a in P for b in D]
    for lim in (1, 1/3):
        hits = sorted([x for x in pairs if x[2] <= lim], key=lambda x: x[2])
        exp = len(pairs) * 2 * lim / 360
        print(f"\n{lim*60:.0f} कला के भीतर: {len(hits)} जोड़े (रैंडम अपेक्षा ~{exp:.1f}), कुल तुलनाएँ {len(pairs)}")
        for a, b, d in hits: print(f"   पी {a:12s} - दिनेश {b:12s} {d*60:5.1f}'")
    # ज्यामितीय अपेक्षा: दिनेश के बिंदुओं को एक साथ रैंडम घुमाकर (ऊपर docstring देखें)
    random.seed(1)
    shifts = [random.uniform(0, 360) for _ in range(2000)]
    pct = lambda xs, p: xs[max(0, math.ceil(p * len(xs)) - 1)]   # nearest-rank परसेंटाइल
    for lim in (1, 1/3):
        cnt = sorted(sum(dist(P[a], D[b] + sh) <= lim for a in P for b in D) for sh in shifts)
        print(f"\nरैंडम घुमाव पर {lim*60:.0f} कला के भीतर जोड़े: औसत {sum(cnt)/len(cnt):.1f}, "
              f"5%-95%: {pct(cnt, 0.05)}-{pct(cnt, 0.95)}")
