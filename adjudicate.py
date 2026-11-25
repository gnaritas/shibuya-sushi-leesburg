#!/usr/bin/env python3
"""Adjudication probe: enumerate the exact 0px junction pairs and measure footer TEXT lefts."""
import json, sys
from playwright.sync_api import sync_playwright

URL = "https://shibuya-sushi-leesburg-demo.up.railway.app"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PROBE = """() => {
  var out = {pairs: [], footer: {}};
  var main = document.querySelector('main');
  var all = main.querySelectorAll(':scope > section > div > *, :scope > div > div > *');
  for (var i = 1; i < all.length; i++) {
    var a = all[i-1], b = all[i];
    var ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
    if (ra.bottom <= 0 || rb.bottom <= 0) continue;
    if (Math.abs(ra.left - rb.left) >= 4) continue;
    var g = Math.round(rb.top - ra.bottom);
    if (g <= 0) {
      out.pairs.push({prev: a.tagName + '.' + (a.className || ''), next: b.tagName + '.' + (b.className || ''),
                      prev_sel: a.parentNode.tagName + '>' + a.parentNode.className, gap: g});
    }
  }
  function textLeft(el) {
    if (!el) return -1;
    var rng = document.createRange(); rng.selectNodeContents(el);
    var r = rng.getBoundingClientRect();
    return Math.round(r.left);
  }
  out.footer.footline_text = textLeft(document.querySelector('footer p.footline'));
  out.footer.addr_text = textLeft(document.querySelector('address.footnap'));
  out.footer.brand_text = textLeft(document.querySelector('footer p.fbrand'));
  return out;
}"""

pages = ["/", "/menu", "/sushi", "/izakaya", "/sake-bar", "/contact"]
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True, executable_path=CHROME, args=["--no-sandbox"])
    for vw in (1280, 390):
        ctx = b.new_context(viewport={"width": vw, "height": 900 if vw == 1280 else 844}, is_mobile=vw == 390)
        pg = ctx.new_page()
        for path in pages:
            pg.goto(URL + path, wait_until="networkidle", timeout=45000)
            d = pg.evaluate(PROBE)
            print("vw=%-5d %-12s footer_text=%s pairs=%s" % (vw, path, json.dumps(d["footer"]), json.dumps(d["pairs"])[:400]))
        ctx.close()
    b.close()
