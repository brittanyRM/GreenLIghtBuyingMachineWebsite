import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)

CSS = r"""
  :root{
    --ink:#101C22; --ink-soft:#1B2C34;
    --paper:#E8E7E0; --paper-dim:#DEDDD5;
    --green:#1B6B3A; --green-bright:#3BA85F; --amber:#B87514;
    --rule:#C6C5BB;
    --display:"Archivo",system-ui,sans-serif;
    --body:"Literata",Georgia,serif;
    --plan:"Spline Sans Mono",ui-monospace,monospace;
    --gutter:clamp(1.25rem,5vw,4.5rem);
    --measure:34rem;
  }
  *{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%;scroll-behavior:smooth}
  @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);
    font-size:clamp(1rem,.96rem + .2vw,1.075rem);line-height:1.62}
  h1,h2,h3,.ui{font-family:var(--display);font-weight:800;letter-spacing:-.02em;line-height:1.04}
  h1{font-size:clamp(2.4rem,1.5rem + 4vw,4.4rem);margin:0 0 1.1rem}
  h2{font-size:clamp(1.8rem,1.2rem + 2.2vw,2.9rem);margin:0 0 1.1rem}
  h3{font-size:1.15rem;font-weight:600;letter-spacing:-.01em;margin:0 0 .4rem;line-height:1.25}
  p{margin:0 0 1.05rem;max-width:var(--measure)}
  a{color:inherit}
  .wrap{padding-inline:var(--gutter);max-width:78rem;margin-inline:auto}
  section{padding-block:clamp(3.25rem,6vw,5.5rem)}
  .band{background:var(--ink);color:var(--paper)}
  .lede{font-size:clamp(1.08rem,1rem + .5vw,1.3rem);max-width:32rem;opacity:.92}

  a.btn{display:inline-block;font-family:var(--display);font-weight:600;font-size:1rem;
    letter-spacing:-.01em;text-decoration:none;padding:.85rem 1.5rem;border-radius:2px;
    background:var(--green-bright);color:var(--ink);border:1px solid transparent}
  a.btn:hover{background:#4FC176}
  a.btn.ghost{background:transparent;color:inherit;border-color:currentColor;opacity:.8}
  a.btn.ghost:hover{opacity:1}
  a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{
    outline:3px solid var(--amber);outline-offset:3px}

  /* nav */
  .nav{background:var(--ink);color:var(--paper)}
  .nav .wrap{display:flex;align-items:center;justify-content:space-between;gap:1rem 2rem;
    flex-wrap:wrap;padding-block:1.15rem}
  .nav .brand{font-family:var(--display);font-weight:800;letter-spacing:-.02em;
    text-decoration:none;font-size:1.02rem;line-height:1.15}
  .nav ul{list-style:none;display:flex;flex-wrap:wrap;gap:.35rem 1.4rem;margin:0;padding:0;
    font-family:var(--display);font-weight:500;font-size:.94rem}
  .nav a{text-decoration:none;opacity:.72;padding-block:.2rem}
  .nav a:hover{opacity:1}
  .nav a[aria-current="page"]{opacity:1;box-shadow:inset 0 -2px 0 var(--green-bright)}
  .nav .btn{padding:.55rem 1.1rem;font-size:.92rem;opacity:1}

  /* page headers */
  .phead{background:var(--ink);color:var(--paper);padding-block:clamp(2.75rem,6vw,4.75rem)}
  .phead p{max-width:36rem;opacity:.88;margin-bottom:0}
  .kicker{font-family:var(--plan);font-size:.78rem;letter-spacing:.08em;color:var(--green-bright);
    margin:0 0 1rem;display:block}

  /* plan drawing */
  .plan{width:100%;height:auto;display:block}
  .plan .sheet{fill:none;stroke:rgba(232,231,224,.22);stroke-width:1}
  .plan .shell{fill:none;stroke:var(--paper);stroke-width:6}
  .plan .keep{stroke:rgba(232,231,224,.55);stroke-width:4}
  .plan .new{stroke:var(--green-bright);stroke-width:4;stroke-linecap:square}
  .plan text{font-family:var(--plan);fill:var(--paper);font-size:15px;letter-spacing:.04em}
  .plan .tag{fill:var(--green-bright);font-size:14px}
  .plan .note{fill:rgba(232,231,224,.55);font-size:13px}
  .plan .fade{opacity:0}
  .plan .new{stroke-dasharray:var(--len,200);stroke-dashoffset:var(--len,200);
    animation:draw .55s ease-out forwards;animation-delay:var(--d,0s)}
  .plan .fade{animation:fadein .5s ease-out forwards;animation-delay:var(--d,0s)}
  @keyframes draw{to{stroke-dashoffset:0}}
  @keyframes fadein{to{opacity:1}}
  @media(prefers-reduced-motion:reduce){.plan .new,.plan .fade{animation:none;stroke-dashoffset:0;opacity:1}}
  .plan-cap{font-family:var(--plan);font-size:.78rem;opacity:.55;margin-top:.9rem}

  /* layout helpers */
  .split{display:grid;gap:clamp(2rem,4vw,3.5rem);grid-template-columns:1fr}
  @media(min-width:52rem){.split{grid-template-columns:repeat(2,minmax(0,1fr))}}
  @media(min-width:62rem){.split.thirds{grid-template-columns:repeat(3,minmax(0,1fr))}}
  .split p{max-width:30rem}
  .hero-grid{display:grid;gap:clamp(2.25rem,5vw,4rem);grid-template-columns:1fr}
  @media(min-width:62rem){.hero-grid{grid-template-columns:minmax(0,25rem) minmax(0,1fr);align-items:center}}
  .cta-row{display:flex;gap:.75rem;flex-wrap:wrap;margin-top:1.75rem}

  .roles{border-top:2px solid var(--ink);padding-top:1.15rem}
  .band .roles{border-color:rgba(232,231,224,.35)}
  .roles .who{font-family:var(--display);font-weight:600;font-size:.88rem;color:var(--green);
    margin-bottom:.85rem;display:block}
  .band .roles .who{color:var(--green-bright)}

  ul.plain{list-style:none;padding:0;margin:0 0 1rem;max-width:var(--measure)}
  ul.plain li{padding:.55rem 0;border-bottom:1px solid var(--rule)}
  .band ul.plain li{border-color:rgba(232,231,224,.2)}

  .fit{display:grid;gap:2.25rem;grid-template-columns:1fr}
  @media(min-width:52rem){.fit{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .fit .col{padding-left:1.25rem;border-left:3px solid var(--green)}
  .fit .col.not{border-left-color:var(--amber)}
  .fit ul{padding:0;margin:.5rem 0 0}
  .fit li{list-style:none;padding:.5rem 0;border-bottom:1px solid var(--rule)}

  ol.stages{list-style:none;counter-reset:s;padding:0;margin:2rem 0 0;display:grid;grid-template-columns:1fr}
  @media(min-width:44rem){ol.stages{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:clamp(2rem,4vw,4rem)}}
  ol.stages li{counter-increment:s;display:grid;grid-template-columns:2.75rem 1fr;gap:.75rem;
    padding:.9rem 0;border-bottom:1px solid var(--rule);align-items:baseline}
  ol.stages li::before{content:counter(s,decimal-leading-zero);font-family:var(--plan);
    font-size:.85rem;color:var(--green);letter-spacing:.05em}
  ol.stages b{font-family:var(--display);font-weight:600;letter-spacing:-.01em}
  ol.stages span{display:block;font-size:.95rem;opacity:.75;line-height:1.45}

  .doors{display:grid;gap:1.5rem;grid-template-columns:1fr;margin-top:2.5rem}
  @media(min-width:52rem){.doors{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .door{border:1px solid var(--rule);padding:clamp(1.5rem,3vw,2.25rem);display:flex;
    flex-direction:column;border-top:4px solid var(--green)}
  .door.buy{border-top-color:var(--amber)}
  .door .who{font-family:var(--plan);font-size:.75rem;letter-spacing:.08em;
    color:var(--green);margin-bottom:.9rem}
  .door.buy .who{color:var(--amber)}
  .door h3{font-size:clamp(1.3rem,1.1rem + .8vw,1.75rem);font-weight:800;letter-spacing:-.02em;margin-bottom:.75rem}
  .door p{flex:1;max-width:none}
  .door .cta-row{margin-top:1.25rem}
  .band .door{border-color:rgba(232,231,224,.3)}

  .qa{border-top:1px solid var(--rule);padding-block:1.4rem;max-width:44rem}
  .qa h3{margin-bottom:.35rem}
  .qa p{margin-bottom:0;max-width:none}

  .book{display:grid;gap:2rem;align-items:start;grid-template-columns:1fr}
  @media(min-width:52rem){.book{grid-template-columns:15rem 1fr;gap:3.5rem}}
  .cover{aspect-ratio:6/9;background:var(--ink);color:var(--paper);padding:1.75rem 1.4rem;
    display:flex;flex-direction:column;justify-content:space-between;border-radius:1px}
  .cover .t{font-family:var(--display);font-weight:800;font-size:1.5rem;line-height:1.03;letter-spacing:-.02em}
  .cover .a{font-family:var(--plan);font-size:.75rem;opacity:.7;letter-spacing:.04em}
  .cover .soon{font-family:var(--display);font-weight:600;font-size:.8rem;color:var(--green-bright);
    margin-bottom:.35rem}
  .cover .bar{height:5px;background:var(--green-bright);width:60%}

  .portrait{aspect-ratio:4/5;background:var(--paper-dim);border:1px solid var(--rule);
    display:flex;align-items:center;justify-content:center;font-family:var(--plan);
    font-size:.8rem;color:#8b8a80;text-align:center;padding:1rem}

  /* form */
  form{max-width:40rem}
  .field{margin-bottom:1.15rem}
  .field label{display:block;font-family:var(--display);font-weight:600;font-size:.9rem;margin-bottom:.35rem}
  .field input,.field select,.field textarea{width:100%;font:inherit;font-size:1rem;
    padding:.7rem .8rem;border:1px solid var(--rule);border-radius:2px;background:#fff;color:var(--ink)}
  .field textarea{min-height:7rem;resize:vertical}
  .field .hint{font-size:.85rem;opacity:.65;margin:.3rem 0 0}
  .pair{display:grid;gap:1.15rem;grid-template-columns:1fr}
  @media(min-width:40rem){.pair{grid-template-columns:repeat(2,minmax(0,1fr))}}
  button.submit{font-family:var(--display);font-weight:600;font-size:1rem;padding:.85rem 1.6rem;
    background:var(--green-bright);color:var(--ink);border:0;border-radius:2px;cursor:pointer}
  button.submit:hover{background:#4FC176}
  button.submit:disabled{opacity:.55;cursor:not-allowed}
  .hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
  .status{max-width:40rem;padding:.85rem 1rem;border-radius:2px;margin-bottom:1.25rem;
    border-left:3px solid var(--rule);background:var(--paper-dim);font-size:.95rem}
  .status.ok{border-left-color:var(--green);background:#DDE9DF}
  .status.err{border-left-color:var(--amber);background:#F0E4CC}

  .todo{background:var(--amber);color:#180F02;padding:.06em .45em;border-radius:2px;
    font-family:var(--plan);font-size:.82em}

  footer{padding-block:2.5rem;font-size:.9rem}
  footer .wrap{display:grid;gap:1.5rem;grid-template-columns:1fr;border-top:1px solid var(--rule);padding-top:1.75rem}
  @media(min-width:52rem){footer .wrap{grid-template-columns:1fr 1fr 1.4fr}}
  footer h4{font-family:var(--display);font-size:.9rem;margin:0 0 .6rem}
  footer ul{list-style:none;padding:0;margin:0}
  footer li{padding:.2rem 0}
  footer a{opacity:.75;text-decoration:none}
  footer a:hover{opacity:1;text-decoration:underline}
  footer .fine{opacity:.6}
"""

PLAN_SVG = r"""<svg class="plan" viewBox="0 0 720 440" role="img" aria-labelledby="plantitle">
  <title id="plantitle">Floor plan showing a three-bedroom house redivided into seven rentable rooms around a shared kitchen and living area.</title>
  <rect class="sheet" x="6" y="6" width="708" height="428"/>
  <rect class="shell" x="26" y="30" width="668" height="366"/>
  <line class="keep" x1="150" y1="30" x2="150" y2="396"/>
  <line class="keep" x1="392" y1="30" x2="392" y2="396"/>
  <line class="new" x1="150" y1="196" x2="694" y2="196" style="--len:544;--d:.25s"/>
  <line class="new" x1="150" y1="238" x2="694" y2="238" style="--len:544;--d:.35s"/>
  <line class="new" x1="272" y1="30"  x2="272" y2="196" style="--len:166;--d:.6s"/>
  <line class="new" x1="530" y1="30"  x2="530" y2="196" style="--len:166;--d:.7s"/>
  <line class="new" x1="312" y1="238" x2="312" y2="396" style="--len:158;--d:.8s"/>
  <line class="new" x1="472" y1="238" x2="472" y2="396" style="--len:158;--d:.9s"/>
  <g class="tag">
    <text class="fade" style="--d:1.15s" x="200" y="120">01</text>
    <text class="fade" style="--d:1.2s"  x="322" y="120">02</text>
    <text class="fade" style="--d:1.25s" x="452" y="120">03</text>
    <text class="fade" style="--d:1.3s"  x="602" y="120">04</text>
    <text class="fade" style="--d:1.35s" x="220" y="330">05</text>
    <text class="fade" style="--d:1.4s"  x="382" y="330">06</text>
    <text class="fade" style="--d:1.45s" x="574" y="330">07</text>
  </g>
  <text class="note fade" style="--d:1.6s" x="326" y="223">shared corridor</text>
  <text class="fade" style="--d:1.6s" transform="translate(96,300) rotate(-90)" font-size="14">kitchen &#183; living &#183; laundry</text>
  <text class="note fade" style="--d:1.75s" x="26" y="420">existing walls</text>
  <text class="tag fade" style="--d:1.75s" x="170" y="420">new walls</text>
</svg>"""

NAVLINKS = [
    ("index.html", "Home"),
    ("how-it-works.html", "Build with us"),
    ("for-buyers.html", "Buy a property"),
    ("the-book.html", "The book"),
    ("about.html", "About"),
]

def nav(current):
    items = ""
    for href, label in NAVLINKS:
        cur = ' aria-current="page"' if href == current else ""
        items += '<li><a href="%s"%s>%s</a></li>\n' % (href, cur, label)
    return """<nav class="nav">
  <div class="wrap">
    <a class="brand" href="index.html">Green Light<br>Buying Machine</a>
    <ul>
%s    </ul>
    <a class="btn" href="apply.html">Get a deal analyzed</a>
  </div>
</nav>""" % items

FOOTER = """<footer>
  <div class="wrap">
    <div>
      <h4>Green Light Buying Machine</h4>
      <p class="fine" style="margin:0">Co-living conversions for experienced Arizona flippers.</p>
    </div>
    <div>
      <h4>Pages</h4>
      <ul>
        <li><a href="how-it-works.html">Build with us</a></li>
        <li><a href="is-it-for-you.html">Is the program for you</a></li>
        <li><a href="for-buyers.html">Buy a finished property</a></li>
        <li><a href="the-book.html">The book</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="apply.html">Get a deal analyzed</a></li>
      </ul>
    </div>
    <div>
      <h4>Fine print</h4>
      <p class="fine" style="margin:0">Real estate investing carries risk. Results depend on the property, the market, and your own execution. Nothing on this site is a guarantee of profit, financial advice, or an offer to sell a security. <span class="todo">Have counsel review before launch.</span></p>
    </div>
  </div>
</footer>"""

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<meta name="description" content="{{DESC}}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;800&family=Literata:opsz,wght@7..72,400;7..72,500&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{{CSS}}</style>
</head>
<body>
{{NAV}}
{{MAIN}}
{{FOOTER}}
<script>
/* Handles every form marked .js-form. Posts JSON to the form's action,
   which forwards to GoHighLevel server-side. Messages come from data
   attributes on the form so each one can speak for itself. */
(function () {
  var FALLBACK = 'hello@example.com'; /* TODO: real inbox */

  Array.prototype.forEach.call(document.querySelectorAll('.js-form'), function (form) {
    var button = form.querySelector('[type=submit]');
    var label = button.textContent;
    var status = document.createElement('div');
    status.className = 'status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.hidden = true;
    form.parentNode.insertBefore(status, form);

    function show(kind, message) {
      status.hidden = false;
      status.className = 'status ' + kind;
      status.textContent = message;
    }

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var payload = {};
      new FormData(form).forEach(function (value, key) { payload[key] = value; });
      payload.source = form.dataset.source || 'website';
      payload.page = window.location.pathname;

      button.disabled = true;
      button.textContent = 'Sending\u2026';
      show('pending', form.dataset.sending || 'Sending\u2026');

      fetch(form.action, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(function (response) {
          if (!response.ok) throw new Error(response.status);
          form.reset();
          show('ok', form.dataset.success || 'Thanks \u2014 we got it.');
          button.textContent = 'Sent';
        })
        .catch(function () {
          show('err', 'That didn\u2019t send. Email ' + FALLBACK + ' and we\u2019ll pick it up from there.');
          button.disabled = false;
          button.textContent = label;
        });
    });
  });
})();
</script>
</body>
</html>
"""

def phead(kicker, h1, lede):
    return """<header class="phead">
  <div class="wrap">
    <span class="kicker">%s</span>
    <h1>%s</h1>
    <p class="lede">%s</p>
  </div>
</header>""" % (kicker, h1, lede)

CTA_BAND = """<section class="band">
  <div class="wrap">
    <h2>Send us a property. We'll tell you if it converts.</h2>
    <p>No charge, no pitch. Send an address and we'll come back with whether the house works for co-living, roughly what room count it supports, and what the conversion would involve. If it's a no, we'll tell you why.</p>
    <div class="cta-row">
      <a class="btn" href="apply.html">Get a deal analyzed</a>
      <a class="btn ghost" href="is-it-for-you.html">See if the program fits</a>
    </div>
  </div>
</section>"""

PAGES = {}

# ---------------------------------------------------------------- home
PAGES["index.html"] = dict(
title="Green Light Buying Machine — co-living conversions for experienced flippers",
desc="A done-with-you program for Arizona fix-and-flippers moving into co-living. We source the deal, you renovate, we bring the buyer.",
main="""<header class="phead">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1 style="font-size:clamp(2.9rem,1.5rem + 6vw,5.6rem)">One house.<br>Seven doors.</h1>
        <p class="lede">Co-living conversions in Arizona, built by operators who already know how to run a rehab and sold to investors who want the finished product. We connect both ends and stand in the middle.</p>
        <div class="cta-row">
          <a class="btn" href="how-it-works.html">I build</a>
          <a class="btn ghost" href="for-buyers.html">I buy</a>
        </div>
      </div>
      <figure style="margin:0">
        """ + PLAN_SVG + """
        <figcaption class="plan-cap">Same footprint. Seven rentable rooms instead of one retail sale.</figcaption>
      </figure>
    </div>
  </div>
</header>

<section>
  <div class="wrap">
    <h2>You're bidding on the same houses as everyone else.</h2>
    <div class="split">
      <div>
        <p>Every flipper in the Valley is competing for the same MLS inventory and selling to the same retail buyer pool. Margins thin out, days on market stretch, and the exit depends on what a family with a mortgage will pay that month.</p>
        <p>Co-living changes what a house is worth, because it changes who buys it. A property converted to shared housing sells to an investor pricing off room-level income, not comps down the street.</p>
      </div>
      <div>
        <p>The catch is that the learning curve is unforgiving. Room count, egress, parking, bathroom ratios, city occupancy rules, the finish standard operators expect &mdash; get one wrong and a good deal becomes an expensive education.</p>
        <p>This program exists so you don't pay for that education with your own capital. You bring the crew and the execution. We bring the deal, the standard, and the buyer.</p>
        <p><a href="how-it-works.html">How the program works &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Who does what</h2>
    <div class="split thirds" style="margin-top:2.5rem">
      <div class="roles">
        <span class="who">We handle</span>
        <h3>Finding the deal</h3>
        <p>We source properties that actually convert &mdash; right bones, right block, right numbers &mdash; underwritten for room count, not bedrooms.</p>
      </div>
      <div class="roles">
        <span class="who">You handle</span>
        <h3>The renovation</h3>
        <p>You already do this. We give you the scope, the standard to build to, and coaching through the parts that differ from a retail flip.</p>
      </div>
      <div class="roles">
        <span class="who">We handle</span>
        <h3>The exit</h3>
        <p>We bring the buyer. You aren't listing into a retail market and hoping &mdash; you know who the property is for before you open a wall.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Two ways in</h2>
    <p>The model has two sides. Operators build the houses. Investors buy them. Both sides are qualified before we put a deal in front of anyone.</p>
    <div class="doors">
      <div class="door">
        <div class="who">If you build</div>
        <h3>Build one of our houses</h3>
        <p>You have completed renovations and a crew. We source the deal, coach you through the conversion, and bring the buyer at the end. You run the job.</p>
        <p style="opacity:.75;font-size:.95rem"><b>Requires:</b> completed projects, capital, an Arizona property.</p>
        <div class="cta-row">
          <a class="btn" href="how-it-works.html">See how the program works</a>
        </div>
      </div>
      <div class="door buy">
        <div class="who">If you buy</div>
        <h3>Buy a finished property</h3>
        <p>You want a co-living property that's already converted, furnished, and built to standard &mdash; without running the renovation yourself. We qualify buyers ahead of inventory.</p>
        <p style="opacity:.75;font-size:.95rem"><b>Requires:</b> proof of funds or financing in place.</p>
        <div class="cta-row">
          <a class="btn" href="for-buyers.html">Get on the buyer list</a>
        </div>
      </div>
    </div>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- how it works
PAGES["how-it-works.html"] = dict(
title="How it works — Green Light Buying Machine",
desc="Ten stages from qualification to buyer placement, and exactly which parts we handle and which parts you do.",
main=phead("The program", "How it works",
  "Ten stages from qualification to buyer placement. You run the renovation. We handle the two hardest parts &mdash; finding the deal and finding the buyer.") + """

<section>
  <div class="wrap">
    <h2>The division of labor</h2>
    <p>Most education sells you information and wishes you luck. This is closer to a joint venture with training attached: we take on the parts that sink first-time conversions, and you do the part you're already good at.</p>
    <div class="split thirds" style="margin-top:2.5rem">
      <div class="roles">
        <span class="who">We handle</span>
        <h3>Deal sourcing</h3>
        <p>Properties are brought to you already screened for co-living use and underwritten on rentable rooms rather than bedroom count.</p>
      </div>
      <div class="roles">
        <span class="who">You handle</span>
        <h3>Execution</h3>
        <p>Your crew, your schedule, your budget &mdash; built to a defined co-living standard with review at set checkpoints.</p>
      </div>
      <div class="roles">
        <span class="who">We handle</span>
        <h3>Buyer placement</h3>
        <p>The exit is arranged rather than hoped for. You know the buyer profile before the first wall goes up.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Ten stages, start to close</h2>
    <p>Every student runs the same sequence, tracked in your portal so you always know what's next and what's waiting on you. <span class="todo">Confirm stage names against the real pipeline.</span></p>
    <ol class="stages">
      <li><div><b>Qualification</b><span>We confirm your experience, capital, and capacity before you enroll.</span></div></li>
      <li><div><b>Market brief</b><span>Where co-living works in the Valley, and why &mdash; submarket by submarket.</span></div></li>
      <li><div><b>Deal sourced</b><span>We bring you a property screened for shared-housing use.</span></div></li>
      <li><div><b>Room-count underwriting</b><span>Pricing a house on rentable rooms instead of bedrooms.</span></div></li>
      <li><div><b>Offer and close</b><span>Structuring and acquiring the property.</span></div></li>
      <li><div><b>Scope and design</b><span>Floor plan, partition strategy, and finish standard.</span></div></li>
      <li><div><b>Renovation</b><span>Your crew executes. We review at defined checkpoints.</span></div></li>
      <li><div><b>Standards inspection</b><span>The property is checked against operator requirements before listing.</span></div></li>
      <li><div><b>Furnish and stage</b><span>Getting the house ready to produce income on day one.</span></div></li>
      <li><div><b>Buyer placement</b><span>We bring the buyer and you close.</span></div></li>
    </ol>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>What you get</h2>
    <div class="split" style="margin-top:2rem">
      <ul class="plain">
        <li>A place in an Arizona cohort</li>
        <li>Direct coaching from Brian and Gina Kingdeski</li>
        <li>Deals sourced and brought to you</li>
        <li>Buyer placement on completed projects</li>
      </ul>
      <ul class="plain">
        <li>The full course library and module handouts</li>
        <li>A student portal tracking your deal through all ten stages</li>
        <li>Renovation scope and co-living build standards</li>
        <li>A copy of <i>The Green Light Buying Machine</i></li>
      </ul>
    </div>
    <p class="todo" style="margin-top:1.5rem">Add enrollment terms and price here once Brian and Gina decide how public to be about the number.</p>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- fit
PAGES["is-it-for-you.html"] = dict(
title="Is it for you — Green Light Buying Machine",
desc="An honest fit list for the program: who it works for, who it doesn't, and what we expect from students.",
main=phead("Before you apply", "Is it for you?",
  "This isn't a starter program. Being honest about that up front saves everyone a hard conversation three weeks in.") + """

<section>
  <div class="wrap">
    <div class="fit">
      <div class="col">
        <h3>A fit if you</h3>
        <ul>
          <li>Have finished renovations you can point to</li>
          <li>Run your own crew or have trades you trust</li>
          <li>Can read a scope and hold a budget</li>
          <li>Have capital or reliable access to it</li>
          <li>Want a different exit, not a different hobby</li>
          <li>Can work an Arizona property</li>
        </ul>
      </div>
      <div class="col not">
        <h3>Not a fit if you</h3>
        <ul>
          <li>Haven't completed a renovation yet</li>
          <li>Are looking for passive income</li>
          <li>Want to assign the contract instead of building</li>
          <li>Need someone else to manage the build</li>
          <li>Are shopping for a guarantee</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>What we expect from you</h2>
    <div class="split" style="margin-top:2rem">
      <ul class="plain">
        <li>You build to the standard, not to your usual retail spec</li>
        <li>You keep the portal current so we can see where the deal stands</li>
        <li>You raise problems early, while they're still cheap</li>
      </ul>
      <ul class="plain">
        <li>You show up to cohort calls</li>
        <li>You make decisions on your own project &mdash; we advise, you own it</li>
      </ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Straight answers</h2>
    <div class="qa">
      <h3>Do I have to use your deal?</h3>
      <p>No. Bring your own if you have one &mdash; we'll underwrite it with you. Sourcing is there because finding the right house is the part most people get wrong, not because it's mandatory. <span class="todo">Confirm this is accurate.</span></p>
    </div>
    <div class="qa">
      <h3>What if the renovation goes sideways?</h3>
      <p>It's your project and your capital, so the risk is real. What the program changes is that you have people who have done this before looking at the same problem, and checkpoints designed to catch trouble before it compounds.</p>
    </div>
    <div class="qa">
      <h3>Is the buyer guaranteed?</h3>
      <p><span class="todo">Answer this precisely with Brian and Gina, and have counsel review the wording.</span> Buyer placement is a core part of the model, and how it's described here needs to match exactly what's contractually promised.</p>
    </div>
    <div class="qa">
      <h3>Do I have to be in Arizona?</h3>
      <p>You don't have to live here, but the property does. Cohorts are Arizona-based and the deals we source are in this market.</p>
    </div>
    <div class="qa">
      <h3>How long does one project take?</h3>
      <p><span class="todo">Add a realistic range from completed student projects.</span></p>
    </div>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- book
PAGES["the-book.html"] = dict(
title="The Green Light Buying Machine — the book, coming soon",
desc="The book by Brian and Gina Kingdeski laying out the co-living conversion model. Join the list to hear when it's out.",
main=phead("Coming soon", "The Green Light Buying Machine",
  "The whole model in print. It isn't out yet &mdash; put your name down and we'll tell you the day it is.") + """

<section>
  <div class="wrap">
    <div class="book">
      <div class="cover">
        <div class="bar"></div>
        <div><div class="t">The Green Light Buying Machine</div></div>
        <div>
          <div class="soon">Coming soon</div>
          <div class="a">Brian &amp; Gina Kingdeski</div>
        </div>
      </div>
      <div>
        <p>Brian and Gina Kingdeski are writing down what they've been teaching in cohorts: how co-living conversions are underwritten, where the margin actually comes from, and what separates a house that works from one that only looks like it does.</p>
        <p>It isn't a motivational book. It's the model, the math, and the mistakes &mdash; written for people who already know how to run a job site and want to know whether this exit is worth their next project.</p>
        <p><span class="todo">Swap the placeholder cover for the real KDP art at 300 DPI or better, and add the retail link on launch.</span></p>

        <h3 style="margin-top:2rem">Hear when it's out</h3>
        <p style="margin-bottom:1.25rem">No sequence, no drip. One email when the book is available.</p>
        <form class="js-form" action="/api/book-waitlist" method="post" novalidate
              data-source="book waitlist"
              data-sending="Adding you&#8230;"
              data-success="You&#8217;re on the list. We&#8217;ll email you the day it&#8217;s out.">
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="pair">
            <div class="field">
              <label for="wl-name">Your name</label>
              <input id="wl-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="wl-email">Email</label>
              <input id="wl-email" name="email" type="email" autocomplete="email" required>
            </div>
          </div>
          <button class="submit" type="submit">Put me on the list</button>
        </form>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>What it covers</h2>
    <p class="todo">Pull six to eight real chapter titles from the manuscript once it's final. Specific chapter names sell a pre-launch book far better than a description does.</p>
    <div class="split" style="margin-top:1.5rem">
      <ul class="plain">
        <li>Why the retail exit keeps getting harder</li>
        <li>What makes a house convertible</li>
        <li>Underwriting on rooms instead of bedrooms</li>
      </ul>
      <ul class="plain">
        <li>Designing the partition plan</li>
        <li>Building to operator standard</li>
        <li>Who buys a finished co-living property</li>
      </ul>
    </div>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- about
PAGES["about.html"] = dict(
title="About Brian and Gina Kingdeski — Green Light Buying Machine",
desc="The people behind the Green Light Buying Machine co-living program in Arizona.",
main=phead("Who runs this", "Brian and Gina Kingdeski",
  "The program is small on purpose. You work with the people whose names are on the book.") + """

<section>
  <div class="wrap">
    <div class="book">
      <div class="portrait">photo of Brian and Gina<br>4:5 &#183; 1200&#215;1500 min</div>
      <div>
        <p class="todo">This page needs real biography. Everything below is scaffolding &mdash; replace it before launch.</p>
        <p>Brian and Gina Kingdeski run the Green Light Buying Machine, an Arizona program that takes experienced fix-and-flippers into co-living conversions. They wrote <i>The Green Light Buying Machine</i> and teach the model directly to each cohort.</p>
        <p><span class="todo">Add: how many projects, how long in the market, what they were doing before, and why they moved to co-living.</span> The one thing this page has to establish is that they've done what they're teaching &mdash; specifics are what make that believable.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Why we teach it this way</h2>
    <div class="split" style="margin-top:2rem">
      <div>
        <p>Most real estate education is sold to people with no experience, because that's the biggest audience. It's also why so much of it doesn't work &mdash; you can't teach someone to run a renovation in a video course.</p>
      </div>
      <div>
        <p>We went the other direction. We only take people who can already build, then we solve what they're actually missing: which houses convert, what standard to build to, and who buys the finished product.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Students say</h2>
    <p class="todo">Add two or three testimonials from students who have closed. Ask each for the before and after: what their retail exit looked like, and what the co-living deal did. Specific numbers beat adjectives, and this audience spots a vague quote immediately.</p>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- apply
PAGES["apply.html"] = dict(
title="Get a deal analyzed — Green Light Buying Machine",
desc="Send us an Arizona property and we'll tell you whether it converts to co-living, what room count it supports, and what the conversion involves.",
main=phead("No charge", "Send us a property",
  "We'll tell you whether it converts, roughly what room count it supports, and what the conversion would involve. If it's a no, we'll tell you why it's a no.") + """

<section>
  <div class="wrap">
    <div class="split">
      <div>
        <form class="js-form" action="/api/deal-analysis" method="post" novalidate
              data-source="website deal analysis"
              data-sending="Sending your property&#8230;"
              data-success="Got it. We&#8217;ll come back to you with an answer on this property, usually within a few days.">
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="pair">
            <div class="field">
              <label for="name">Your name</label>
              <input id="name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="address">Property address</label>
            <input id="address" name="address" type="text" required>
            <p class="hint">Arizona properties only. An MLS or Zillow link works too.</p>
          </div>
          <div class="pair">
            <div class="field">
              <label for="price">Asking or contract price</label>
              <input id="price" name="price" type="text">
            </div>
            <div class="field">
              <label for="specs">Beds, baths, square footage</label>
              <input id="specs" name="specs" type="text" placeholder="3 / 2 / 1,650">
            </div>
          </div>
          <div class="field">
            <label for="experience">Renovations you've completed</label>
            <select id="experience" name="experience">
              <option value="">Select one</option>
              <option>None yet</option>
              <option>1 to 3</option>
              <option>4 to 10</option>
              <option>More than 10</option>
            </select>
          </div>
          <div class="field">
            <label for="notes">Anything else we should know</label>
            <textarea id="notes" name="notes"></textarea>
          </div>
          <button class="submit" type="submit">Send the property</button>
        </form>
      </div>
      <div>
        <h3 style="margin-bottom:1rem">What happens next</h3>
        <ul class="plain">
          <li>You send the address</li>
          <li>We run the layout and the numbers</li>
          <li>You get a written answer, usually within a few days</li>
          <li>If it works and you want in, we talk about the cohort</li>
        </ul>
        <h3 style="margin:2rem 0 1rem">Not ready for that</h3>
        <p>Read <a href="is-it-for-you.html">the fit list</a> first, or get on the list for <a href="the-book.html">the book</a>. Neither costs you anything and both will tell you more than a sales call would.</p>
      </div>
    </div>
  </div>
</section>""")


# ---------------------------------------------------------------- buyers
PAGES["for-buyers.html"] = dict(
title="Buy a finished co-living property — Green Light Buying Machine",
desc="Qualified investors get first look at Arizona co-living properties, converted and built to operator standard.",
main=phead("For investors", "Buy a finished property",
  "Converted, furnished, and built to standard. You didn't run the renovation and you don't have to fix what someone else got wrong.") + """

<section>
  <div class="wrap">
    <h2>What you're actually buying</h2>
    <div class="split">
      <div>
        <p>A single-family house in the Valley, reconfigured into individually rented rooms with shared kitchen and living space. Built to the standard co-living operators require rather than to whatever a contractor thought was close enough.</p>
        <p>Every property in our inventory was renovated by an operator inside our program, to a scope we set, with review at defined checkpoints. That's the difference between this and buying somebody's first attempt at a room conversion.</p>
      </div>
      <div>
        <p><span class="todo">Specify exactly what conveys: furnished or unfurnished, management in place or not, tenants placed or vacant at close, and any warranty on the work. Buyers will ask on the first call, and the answer belongs on this page.</span></p>
        <p><span class="todo">If there is a listing or referral fee to the buyer, disclose it here.</span></p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>How it works</h2>
    <ol class="stages">
      <li><div><b>You get qualified</b><span>Short conversation about your criteria, timeline, and how you're funding the purchase.</span></div></li>
      <li><div><b>You go on the list</b><span>Qualified buyers see properties before they're marketed anywhere else.</span></div></li>
      <li><div><b>We send matches</b><span>Address, scope, room count, and the numbers, as properties come available.</span></div></li>
      <li><div><b>You tour and diligence</b><span>Your inspector, your lender, your timeline. We don't rush this part.</span></div></li>
      <li><div><b>You close</b><span>On a property that was built to be exactly what it is.</span></div></li>
    </ol>
    <p style="margin-top:2rem"><span class="todo">Confirm this sequence with Brian and Gina, especially whether buyers are matched before or after a property is under renovation.</span></p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Who we can work with</h2>
    <div class="fit">
      <div class="col">
        <h3>A fit if you</h3>
        <ul>
          <li>Have cash or financing already arranged</li>
          <li>Are buying to hold, not to resell quickly</li>
          <li>Understand shared housing is operationally different from a single-tenant rental</li>
          <li>Can move on a timeline when the right property comes up</li>
        </ul>
      </div>
      <div class="col not">
        <h3>Not a fit if you</h3>
        <ul>
          <li>Are still deciding whether to invest at all</li>
          <li>Need seller financing we don't offer</li>
          <li>Want a guaranteed return</li>
          <li>Expect a hands-off asset with no management decisions</li>
        </ul>
      </div>
    </div>
    <p style="margin-top:2rem;opacity:.8;font-size:.95rem">Co-living properties produce income from multiple rooms, which means vacancy, turnover, and management work differently than they do on a standard rental. We'll walk you through how before you buy, not after.</p>
  </div>
</section>

<section class="band" id="qualify">
  <div class="wrap">
    <div class="split">
      <div>
        <h2>Get on the buyer list</h2>
        <p>Tell us what you're looking for and how you're funding it. If it's a fit, you'll hear from us when something matches &mdash; usually before it's listed anywhere.</p>
        <form class="js-form" action="/api/buyer-inquiry" method="post" novalidate
              data-source="buyer list"
              data-sending="Sending&#8230;"
              data-success="Got it. We&#8217;ll be in touch to talk through what you&#8217;re looking for.">
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="pair">
            <div class="field">
              <label for="b-name">Your name</label>
              <input id="b-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="b-phone">Phone</label>
              <input id="b-phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="b-email">Email</label>
            <input id="b-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="pair">
            <div class="field">
              <label for="b-funding">How you'd fund a purchase</label>
              <select id="b-funding" name="funding" required>
                <option value="">Select one</option>
                <option>Cash</option>
                <option>Conventional or DSCR financing</option>
                <option>1031 exchange</option>
                <option>Partnership or fund</option>
                <option>Still figuring it out</option>
              </select>
            </div>
            <div class="field">
              <label for="b-timeline">Timeline</label>
              <select id="b-timeline" name="timeline" required>
                <option value="">Select one</option>
                <option>Ready now</option>
                <option>Next 3 months</option>
                <option>3 to 6 months</option>
                <option>Just researching</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="b-portfolio">Rentals you own now</label>
            <select id="b-portfolio" name="portfolio">
              <option value="">Select one</option>
              <option>None yet</option>
              <option>1 to 3</option>
              <option>4 to 10</option>
              <option>More than 10</option>
            </select>
          </div>
          <div class="field">
            <label for="b-notes">What you're looking for</label>
            <textarea id="b-notes" name="notes" placeholder="Area, budget range, anything else worth knowing."></textarea>
          </div>
          <button class="submit" type="submit">Get on the list</button>
        </form>
      </div>
      <div>
        <h3 style="margin-bottom:1rem">What happens next</h3>
        <ul class="plain">
          <li>We read what you sent</li>
          <li>A short call to understand your criteria</li>
          <li>You go on the qualified list</li>
          <li>You hear from us when a property matches</li>
        </ul>
        <p style="margin-top:2rem;font-size:.95rem;opacity:.8">We don't sell or share this list, and we won't send you properties that don't fit what you told us.</p>
      </div>
    </div>
  </div>
</section>""")

for filename, page in PAGES.items():
    html = (SHELL
            .replace("{{TITLE}}", page["title"])
            .replace("{{DESC}}", page["desc"])
            .replace("{{CSS}}", CSS)
            .replace("{{NAV}}", nav(filename))
            .replace("{{MAIN}}", page["main"])
            .replace("{{FOOTER}}", FOOTER))
    with open(os.path.join(OUT, filename), "w") as f:
        f.write(html)
    print(filename, len(html), "bytes")
