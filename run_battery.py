#!/usr/bin/env python3
"""Vision battery for shibuya-sushi-leesburg new-site sign-off.
OpenRouter gemini-2.5-flash, threaded, forced VERDICT line. Mobile shots resampled to 390 first."""
import base64, json, os, subprocess, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, 'shots')
SMALL = os.path.join(SHOTS, 'small')
os.makedirs(SMALL, exist_ok=True)

env = {}
for line in open(os.path.expanduser('~/.hermes/.env')):
    line = line.strip()
    if line and '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1); env[k.strip()] = v.strip().strip('"\'' )
KEY = env.get('OPENROUTER_API_KEY') or env.get('OPENROUTER_KEY')
if not KEY:
    print('NO OPENROUTER KEY'); sys.exit(2)

# resample mobile dsf2 shots to 390 wide
for f in sorted(os.listdir(SHOTS)):
    if f.startswith('m_') and f.endswith('.png'):
        src = os.path.join(SHOTS, f)
        dst = os.path.join(SMALL, f)
        subprocess.run(['sips', '--resampleWidth', '390', src, '--out', dst],
                       capture_output=True, check=True)
        print('resampled', f)

Q = ("This is a full-page {kind} (390px-wide mobile / 1280px desktop) screenshot of a business website "
     "(dark charcoal + vermillion Japanese-izakaya design, washi-cream body). List every visual or layout defect: "
     "misaligned columns/grids, text overflowing or clipped, uneven margins/spacing, overlapping elements, "
     "stretched/cropped images, broken nav/footer, inconsistent widths, garbled characters or stray glyphs. "
     "Do NOT flag: map tiles that are blank/grey (sweep artifact), faint decorative circles behind text, "
     "dashed/double divider rules (intentional), responsive single-column stacking on mobile, textarea resize "
     "handles, buttons that fit their text tightly, normal line-wrapping in the footer, the © year. "
     "Answer with ONE line only: 'VERDICT: CLEAN' or 'VERDICT: MAP-BLANK' or 'VERDICT: DEFECTS - <list>'.")

def ask(name, path, kind):
    data = base64.b64encode(open(path, 'rb').read()).decode()
    body = {
        'model': 'google/gemini-2.5-flash',
        'temperature': 0.2,
        'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': Q.format(kind=kind)},
            {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + data}},
        ]}],
        'max_tokens': 400,
    }
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
                                 data=json.dumps(body).encode(),
                                 headers={'Authorization': 'Bearer ' + KEY,
                                          'Content-Type': 'application/json'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                j = json.load(r)
            txt = j['choices'][0]['message']['content'].strip()
            return name, txt
        except Exception as e:
            if attempt == 2:
                return name, 'ERROR ' + repr(e)[:120]

jobs = []
for f in sorted(os.listdir(SMALL)):
    if f.endswith('.png'):
        jobs.append((f, os.path.join(SMALL, f), 'mobile'))
for f in sorted(os.listdir(SHOTS)):
    if f.startswith('d_') and f.endswith('.png'):
        jobs.append((f, os.path.join(SHOTS, f), 'desktop'))
jobs.append(('og.png', os.path.join(HERE, 'public', 'og.png'), 'desktop (it is a 1200x630 social share card — judge text fit inside the vermillion disc, no clipping, readable contrast)'))

results = {}
with ThreadPoolExecutor(max_workers=5) as ex:
    for name, txt in ex.map(lambda a: ask(*a), jobs):
        results[name] = txt
        print('%-28s %s' % (name, (txt or '')[:220]))
open(os.path.join(SHOTS, 'vision-results.json'), 'w').write(json.dumps(results, indent=1))
print('wrote vision-results.json')
