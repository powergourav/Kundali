"""
"दोहरा लॉक": राशि कुंडली में राहु-केतु विपरीत, नवांश में एक ही क्रम।
भाव के आधार पर और राशि के आधार पर, दोनों तरह से जाँच।
"""
import random
from kundli_sim import chart, random_birth, place, sign
from sanyog_sim import nav, DINESH, P
from rinanubandh import saptamesh

def h(pl, lg): return (pl - lg) % 12  # भाव (0 = पहला)

def info(b, g):
    r = {}
    r["d1_house_rev"] = (h(sign(b["Rahu"]), sign(b["Lagna"])) - h(sign(g["Rahu"]), sign(g["Lagna"]))) % 12 == 6
    r["d9_house_same"] = h(nav(b["Rahu"]), nav(b["Lagna"])) == h(nav(g["Rahu"]), nav(g["Lagna"]))
    r["d1_sign_rev"] = (sign(b["Rahu"]) - sign(g["Rahu"])) % 12 == 6
    r["d9_sign_same"] = nav(b["Rahu"]) == nav(g["Rahu"])
    def touch(x, y):
        axis = {sign(y["Rahu"]), sign(y["Ketu"])}
        return bool(axis & {sign(x["Moon"]), sign(x["Venus"]), sign(x["Lagna"]), sign(saptamesh(x))})
    r["touch"] = touch(b, g) or touch(g, b)
    return r

if __name__ == "__main__":
    me = info(DINESH, P)
    print("दिनेश-पी:", me)
    random.seed(4); N = 200_000
    keys = ["d1_house_rev", "d9_house_same", "house_lock", "house_lock_touch", "d1_sign_rev", "d9_sign_same", "sign_lock", "touch"]
    c = dict.fromkeys(keys, 0)
    for _ in range(N):
        jb = random_birth(1980, 2001)
        gap = min(12, max(-3, random.gauss(3.5, 2.5)))
        b, g = chart(jb, *place()), chart(jb + gap * 365.25, *place())
        r = info(b, g)
        r["house_lock"] = r["d1_house_rev"] and r["d9_house_same"]
        r["house_lock_touch"] = r["house_lock"] and r["touch"]
        r["sign_lock"] = r["d1_sign_rev"] and r["d9_sign_same"]
        for k in keys: c[k] += r[k]
    for k in keys:
        v = c[k]; print(f"{k:18s} {100*v/N:7.3f}%  " + (f"(~1 in {N/v:,.0f})" if v else ""))
