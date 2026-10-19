// Page Math engine: exact pagination arithmetic on whole numbers.
var TOTAL_ERR = "the item count must be a whole number from 0 to 1000000000";
var SIZE_ERR = "the page size must be a whole number from 1 to 1000000";
var PAGE_ERR = "the page number must be a whole number from 1 to 1000000000";
var ITEM_ERR = "the item number must be a whole number from 1 to 1000000000";
var COUNT_ERR = "the page count must be a whole number from 1 to 1000000000";
var WIDTH_ERR = "the window width must be a whole number from 1 to 1000";

function _int(t, lo, hi, err) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,10}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pages(n) { return n + (n === 1 ? " page" : " pages"); }
function _items(n) { return n + (n === 1 ? " item" : " items"); }
function _range(a, b) { return a === b ? "item " + a : "items " + a + " to " + b; }
function _span(a, b) { return a === b ? "page " + a : "pages " + a + " to " + b; }

// The page truth: how many pages, what the last one holds, and what one page shows.
function pageTruth(total, size, page) {
  var t = _int(total, 0, 1000000000, TOTAL_ERR), s = _int(size, 1, 1000000, SIZE_ERR), p = _int(page, 1, 1000000000, PAGE_ERR);
  if (t === 0) return "With 0 items there are no pages, so there is nothing to show.";
  var pages = Math.floor((t + s - 1) / s);
  if (p > pages) throw new Error("the page number must be a whole number from 1 to " + pages);
  var last = t - s * (pages - 1);
  var a = s * (p - 1) + 1, b = Math.min(t, s * p);
  return _items(t) + " at " + s + " per page fill " + _pages(pages) + ". " +
    (last === s ? "The last page is full." : "The last page holds " + _items(last) + ".") +
    " Page " + p + " shows " + _range(a, b) + " (OFFSET " + (s * (p - 1)) + ", LIMIT " + s + ").";
}

// The locate truth: which page an item lands on.
function locateTruth(item, size) {
  var k = _int(item, 1, 1000000000, ITEM_ERR), s = _int(size, 1, 1000000, SIZE_ERR);
  var page = Math.floor((k - 1) / s) + 1, pos = k - s * (page - 1);
  return "Item " + k + " at " + s + " per page is on page " + page + ", number " + pos + " on that page. Its zero-based index is " + (k - 1) +
    " and that page starts at OFFSET " + (s * (page - 1)) + ".";
}

// The window truth: which page links a pager of a set width shows.
function windowTruth(current, count, width) {
  var n = _int(count, 1, 1000000000, COUNT_ERR);
  var c = _int(current, 1, 1000000000, PAGE_ERR);
  if (c > n) throw new Error("the current page must be a whole number from 1 to " + n);
  var w = _int(width, 1, 1000, WIDTH_ERR);
  var s = Math.max(1, Math.min(c - Math.floor(w / 2), n - w + 1)), e = Math.min(n, s + w - 1);
  return "On page " + c + " of " + n + ", a window of " + w + (w === 1 ? " link" : " links") + " covers " + _span(s, e) + ". " +
    (s > 1 ? "A separate link to page 1 is needed. " : "Page 1 is already in the window. ") +
    (e < n ? "A separate link to page " + n + " is needed." : "Page " + n + " is already in the window.");
}
