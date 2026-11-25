#!/usr/bin/env python3
import json
from playwright.sync_api import sync_playwright
URL = "https://shibuya-sushi-leesburg-demo.up.railway.app"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

JS404 = """() => {
  var a = [];
  document.querySelectorAll('main a').forEach(function (x) {
    var r = x.getBoundingClientRect();
    a.push([x.textContent.trim().slice(0, 22), Math.round(r.left), Math.round(r.right), window.innerWidth]);
  });
  return a;
}"""

JSFOOT = """() => {
  var out = [];
  ['p.ftel a', 'p.fmail a'].forEach(function (s) {
    var x = document.querySelector(s);
    if (x) {
      var r = x.getBoundingClientRect();
      var box = x.closest('footer').querySelector('.footgrid').getBoundingClientRect();
      out.push([s, Math.round(r.left), Math.round(r.right), Math.round(window.innerWidth), Math.round(box.right)]);
    }
  });
  return out;
}"""

JSFNLINES = """() => {
  var out = [];
  ['p.fline', 'p.fline2'].forEach(function (s) {
    var els = document.querySelectorAll('footer ' + s);
    els.forEach(function (y, i) {
      var r = y.getBoundingClientRect();
      out.push([s + '#' + i, Math.round(r.left), Math.round(r.right), Math.round(r.height)]);
    });
  });
  var br = document.querySelector('footer p.bunrule');
  if (br) { var r2 = br.getBoundingClientRect(); out.push(['bunrule', Math.round(r2.left), Math.round(r2.right), 0]); }
  return out;
}"""

JSPANEL = """() => {
  var out = [];
  var ps = document.querySelectorAll('aside.panel p');
  if (ps.length) { var r = ps[0].getBoundingClientRect(); out.push(['panel-para', Math.round(r.left), Math.round(r.right)]); }
  var rng = document.createRange();
  var f = document.querySelector('footer p.footline');
  if (f) { rng.selectNodeContents(f); var rr = rng.getBoundingClientRect(); out.push(['footline-text', Math.round(rr.left), Math.round(rr.right)]); }
  var b = document.querySelector('footer p.fbrand');
  if (b) { var rb = b.getBoundingClientRect(); out.push(['fbrand-box', Math.round(rb.left), Math.round(rb.right)]); }
  return out;
}"""

def run():
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, executable_path=CHROME, args=["--no-sandbox"])
        ctx = b.new_context(viewport={"width": 390, "height": 844}, is_mobile=True)
        pg = ctx.new_page()
        for path, js in (("/404", JS404), ("/sushi", JSFOOT), ("/menu", JSFNLINES)):
            pg.goto(URL + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(500)
            print("m", path, json.dumps(pg.evaluate(js)))
        ctx.close()
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        pg = ctx.new_page()
        for path, js in (("/menu", JSFNLINES), ("/", JSPANEL)):
            pg.goto(URL + path, wait_until="networkidle", timeout=45000)
            pg.wait_for_timeout(500)
            print("d", path, json.dumps(pg.evaluate(js)))
        ctx.close()
        b.close()

run()
