# Page Math

Pagination arithmetic. 103 items at 10 per page fill 11 pages, and the last page holds only 3.

## What it computes

- **The page truth** - pages needed for a total, what the last page holds, and the items plus SQL OFFSET and LIMIT for one page.
- **The locate truth** - which page an item number lands on, its place on that page, its zero-based index and the page's OFFSET.
- **The window truth** - which page links a pager of a set width shows around the current page, and whether separate first and last page links are needed.

Item counts go to 1000000000, page sizes to 1000000, window widths to 1000. Items and pages count from 1.

## Boundary

Arithmetic only, on whole numbers. It does not know how any real database, API or website pages its results, and gives no verdict on whether your paging is right or fast. Every figure is the owner's own entry.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic (closed-form integer division and clamping).
- `oracle.py` - the Python mirror (lists every page and item for small inputs, divmod for large) that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (81 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/pagemath/
Repo: https://github.com/iLanis-agent/pagemath
