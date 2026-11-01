"""
Parashara's Light का दशकूट (कालप्रकाशिका विधि, ४४ अंक) - पूरी गणना।
अधिकतम अंक (रिपोर्ट के कुल से निकाले गए): दिन ३, गण ६, माहेंद्र २, स्त्री-दीर्घ २,
योनि ४, राशि ७, राशीश ५, वश्य २, रज्जु ८, वेध २ = ४१; लिंग १, गोत्र १, वर्ण १ = ३।
गोत्र (नक्षत्र-गोत्र) की तालिका उपलब्ध नहीं, इसलिए हमेशा १ माना गया।
"""
import collections
from kundli_sim import ashtakoot
from dashakoot_enum import dashakoot, pada_info

def score44(Lb, bn, bs, Lg, gn, gs):
    k = dashakoot(bn, bs, gn, gs); a = ashtakoot(Lb, Lg)
    s = (3 * k["दिन"] + 6 * k["गण"] + 2 * k["माहेंद्र"] + 2 * k["स्त्री-दीर्घ"] + a["yoni"]
         + 7 * k["राशि"] + a["maitri"] + 2 * k["वश्य"] + 8 * k["रज्जु"] + 2 * k["वेध"])
    return s + 1 + 1 + a["varna"]   # लिंग, गोत्र, वर्ण

if __name__ == "__main__":
    DB, DG = 12 * 4 + 2, 20 * 4 + 1          # हस्त ३, उत्तराषाढ़ा २
    me = score44(*pada_info(DB), *pada_info(DG))
    print("दिनेश-पी:", me, "/ ४४")
    both = collections.Counter(); fixed = collections.Counter()
    for pb in range(108):
        for pg in range(108):
            s = score44(*pada_info(pb), *pada_info(pg))
            both[s] += 1
            if pb == DB: fixed[s] += 1
    for name, d, n in (("दोनों रैंडम", both, 108 * 108), ("दिनेश स्थिर", fixed, 108)):
        ge = sum(v for s, v in d.items() if s >= me)
        print(f"\n{name}: {me}+ पाने वाले {100*ge/n:.2f}%  (~1 in {n/ge:.1f})")
        cum = 0
        for s in sorted(d, reverse=True):
            cum += d[s]
            if s >= 30 or s == me: print(f"   {s:4.1f}: इतना या ज़्यादा {100*cum/n:6.2f}%")
