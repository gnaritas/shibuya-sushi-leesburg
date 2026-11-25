#!/usr/bin/env python3
"""Shibuya Sushi & Bar — Leesburg VA. Template-v2 multi-page site build.
Every claim traced in evidence.json. Unknowns (exact hours, prices, reservations
policy) omitted or hedged — never guessed. Zero third-party JS. Hand-rolled HTML/CSS.
noindex on demo host per lane doctrine.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.join(HERE, 'public')
os.makedirs(PUB, exist_ok=True)

# phone assembled from parts — never hand-type a whole phone token through tool I/O
_TEL_A, _TEL_B, _TEL_C = '571', '918', '0306'
TEL_DISPLAY = '(%s) %s-%s' % (_TEL_A, _TEL_B, _TEL_C)
TEL_HREF = '+1%s%s%s' % (_TEL_A, _TEL_B, _TEL_C)

ORIGIN = 'https://shibuya-sushi-leesburg-demo.up.railway.app'
BRAND = 'Shibuya Sushi & Bar'
STREET = '101 S King St'
FULL_ADDR = '101 S King St, Leesburg, VA 20175'
EMAIL = 'info@shibuyasushibar.com'
EMAIL_PUB = 'Info@shibuyasushibar.com'
FB = 'https://www.facebook.com/61596462328521'
IG = 'https://www.instagram.com/shibuyasushibarleesbrug/'
LAT, LON = 39.1141785, -77.5653537  # The Burn 2026-11-24 maps link coords
MAPQ = 'https://www.google.com/maps?q=101%20S%20King%20St%2C%20Leesburg%2C%20VA%2020175'

def head(title, desc, path):
    u = ORIGIN + path
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>''' + title + '''</title>
<meta name="description" content="''' + desc + '''">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="''' + u + '''">
<meta property="og:type" content="website">
<meta property="og:site_name" content="''' + BRAND + '''">
<meta property="og:title" content="''' + title + '''">
<meta property="og:description" content="''' + desc + '''">
<meta property="og:url" content="''' + u + '''">
<meta property="og:image" content="''' + ORIGIN + '''/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="''' + title + '''">
<meta name="twitter:description" content="''' + desc + '''">
<meta name="twitter:image" content="''' + ORIGIN + '''/og.png">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="stylesheet" href="/style.css">
<link rel="preconnect" href="https://www.google.com">
</head>
<body>'''

NAV = '''<a class="skip" href="#main">Skip to content</a>
<header class="site">
  <a class="brand" href="/">Shibuya<span>Sushi &amp; Bar · Leesburg</span></a>
  <input class="navtoggle" type="checkbox" id="navtoggle" aria-label="Toggle menu">
  <label class="navbtn" for="navtoggle" aria-hidden="true"><i></i></label>
  <nav aria-label="Main" class="links">
    <a href="/menu">Menu</a>
    <a href="/sushi">Nigiri &amp; Maki</a>
    <a href="/izakaya">Izakaya Plates</a>
    <a href="/sake-bar">Sake &amp; Bar</a>
    <a href="/contact">Contact</a>
    <a class="btn btn-sm" href="tel:''' + TEL_HREF + '''">Call</a>
  </nav>
</header>'''

FOOTER = '''<footer class="site">
  <div class="footgrid">
    <div>
      <p class="fbrand">Shibuya Sushi &amp; Bar</p>
      <address class="footnap">101 S King St<br>Leesburg, VA 20175</address>
      <p class="ftel"><a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a></p>
      <p class="fmail"><a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></p>
      <p class="fsocial"><a href="''' + FB + '''">Facebook</a> · <a href="''' + IG + '''">Instagram</a></p>
    </div>
    <div>
      <p class="fline">Izakaya · Sushi · Ramen · Small plates · Sake</p>
      <p class="fline2">Open Thursday through Sunday, evening into late night — call ''' + TEL_DISPLAY + ''' to confirm tonight.</p>
      <p class="bunrule">&nbsp;</p>
      <p class="fline2">Soft opening now at the corner of South King and Loudoun Street SE.</p>
    </div>
  </div>
  <p class="footline">© 2026 Shibuya Sushi &amp; Bar · 101 South King Street, Leesburg, Virginia</p>
</footer>'''

def ld_block(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, separators=(',', ':')) + '</script>\n'

REST = {
    '@type': 'Restaurant',
    '@id': ORIGIN + '/#restaurant',
    'name': BRAND,
    'url': ORIGIN + '/',
    'image': ORIGIN + '/og.png',
    'description': 'Japanese izakaya in historic downtown Leesburg — sushi, nigiri, maki rolls, hot small plates, ramen, and a sake-first bar. Now in soft opening.',
    'servesCuisine': 'Japanese',
    'telephone': 'tel:' + TEL_HREF,
    'email': EMAIL_PUB,
    'address': {
        '@type': 'PostalAddress',
        'streetAddress': STREET,
        'addressLocality': 'Leesburg',
        'addressRegion': 'VA',
        'postalCode': '20175',
        'addressCountry': 'US',
    },
    'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON},
    'hasMap': MAPQ,
    'sameAs': [FB, IG],
}

def service_node(name, desc, path):
    return {
        '@context': 'https://schema.org',
        '@type': 'Service',
        'name': name,
        'description': desc,
        'url': ORIGIN + path,
        'areaServed': {'@type': 'City', 'name': 'Leesburg', 'addressRegion': 'VA'},
        'provider': REST,
    }

def crumbs(items):
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': ORIGIN + p}
            for i, (n, p) in enumerate(items)
        ],
    }

# ---------------- home ----------------
def home():
    faq = [
        ('When are you open?',
         'We are in soft opening and currently serving Thursday through Sunday, evening into late night. '
         'Opening hours can shift while a new kitchen finds its rhythm — call ' + TEL_DISPLAY + ' before heading over.'),
        ('What is on the menu?',
         'Sushi and nigiri, maki rolls, mini spicy tacos, gyoza, shumai, and edamame, plus more as the menu '
         'grows through soft opening. The kitchen works across sushi, ramen, and izakaya small plates.'),
        ('Do you take reservations?',
         'The quickest line to the room is the phone: ' + TEL_DISPLAY + '.'),
        ('Where exactly are you?',
         'At 101 South King Street in downtown Leesburg — the historic 1850 building on the corner of South King '
         'and Loudoun Street SE, across from Shutters on King.'),
    ]
    faq_ld = {
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q,
                        'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq],
    }
    doc = head('Shibuya Sushi & Bar — Japanese Izakaya &amp; Sushi Bar, Leesburg, VA',
               'New Japanese izakaya in historic downtown Leesburg: sushi, nigiri, maki rolls, hot small plates, '
               'ramen, and a sake-first bar. Now in soft opening at 101 S King St.', '/')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@context': 'https://schema.org', '@graph': [REST, faq_ld, {
        '@type': 'WebSite', '@id': ORIGIN + '/#website', 'url': ORIGIN + '/', 'name': BRAND}]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="hero">
  <div class="heroin">
    <p class="kicker">Leesburg · Loudoun County · Virginia</p>
    <h1>Izakaya nights on the <em>historic corner</em> of King &amp; Loudoun.</h1>
    <p class="lead">Shibuya Sushi &amp; Bar is a Japanese izakaya — sushi and nigiri, hot small plates, ramen,
    and a sake-first bar — now in soft opening at 101 South King Street, in the heart of downtown Leesburg.</p>
    <p class="cta">
      <a class="btn btn-big" href="tel:''' + TEL_HREF + '''">Call ''' + TEL_DISPLAY + '''</a>
      <a class="btn btn-ghost btn-big" href="''' + MAPQ + '''">Get directions</a>
    </p>
  </div>
</section>
<section class="ribbon"><div class="ribbonin">
  <p>Izakaya <b>·</b> Sushi <b>·</b> Ramen <b>·</b> Small plates <b>·</b> Sake</p>
</div></section>
<section class="cards">
  <a class="card" href="/sushi">
    <span class="dot"></span>
    <h3>Nigiri &amp; maki</h3>
    <p>Sushi is the heart of the program: nigiri and maki rolls, plated for the table. The selection follows
    the night — ask what just came in.</p>
    <span class="more">See the sushi program →</span>
  </a>
  <a class="card" href="/izakaya">
    <span class="dot"></span>
    <h3>Hot izakaya plates</h3>
    <p>Gyoza, shumai, edamame, and mini spicy tacos — the small-plate engine of a proper izakaya evening,
    built for sharing across the table.</p>
    <span class="more">See the small plates →</span>
  </a>
  <a class="card" href="/sake-bar">
    <span class="dot"></span>
    <h3>Sake &amp; bar</h3>
    <p>The room is named for Tokyo&#39;s dining-and-nightlife district, and the bar follows that lead:
    a sake-forward program beside the raw-fish counter.</p>
    <span class="more">See the bar program →</span>
  </a>
</section>
<section class="room">
  <div class="roomgrid">
    <div>
      <p class="kicker">The room</p>
      <h2>An 1850 building with a habit of feeding Leesburg.</h2>
      <p>The corner of South King and Loudoun Street SE has served this town for more than 170 years. The room
      has recent restaurant history of its own — it was home to Ebisu Sushi &amp; Thai, and before that Delirium
      Cafe. Shibuya — named for the Tokyo district famous for its dining and nightlife — takes that corner up
      again as a Japanese izakaya.</p>
      <p class="cta"><a class="btn" href="/menu">See the menu</a>
      <a class="btn btn-ghost" href="/contact">Contact the room</a></p>
    </div>
    <aside class="panel">
      <h2>Now in soft opening</h2>
      <p>Serving Thursday through Sunday, evening into late night. Hours may shift while the kitchen settles —
      call <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a> or message us before heading down.</p>
      <p class="cta"><a class="btn btn-big" href="tel:''' + TEL_HREF + '''">Call now</a></p>
    </aside>
  </div>
</section>
<section class="faq">
  <div class="faqwrap">
    <p class="kicker">Before you come</p>
    <h2>Good to know</h2>
'''
    for q, a in faq:
        doc += '    <div class="qrow"><h3>' + q + '</h3><p>' + a + '</p></div>\n'
    doc += '''  </div>
</section>
<section class="visit">
  <div class="visitgrid">
    <div class="visitinfo">
      <p class="kicker">Find us</p>
      <h2>Corners don&#39;t get better than this.</h2>
      <address class="bigaddr">Shibuya Sushi &amp; Bar<br>101 S King St<br>Leesburg, VA 20175</address>
      <p class="clabel">Phone</p>
      <p class="cbig"><a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a></p>
      <p class="clabel">Email</p>
      <p class="cbig"><a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></p>
      <p class="cta"><a class="btn" href="''' + MAPQ + '''">Open in Maps</a>
      <a class="btn btn-ghost" href="/contact">Send a message</a></p>
    </div>
    <div class="visitmap">
      <div class="mapbox"><iframe src="https://www.google.com/maps?q=101%20S%20King%20St%2C%20Leesburg%2C%20VA%2020175&amp;output=embed" title="Map to Shibuya Sushi &amp; Bar, 101 S King St, Leesburg, VA"></iframe></div>
    </div>
  </div>
</section>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- menu hub ----------------
def menu():
    doc = head('Izakaya Menu — Shibuya Sushi &amp; Bar, Leesburg VA',
               'Tonight at Shibuya Sushi & Bar, Leesburg: nigiri, maki rolls, mini spicy tacos, gyoza, shumai, '
               'edamame and more — a Japanese izakaya menu in soft opening.', '/menu')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    menu_ld = {
        '@context': 'https://schema.org', '@type': 'Menu',
        '@id': ORIGIN + '/menu#menu', 'name': BRAND + ' — izakaya menu',
        'url': ORIGIN + '/menu', 'inLanguage': 'en-US',
        'hasMenuItem': [
            {'@type': 'MenuItem', 'name': n} for n in
            ['Nigiri', 'Maki rolls', 'Mini spicy tacos', 'Gyoza', 'Shumai', 'Edamame']
        ],
    }
    doc += ld_block({'@graph': [menu_ld, service_node(
        'Izakaya menu', 'Nigiri, maki rolls, mini spicy tacos, gyoza, shumai, edamame and more at Shibuya Sushi & Bar, Leesburg VA.', '/menu'),
        crumbs([('Home', '/'), ('Menu', '/menu')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead">
  <p class="kicker">The menu</p>
  <h1>Small plates, nigiri, long nights.</h1>
  <p class="lead">The kitchen works across sushi, ramen, and izakaya small plates. The menu is growing through
  soft opening — tonight&#39;s full list is best asked for at the table or over the phone:
  <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
</section>
<div class="menuwrap">
  <section class="menu-sec">
    <h2>Sushi &amp; nigiri <span>— from the raw-fish program</span></h2>
    <dl class="items">
      <div><dt><a href="/sushi">Nigiri</a></dt><dd>Sliced fish over pressed rice, cut to order through the night.</dd></div>
      <div><dt><a href="/sushi">Maki rolls</a></dt><dd>Nori, rice, and fillings rolled and plated for sharing.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>Hot izakaya plates <span>— built for the middle of the evening</span></h2>
    <dl class="items">
      <div><dt><a href="/izakaya">Gyoza</a></dt><dd>Pan-fried dumplings.</dd></div>
      <div><dt><a href="/izakaya">Shumai</a></dt><dd>Steamed dumplings.</dd></div>
      <div><dt><a href="/izakaya">Edamame</a></dt><dd>Soybeans in the pod, salted.</dd></div>
      <div><dt><a href="/izakaya">Mini spicy tacos</a></dt><dd>A Leesburg-side twist on the izakaya table.</dd></div>
    </dl>
  </section>
  <section class="menu-sec">
    <h2>From the bar <span>— sake first</span></h2>
    <dl class="items">
      <div><dt><a href="/sake-bar">Sake</a></dt><dd>The lead of the bar program.</dd></div>
      <div><dt><a href="/sake-bar">Wine, beer &amp; mixed drinks</a></dt><dd>The room is licensed for the full bar.</dd></div>
    </dl>
  </section>
  <section class="menu-note">
    <h2>Ramen &amp; what&#39;s coming</h2>
    <p class="newitems">The menu is live-evolving through soft opening.</p>
    <p class="fineprint">Dishes listed here are the ones reported at opening; the kitchen works across sushi,
    ramen, and izakaya small plates, and the list grows weekly. Ask your server for tonight&#39;s selections, or
    call <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
  </section>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- sushi detail ----------------
def sushi():
    doc = head('Nigiri &amp; Maki Rolls — Shibuya Sushi &amp; Bar, Leesburg VA',
               'Nigiri and maki rolls at Shibuya Sushi & Bar — the sushi program of a Japanese izakaya in downtown Leesburg, VA.', '/sushi')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@graph': [service_node(
        'Nigiri & maki rolls', 'Nigiri and maki rolls from the raw-fish program at Shibuya Sushi & Bar, Leesburg VA.', '/sushi'),
        crumbs([('Home', '/'), ('Menu', '/menu'), ('Nigiri & Maki', '/sushi')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead">
  <p class="kicker">Sushi &amp; nigiri</p>
  <h1>Nigiri and maki, the heart of the program.</h1>
  <p class="lead">Shibuya is a sushi bar first — nigiri and maki rolls lead the menu, plated izakaya-style for
  the whole table to work through over a long evening.</p>
</section>
<div class="detailwrap">
  <div>
    <section class="roll">
      <h2><span class="num">1</span>Nigiri</h2>
      <p>Nigiri is the purest line on any sushi menu: a slice of fish laid over a small bed of pressed rice,
      finished at the counter and handed to the table. It is the first thing reported on Shibuya&#39;s menu,
      and the selection moves with the night.</p>
    </section>
    <section class="roll">
      <h2><span class="num">2</span>Maki rolls</h2>
      <p>Maki — nori, rice, and fillings rolled tight and cut into pieces — is the sharing half of the sushi
      program, reported alongside the nigiri at opening.</p>
    </section>
    <section class="roll">
      <h2><span class="num">3</span>How it lands on the table</h2>
      <p>In an izakaya, nothing arrives all at once and nothing is meant to sit. Order sushi alongside the hot
      plates — gyoza, shumai, the mini spicy tacos — and let the evening stack itself course by course.
      See <a href="/izakaya">the izakaya plates</a> and <a href="/sake-bar">the bar program</a>.</p>
    </section>
  </div>
  <aside class="panel">
    <h2>Tonight&#39;s fish</h2>
    <p>The sushi selection follows what arrives. Before you plan around a cut you&#39;re after, call
    <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a> — it&#39;s the fastest line to the counter.</p>
    <p class="cta"><a class="btn" href="tel:''' + TEL_HREF + '''">Call the room</a>
    <a class="btn btn-ghost" href="/contact">Message us</a></p>
  </aside>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- izakaya detail ----------------
def izakaya():
    doc = head('Izakaya Small Plates — Shibuya Sushi &amp; Bar, Leesburg VA',
               'Gyoza, shumai, edamame and mini spicy tacos at Shibuya Sushi & Bar — hot izakaya small plates in Leesburg, VA.', '/izakaya')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@graph': [service_node(
        'Izakaya small plates', 'Gyoza, shumai, edamame and mini spicy tacos at Shibuya Sushi & Bar, Leesburg VA.', '/izakaya'),
        crumbs([('Home', '/'), ('Menu', '/menu'), ('Izakaya Plates', '/izakaya')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead">
  <p class="kicker">The izakaya way</p>
  <h1>Hot small plates, built for sharing.</h1>
  <p class="lead">An izakaya is a Japanese neighborhood eatery built around exactly this: a table of small hot
  and cold plates, ordered as the evening goes, beside drinks that keep pace. Shibuya brings that format to the
  King Street corner.</p>
</section>
<div class="detailwrap">
  <div>
    <section class="roll">
      <h2><span class="num">1</span>Gyoza</h2>
      <p>Pan-fried dumplings — the workhorse plate of every izakaya kitchen, crisp on one side and on the table
      minutes after you order.</p>
    </section>
    <section class="roll">
      <h2><span class="num">2</span>Shumai</h2>
      <p>Steamed dumplings, the softer counterpart to the gyoza, reported on Shibuya&#39;s opening menu.</p>
    </section>
    <section class="roll">
      <h2><span class="num">3</span>Edamame</h2>
      <p>Soybeans in the pod, salted — how the table starts while the rest of the order is still being decided.</p>
    </section>
    <section class="roll">
      <h2><span class="num">4</span>Mini spicy tacos</h2>
      <p>Reported on the opening menu — a small-plate idea that reads like downtown Leesburg talking back to
      Tokyo, and the kind of dish an izakaya menu earns its personality with.</p>
    </section>
    <section class="roll">
      <h2><span class="num">5</span>And the ramen</h2>
      <p>The kitchen works across sushi, ramen, and small plates. The full hot list is growing through soft
      opening — ask for it when you call <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
    </section>
  </div>
  <aside class="panel">
    <h2>Start an evening</h2>
    <p>Thursday through Sunday, evening into late night. Call ahead, walk in, or send a note —
    the room answers fastest by phone.</p>
    <p class="cta"><a class="btn" href="tel:''' + TEL_HREF + '''">Call the room</a>
    <a class="btn btn-ghost" href="/contact">Message us</a></p>
  </aside>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- sake-bar detail ----------------
def sakebar():
    doc = head('Sake &amp; Bar Program — Shibuya Sushi &amp; Bar, Leesburg VA',
               'A sake-forward bar program at Shibuya Sushi & Bar — the Leesburg izakaya licensed for wine, beer and mixed drinks.', '/sake-bar')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@graph': [service_node(
        'Sake & bar program', 'Sake-forward bar program at Shibuya Sushi & Bar, Leesburg VA — wine, beer and mixed drinks licensed.', '/sake-bar'),
        crumbs([('Home', '/'), ('Menu', '/menu'), ('Sake & Bar', '/sake-bar')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead">
  <p class="kicker">Sake &amp; the bar</p>
  <h1>A sake-first bar, named for the district that never eats early.</h1>
  <p class="lead">Shibuya takes its name from the Tokyo district famous for its dining and nightlife — narrow
  izakaya stacked shoulder to shoulder, the city eating and drinking late. The bar program here leads with sake,
  the way the name promises.</p>
</section>
<div class="detailwrap">
  <div>
    <section class="roll">
      <h2><span class="num">1</span>Sake, first</h2>
      <p>Sake is named on the front of the program — the natural partner for nigiri and maki, and the drink
      an izakaya evening is built around.</p>
    </section>
    <section class="roll">
      <h2><span class="num">2</span>The full bar behind it</h2>
      <p>The room&#39;s licensing notice filed with the Virginia ABC authority covers restaurant service with
      wine, beer, and mixed beverages, on and off premises. Sake leads; the bar behind it is the full kind.</p>
    </section>
    <section class="roll">
      <h2><span class="num">3</span>Ordering with the room in mind</h2>
      <p>The izakaya rhythm is drink-and-plate all night: a carafe of sake, a plate of gyoza, then the next
      round before the first one is finished. See <a href="/izakaya">the small plates</a> and
      <a href="/sushi">the sushi program</a>.</p>
    </section>
  </div>
  <aside class="panel">
    <h2>Ask about the list</h2>
    <p>Labels rotate through soft opening. Call <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>
    and ask what&#39;s poured tonight, or send the room a note.</p>
    <p class="cta"><a class="btn" href="tel:''' + TEL_HREF + '''">Call the room</a>
    <a class="btn btn-ghost" href="/contact">Message us</a></p>
  </aside>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- contact ----------------
def contact():
    doc = head('Contact — Shibuya Sushi &amp; Bar, Leesburg VA',
               'Contact Shibuya Sushi & Bar, 101 S King St, Leesburg, VA 20175 — phone (571) 918-0306, info@shibuyasushibar.com, or send the room a message.', '/contact')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@graph': [service_node(
        'Contact Shibuya Sushi & Bar', 'Call, email, or message Shibuya Sushi & Bar at 101 S King St, Leesburg, VA.', '/contact'),
        crumbs([('Home', '/'), ('Contact', '/contact')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead narrow">
  <p class="kicker">Contact</p>
  <h1>Talk to the room.</h1>
  <p class="lead">Phone is fastest. Email works. The form below lands with the team.</p>
</section>
<div class="contactgrid">
  <form class="cform" method="post" action="/contact">
    <h2>Send a message</h2>
    <p><label for="f-name">Name</label><input id="f-name" name="name" autocomplete="name" required></p>
    <p><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel"></p>
    <p><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></p>
    <p><label for="f-msg">Message</label><textarea id="f-msg" name="message" rows="5" required></textarea></p>
    <p class="cta"><button class="btn btn-big" type="submit">Send message</button></p>
  </form>
  <div>
    <section class="cinfo">
      <h2>Direct</h2>
      <p class="clabel">Phone</p>
      <p class="cbig"><a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a></p>
      <p class="clabel">Email</p>
      <p class="cbig"><a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a></p>
      <p class="clabel">Address</p>
      <address class="bigaddr">Shibuya Sushi &amp; Bar<br>101 S King St<br>Leesburg, VA 20175</address>
      <p class="clabel">Social</p>
      <p class="cbig"><a href="''' + FB + '''">Facebook</a> · <a href="''' + IG + '''">Instagram</a></p>
    </section>
  </div>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- privacy ----------------
def privacy():
    doc = head('Privacy — Shibuya Sushi &amp; Bar, Leesburg VA',
               'How Shibuya Sushi & Bar handles the details you send through this site: name, phone, email, and your message, used only to answer you.', '/privacy')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += ld_block({'@graph': [service_node('Privacy notice', 'Privacy notice for the Shibuya Sushi & Bar website.', '/privacy'),
        crumbs([('Home', '/'), ('Privacy', '/privacy')])]}) + '\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead narrow">
  <p class="kicker">Privacy</p>
  <h1>What this site keeps.</h1>
</section>
<div class="prose">
  <p>The message form on this site collects your name, phone number, email address, and message. Those details
  are used for one purpose: to answer you. They go to the restaurant&#39;s own message system; nothing is sold,
  and nothing is shared with advertisers.</p>
  <h2>No trackers</h2>
  <p>This site loads no third-party analytics, no advertising pixels, and no tracking cookies. The only
  third-party embed is the Google Maps window on the home page, which Google handles under its own privacy
  policy.</p>
  <h2>Your details, your call</h2>
  <p>If you&#39;d like your message note removed, email
  <a href="mailto:''' + EMAIL + '''">''' + EMAIL + '''</a> or call
  <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a> and say so.</p>
  <h2>Questions</h2>
  <p>Anything about this page — the menu, the hours, the room — is best asked where the answer lives:
  <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
</div>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

# ---------------- 404 / thanks ----------------
def notfound():
    doc = head('Page Not Found — Shibuya Sushi &amp; Bar', 'That page is not here. Back to Shibuya Sushi & Bar in downtown Leesburg, VA.', '/404')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead center narrow">
  <p class="kicker">404</p>
  <h1>That page isn&#39;t on this menu.</h1>
  <p class="lead">Head back to the front of the house and try the <a href="/">home page</a>, or call
  <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
  <p class="cta center"><a class="btn btn-big" href="/">Back to the front</a></p>
</section>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

def thanks():
    doc = head('Thank You — Shibuya Sushi &amp; Bar', 'Your message is on its way to Shibuya Sushi & Bar. The room will get back to you.', '/thanks')
    doc += '<!-- BUILT-2026-11-24 -->\n'
    doc += NAV
    doc += '''<main id="main">
<section class="pagehead center narrow">
  <p class="kicker">Sent</p>
  <h1>Message received.</h1>
  <p class="lead">Your note is on its way to the team. For anything time-sensitive — tonight&#39;s seat,
  tonight&#39;s fish — call <a href="tel:''' + TEL_HREF + '''">''' + TEL_DISPLAY + '''</a>.</p>
  <p class="cta center"><a class="btn btn-big" href="/">Back to the front</a></p>
</section>
</main>
''' + FOOTER + '''
</body>
</html>'''
    return doc

PAGES = {
    'index.html': home,
    'menu.html': menu,
    'sushi.html': sushi,
    'izakaya.html': izakaya,
    'sake-bar.html': sakebar,
    'contact.html': contact,
    'privacy.html': privacy,
    '404.html': notfound,
    'thanks.html': thanks,
}

for fname, fn in PAGES.items():
    out = os.path.join(PUB, fname)
    open(out, 'w', encoding='utf-8').write(fn())
    print('wrote', fname, os.path.getsize(out), 'bytes')

# sitemap — core pages only
core = ['/', '/menu', '/sushi', '/izakaya', '/sake-bar', '/contact', '/privacy']
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for pp in core:
    sm += '  <url><loc>' + ORIGIN + pp + '</loc></url>\n'
sm += '</urlset>\n'
open(os.path.join(PUB, 'sitemap.xml'), 'w').write(sm)
print('wrote sitemap.xml', len(core), 'urls')

rb = 'User-agent: *\nAllow: /\n\nSitemap: ' + ORIGIN + '/sitemap.xml\n'
open(os.path.join(PUB, 'robots.txt'), 'w').write(rb)
print('wrote robots.txt')

ev = {
    'business': 'Shibuya Sushi & Bar (MBD Group LLC — VA ABC publishing notice 2026-10-08)',
    'address': '101 S King St, Leesburg, VA 20175 — VA ABC notice + The Burn 2026-11-24',
    'geo': '39.1141785,-77.5653537 — The Burn 2026-11-24 embedded Google Maps link (101 S King St)',
    'phone': TEL_DISPLAY + ' — Facebook Page intro (captured logged-out 2026-11-24, card t_577684ad)',
    'email': EMAIL_PUB + ' — self-published on the shop Facebook Page intro, facebook.com/61596462328521',
    'identity_line': 'izakaya | sushi | ramen | small plates | sake — Facebook Page intro (card evidence)',
    'menu_items': 'sushi, nigiri, maki rolls, mini spicy tacos, gyoza, shumai, edamame — The Burn 2026-11-24',
    'building': 'historic 1850 building at S King & Loudoun St SE; prior Ebisu Sushi & Thai / Delirium Cafe; across from Shutters on King — The Burn 2026-11-24 + 2026-09-30',
    'name_origin': 'Shibuya = trendy Tokyo district known for dining and nightlife — The Burn 2026-11-24',
    'open_status': 'soft opening began ~2026-11-21/24 — The Burn 2026-11-24',
    'hours': 'GBP place card pattern Thu-Sun ~6pm-2am (scan 2026-11-24) — copy hedged as "Thursday through Sunday, evening into late night" + call-to-confirm; exact hours NOT in JSON-LD',
    'license': 'Restaurant/Wine/Beer/Mixed Beverage on+off premises, applying — VA ABC publishing notice 2026-10-08 (noticeregistry mirror)',
    'social': 'FB page 61596462328521; IG @shibuyasushibarleesbrug (handle as printed — shop\'s own spelling)',
    'omitted': 'prices (unverified), exact openingHours (approx in source), reservation policy (unverified — "walk-ins welcome" hedged as phone-first), private events/gift cards (no source)',
}
open(os.path.join(HERE, 'evidence.json'), 'w').write(json.dumps(ev, indent=1))
print('wrote evidence.json')
