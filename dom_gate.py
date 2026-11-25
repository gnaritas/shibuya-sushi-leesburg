#!/usr/bin/env python3
"""DOM-metrics gate for shibuya-sushi-leesburg (measurement = ground truth pass).
Checks at BOTH gate viewports: overflow, nav alignment, map container >=200px,
panel/card rect consistency, label->text gap on the form, bare p+p junctions at 0px."""
import json, os, sys
from playwright.sync_api import sync_playwright

URL = "https://shibuya-sushi-leesburg-demo.up.railway.app"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PROBE = """() => {
  var out = {};
  out.sw = document.documentElement.scrollWidth;
  out.iw = window.innerWidth;
  var nav = document.querySelector('nav.links');
  if (nav) {
    var links = nav.querySelectorAll('a'); var cys = []; var tops = [];
    for (var i = 0; i < links.length; i++) {
      var r = links[i].getBoundingClientRect();
      if (r.width > 0) { cys.push(Math.round(r.top + r.height / 2)); tops.push(Math.round(r.top)); }
    }
    out.nav_cys = cys; out.nav_tops = tops;
    out.nav_scrollw = nav.scrollWidth; out.nav_clientw = nav.clientWidth;
  }
  var frame = document.querySelector('div.mapbox iframe, section.visitmap iframe');
  if (frame) {
    var box = frame.parentNode.getBoundingClientRect();
    out.map_box = {w: Math.round(box.width), h: Math.round(box.height)};
    var fr = frame.getBoundingClientRect();
    out.map_iframe = {w: Math.round(fr.width), h: Math.round(fr.height)};
  }
  var panels = document.querySelectorAll('aside.panel');
  out.panel_w = [];
  for (var i = 0; i < panels.length; i++) out.panel_w.push(Math.round(panels[i].getBoundingClientRect().width));
  var cards = document.querySelectorAll('a.card');
  out.card_w = [];
  for (var i = 0; i < cards.length; i++) out.card_w.push(Math.round(cards[i].getBoundingClientRect().width));
  var h1 = document.querySelector('h1');
  if (h1) { var r = h1.getBoundingClientRect(); out.h1 = {right: Math.round(r.right), bottom: Math.round(r.bottom)}; }
  var main = document.querySelector('main');
  if (main) {
    var zero = 0, blocks = main.querySelectorAll('section, div, p, h2, h3, dl, form, address');
    var prev = null;
    var all = main.querySelectorAll(':scope > section > div > *, :scope > div > div > *');
    var gaps = [];
    var kids = all;
    for (var i = 1; i < kids.length; i++) {
      var a = kids[i-1].getBoundingClientRect(), b = kids[i].getBoundingClientRect();
      if (a.bottom > 0 && b.bottom > 0 && Math.abs(a.left - b.left) < 4) {
        var g = Math.round(b.top - a.bottom);
        if (g < 0) g = 0;
        gaps.push(g);
      }
    }
    out.min_gap = gaps.length ? Math.min.apply(null, gaps) : -1;
  }
  var form = document.querySelector('form.cform');
  if (form) {
    var lbl = form.querySelector('label'); var inp = form.querySelector('input');
    if (lbl && inp) {
      var rng = document.createRange(); rng.selectNodeContents(lbl);
      var tr = rng.getBoundingClientRect(); var ir = inp.getBoundingClientRect();
      out.label_input_gap = Math.round(ir.top - tr.bottom);
    }
  }
  var foot = document.querySelector('footer p.footline');
  if (foot) {
    var fr2 = foot.getBoundingClientRect();
    var addr = document.querySelector('address.footnap');
    out.foot_left = {footline: Math.round(fr2.left), addr: addr ? Math.round(addr.getBoundingClientRect().left) : -1};
  }
  return out;
}"""

def main():
    fails = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, executable_path=CHROME, args=["--no-sandbox"])
        pages = ["/", "/menu", "/sushi", "/izakaya", "/sake-bar", "/contact", "/privacy", "/404", "/thanks"]
        for vw, vh, mob, ua in ((1280, 900, False, None), (390, 844, True, "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")):
            ctx = b.new_context(viewport={"width": vw, "height": vh}, is_mobile=mob, **({"user_agent": ua} if ua else {}))
            pg = ctx.new_page()
            for path in pages:
                pg.goto(URL + path, wait_until="networkidle", timeout=45000)
                pg.wait_for_timeout(900)
                d = pg.evaluate(PROBE)
                tag = ("desktop" if vw == 1280 else "mobile")
                issues = []
                if d["sw"] > d["iw"] + 1: issues.append("overflow %d>%d" % (d["sw"], d["iw"]))
                if "map_box" in d and d["map_box"]["w"] < 200: issues.append("map box %d<200" % d["map_box"]["w"])
                if "map_iframe" in d and d["map_iframe"]["w"] < 200: issues.append("map iframe %d<200" % d["map_iframe"]["w"])
                cys = d.get("nav_cys") or []
                if len(set(cys)) > 1 and vw == 1280: issues.append("nav cy spread %r" % cys)
                if d.get("nav_scrollw", 0) > d.get("nav_clientw", 10 ** 9) + 1: issues.append("nav clipped")
                cw = d.get("card_w") or []
                if vw == 1280 and len(cw) == 3 and max(cw) - min(cw) > 2: issues.append("card widths %r" % cw)
                if d.get("min_gap", -1) == 0: issues.append("0px junction")
                lg = d.get("label_input_gap")
                if lg is not None and lg < 4: issues.append("label gap %d" % lg)
                fl = d.get("foot_left")
                if fl and fl["addr"] >= 0 and abs(fl["footline"] - fl["addr"]) > 2: issues.append("footer left %r" % fl)
                print("%-8s %-14s %s %s" % (tag, path, json.dumps(d, sort_keys=True)[:150], "CLEAN" if not issues else "FLAG " + "; ".join(issues)))
                if issues: fails.append((tag, path, issues))
            ctx.close()
        b.close()
    print("GATE:", "CLEAN" if not fails else "FLAGS %r" % fails)
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
