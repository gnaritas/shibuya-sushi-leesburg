#!/usr/bin/env python3
"""Render sweep for the LIVE G&A Pizzeria demo (t_0e8cb9b4).
Playwright + real Chrome. Mobile 390x844 is_mobile at DPR 1 and 2 (scrollWidth must equal innerWidth)
plus full-page screenshots at 390 (x2) and 1280 (x1) saved to shots/ for the vision battery."""
import glob, os, sys, json
from playwright.sync_api import sync_playwright

URL = (sys.argv[1] if len(sys.argv) > 1 else "https://shibuya-sushi-leesburg-demo.up.railway.app").rstrip("/")
HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, "shots")
os.makedirs(SHOTS, exist_ok=True)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1")
PAGES = [("/" if os.path.basename(p) == "index.html" else "/" + os.path.basename(p)[:-5])
         for p in sorted(glob.glob(os.path.join(HERE, "public", "*.html")))]

def main():
    bad = []
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, executable_path=CHROME, args=["--no-sandbox"])
        # overflow gates: mobile x1 / x2
        for scale, label in ((1, "x1"), (2, "x2")):
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=scale,
                                is_mobile=True, user_agent=UA)
            pg = ctx.new_page()
            for path in PAGES:
                try:
                    pg.goto(URL + path, wait_until="networkidle", timeout=45000)
                    d = json.loads(pg.evaluate("JSON.stringify({sw:document.documentElement.scrollWidth,iw:innerWidth})"))
                except Exception as e:
                    d = {"sw": -1, "iw": -1}
                    print("GOTO ERR", path, repr(e)[:80])
                ok = 0 < d["iw"] and d["sw"] <= d["iw"] + 1
                print("%s-390 %-36s sw=%-5d iw=%d %s" % (label, path, d["sw"], d["iw"], "OK" if ok else "OVERFLOW"))
                if not ok:
                    bad.append((label, path, d["sw"], d["iw"]))
            ctx.close()
        # mobile full-page shots (DPR2)
        ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2,
                            is_mobile=True, user_agent=UA)
        pg = ctx.new_page()
        for path in PAGES:
            pg.goto(URL + path, wait_until="networkidle", timeout=45000)
            pg.screenshot(path=os.path.join(SHOTS, ("m_" + path.strip("/").replace("/", "-") or "home") + ".png"), full_page=True)
        ctx.close()
        # desktop full-page shots (1280)
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        pg = ctx.new_page()
        for path in PAGES:
            pg.goto(URL + path, wait_until="networkidle", timeout=45000)
            pg.screenshot(path=os.path.join(SHOTS, ("d_" + path.strip("/").replace("/", "-") or "home") + ".png"), full_page=True)
        ctx.close()
        b.close()
    print("SHOTS ->", SHOTS)
    print("SWEEP:", "CLEAN" if not bad else "FAILURES %r" % bad)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
