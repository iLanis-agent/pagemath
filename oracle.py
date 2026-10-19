#!/usr/bin/env python3
# Page Math oracle - mirrors engine.js. Small cases are checked by listing every page and item; large ones use divmod.
import json, re

TOTAL_ERR = "the item count must be a whole number from 0 to 1000000000"
SIZE_ERR = "the page size must be a whole number from 1 to 1000000"
PAGE_ERR = "the page number must be a whole number from 1 to 1000000000"
ITEM_ERR = "the item number must be a whole number from 1 to 1000000000"
COUNT_ERR = "the page count must be a whole number from 1 to 1000000000"
WIDTH_ERR = "the window width must be a whole number from 1 to 1000"

def num(t, lo, hi, err):
    t = t.strip() if isinstance(t, str) else ""
    if not re.fullmatch(r"[0-9]{1,10}", t): raise ValueError(err)
    v = int(t)
    if v < lo or v > hi: raise ValueError(err)
    return v

def plural(n, one, many): return f"{n} {one if n == 1 else many}"

def chunks(t, s):
    # list pages as (first, last) item numbers when small enough to list
    return [(a, min(t, a + s - 1)) for a in range(1, t + 1, s)]

def page_truth(total, size, page):
    t = num(total, 0, 10**9, TOTAL_ERR); s = num(size, 1, 10**6, SIZE_ERR); p = num(page, 1, 10**9, PAGE_ERR)
    if t == 0: return "With 0 items there are no pages, so there is nothing to show."
    if t <= 20000:
        cs = chunks(t, s); pages = len(cs); last = cs[-1][1] - cs[-1][0] + 1
        if p > pages: raise ValueError(f"the page number must be a whole number from 1 to {pages}")
        a, b = cs[p - 1]
    else:
        q, r = divmod(t, s); pages = q + (1 if r else 0); last = r if r else s
        if p > pages: raise ValueError(f"the page number must be a whole number from 1 to {pages}")
        a = (p - 1) * s + 1; b = min(t, p * s)
    rng = f"item {a}" if a == b else f"items {a} to {b}"
    lastsent = "The last page is full." if last == s else f"The last page holds {plural(last, 'item', 'items')}."
    return f"{plural(t, 'item', 'items')} at {s} per page {"fills" if t == 1 else "fill"} {plural(pages, 'page', 'pages')}. {lastsent} Page {p} shows {rng} (OFFSET {(p - 1) * s}, LIMIT {s})."

def locate(item, size):
    k = num(item, 1, 10**9, ITEM_ERR); s = num(size, 1, 10**6, SIZE_ERR)
    if k <= 20000:
        page = next(i for i, (a, b) in enumerate(chunks(k, s), 1) if a <= k <= b)
        a = (page - 1) * s + 1
        pos = k - a + 1
    else:
        page, rem = divmod(k - 1, s); page += 1; pos = rem + 1
    return f"Item {k} at {s} per page is on page {page}, number {pos} on that page. Its zero-based index is {k - 1} and that page starts at OFFSET {(page - 1) * s}."

def window(current, count, width):
    n = num(count, 1, 10**9, COUNT_ERR)
    c = num(current, 1, 10**9, PAGE_ERR)
    if c > n: raise ValueError(f"the current page must be a whole number from 1 to {n}")
    w = num(width, 1, 1000, WIDTH_ERR)
    wp = min(w, n)
    ideal = c - w // 2
    if n <= 3000:
        cands = [s for s in range(1, n - wp + 2) if s <= c <= s + wp - 1]
    else:
        cands = [s for s in {1, n - wp + 1, ideal} if 1 <= s <= n - wp + 1 and s <= c <= s + wp - 1]
    s = min(cands, key=lambda x: (abs(x - ideal), x)); e = s + wp - 1
    span = f"page {s}" if s == e else f"pages {s} to {e}"
    return (f"On page {c} of {n}, a window of {w} {'link' if w == 1 else 'links'} covers {span}. " +
            ("A separate link to page 1 is needed. " if s > 1 else "Page 1 is already in the window. ") +
            (f"A separate link to page {n} is needed." if e < n else f"Page {n} is already in the window."))

FNS = {"pageTruth": page_truth, "locateTruth": locate, "windowTruth": window}
CASES = [
    ("pageTruth", ["103", "10", "11"]), ("pageTruth", ["103", "10", "1"]), ("pageTruth", ["100", "10", "10"]), ("pageTruth", ["100", "10", "5"]), ("pageTruth", ["1", "10", "1"]),
    ("pageTruth", ["10", "10", "1"]), ("pageTruth", ["11", "10", "2"]), ("pageTruth", ["0", "10", "1"]), ("pageTruth", ["5", "1", "5"]), ("pageTruth", ["5", "1", "1"]),
    ("pageTruth", ["7", "3", "3"]), ("pageTruth", ["7", "3", "2"]), ("pageTruth", ["19", "10", "2"]), ("pageTruth", ["20000", "7", "2858"]), ("pageTruth", ["20001", "20000", "2"]),
    ("pageTruth", ["1000000000", "1000000", "1000"]), ("pageTruth", ["1000000000", "1", "1000000000"]), ("pageTruth", ["999999999", "1000000", "1000"]), ("pageTruth", ["30000", "7", "4286"]), ("pageTruth", ["30001", "7", "4286"]),
    ("pageTruth", [" 103 ", " 10 ", " 11 "]), ("pageTruth", ["103", "10", "12"]), ("pageTruth", ["103", "10", "0"]), ("pageTruth", ["103", "0", "1"]), ("pageTruth", ["103", "1000001", "1"]),
    ("pageTruth", ["1000000001", "10", "1"]), ("pageTruth", ["x", "10", "1"]), ("pageTruth", ["103", "10", ""]), ("pageTruth", ["-5", "10", "1"]), ("pageTruth", ["0", "0", "1"]), ("pageTruth", ["10.5", "10", "1"]),
    ("locateTruth", ["1", "10"]), ("locateTruth", ["10", "10"]), ("locateTruth", ["11", "10"]), ("locateTruth", ["95", "10"]), ("locateTruth", ["100", "10"]),
    ("locateTruth", ["101", "10"]), ("locateTruth", ["1", "1"]), ("locateTruth", ["57", "1"]), ("locateTruth", ["57", "57"]), ("locateTruth", ["58", "57"]),
    ("locateTruth", ["20000", "7"]), ("locateTruth", ["20001", "7"]), ("locateTruth", ["1000000000", "1000000"]), ("locateTruth", ["1000000000", "7"]), ("locateTruth", ["999999", "1000000"]),
    ("locateTruth", ["0", "10"]), ("locateTruth", ["5", "0"]), ("locateTruth", ["x", "10"]), ("locateTruth", ["1000000001", "10"]), ("locateTruth", ["5", ""]),
    ("windowTruth", ["11", "20", "5"]), ("windowTruth", ["1", "20", "5"]), ("windowTruth", ["20", "20", "5"]), ("windowTruth", ["2", "20", "5"]), ("windowTruth", ["19", "20", "5"]),
    ("windowTruth", ["3", "20", "5"]), ("windowTruth", ["18", "20", "5"]), ("windowTruth", ["10", "20", "4"]), ("windowTruth", ["10", "20", "1"]), ("windowTruth", ["1", "1", "5"]),
    ("windowTruth", ["2", "3", "10"]), ("windowTruth", ["3", "5", "5"]), ("windowTruth", ["4", "5", "3"]), ("windowTruth", ["1", "5", "5"]), ("windowTruth", ["500", "1000", "1000"]),
    ("windowTruth", ["500", "1000", "999"]), ("windowTruth", ["500000000", "1000000000", "7"]), ("windowTruth", ["1", "1000000000", "7"]), ("windowTruth", ["1000000000", "1000000000", "7"]), ("windowTruth", ["2999", "3000", "2"]),
    ("windowTruth", ["5", "3500", "10"]), ("windowTruth", ["3500", "3500", "10"]), ("windowTruth", [" 11 ", " 20 ", " 5 "]), ("windowTruth", ["21", "20", "5"]), ("windowTruth", ["0", "20", "5"]),
    ("windowTruth", ["5", "0", "5"]), ("windowTruth", ["5", "20", "0"]), ("windowTruth", ["5", "20", "1001"]), ("windowTruth", ["x", "20", "5"]), ("windowTruth", ["5", "", "5"]),
]
out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
