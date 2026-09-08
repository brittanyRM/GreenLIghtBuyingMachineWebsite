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
  .hero-plan{background:#fff;border:1px solid rgba(232,231,224,.3);padding:.75rem;
    aspect-ratio:auto;display:block}
  .hero-plan img{width:100%;height:auto;object-fit:contain;background:#fff}
  .hero-plan::after{content:"";position:absolute;inset:.35rem;
    border:1px solid rgba(16,28,34,.12);pointer-events:none}

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

  .stats{display:grid;gap:1.5rem;grid-template-columns:repeat(3,minmax(0,1fr));
    padding-block:clamp(2.25rem,4vw,3.25rem)}
  .stat .n{font-family:var(--display);font-weight:800;letter-spacing:-.03em;
    font-size:clamp(2.1rem,1.4rem + 3vw,3.6rem);line-height:1;color:var(--green-bright)}
  .stat .l{font-family:var(--display);font-weight:600;font-size:.82rem;letter-spacing:.02em;
    opacity:.75;margin-top:.5rem}

  .grid-plans,.grid-homes{display:grid;gap:.75rem;margin-top:1.75rem}
  .grid-plans{grid-template-columns:repeat(2,minmax(0,1fr))}
  .grid-homes{grid-template-columns:repeat(2,minmax(0,1fr))}
  @media(min-width:44rem){.grid-plans{grid-template-columns:repeat(3,minmax(0,1fr))}
    .grid-homes{grid-template-columns:repeat(3,minmax(0,1fr))}}
  @media(min-width:66rem){.grid-homes{grid-template-columns:repeat(4,minmax(0,1fr))}}
  .shot{margin:0;position:relative;overflow:hidden;border:1px solid var(--rule);
    background:var(--paper-dim);cursor:zoom-in;padding:0}
  .band .shot{border-color:rgba(232,231,224,.25)}
  .shot img{width:100%;height:100%;object-fit:cover;display:block;
    transition:transform .35s ease;background:#fff}
  .grid-homes .shot{aspect-ratio:4/3}
  .grid-plans .shot{aspect-ratio:4/3}
  .grid-plans .shot img{object-fit:contain;background:#fff}
  .shot:hover img,.shot:focus-visible img{transform:scale(1.04)}
  @media(prefers-reduced-motion:reduce){.shot img{transition:none}
    .shot:hover img,.shot:focus-visible img{transform:none}}
  .shot figcaption{position:absolute;left:0;right:0;bottom:0;padding:.5rem .7rem;
    font-family:var(--plan);font-size:.72rem;color:#fff;
    background:linear-gradient(to top,rgba(16,28,34,.85),rgba(16,28,34,0));
    opacity:0;transition:opacity .25s ease}
  .shot:hover figcaption,.shot:focus-visible figcaption{opacity:1}
  .grid-plans .shot figcaption{opacity:1;background:linear-gradient(to top,rgba(16,28,34,.8),rgba(16,28,34,0))}

  .lightbox{position:fixed;inset:0;background:rgba(16,28,34,.95);z-index:99;
    display:none;align-items:center;justify-content:center;padding:clamp(1rem,4vw,3rem)}
  .lightbox[open],.lightbox.open{display:flex}
  .lightbox img{max-width:100%;max-height:88vh;object-fit:contain;background:#fff}
  .lightbox .close{position:absolute;top:1rem;right:1.25rem;background:none;border:0;
    color:var(--paper);font-size:2.5rem;line-height:1;cursor:pointer;padding:.25rem .5rem}
  .lightbox .cap{position:absolute;bottom:1.25rem;left:0;right:0;text-align:center;
    font-family:var(--plan);font-size:.8rem;color:var(--paper);opacity:.8}

  .embed{background:#fff;border:1px solid var(--rule);padding:.5rem;margin-top:1.5rem}
  .embed iframe{width:100%;min-height:800px;border:0;display:block}

  .steps2{display:grid;gap:1.5rem;grid-template-columns:1fr;margin-top:2rem}
  @media(min-width:52rem){.steps2{grid-template-columns:repeat(2,minmax(0,1fr))}}
  .stepbox{border:1px solid var(--rule);border-top:4px solid var(--green);
    padding:clamp(1.5rem,3vw,2rem)}
  .band .stepbox{border-color:rgba(232,231,224,.3);border-top-color:var(--green-bright)}
  .stepbox .n{font-family:var(--plan);font-size:.75rem;letter-spacing:.08em;
    color:var(--green);margin-bottom:.75rem}
  .band .stepbox .n{color:var(--green-bright)}
  .stepbox p{max-width:none}

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

PLAN_SVG = r"""<svg class="plan" viewBox="0 0 720 460" role="img" aria-labelledby="plantitle">
  <title id="plantitle">Floor plan of a single-family house redivided into ten named bedrooms around a shared kitchen, living room and laundry.</title>
  <rect class="sheet" x="6" y="6" width="708" height="448"/>
  <rect class="shell" x="26" y="30" width="668" height="380"/>
  <line class="keep" x1="170" y1="30" x2="170" y2="410"/>
  <line class="keep" x1="485" y1="30" x2="485" y2="410"/>
  <line class="new" x1="170" y1="200" x2="694" y2="200" style="--len:524;--d:.25s"/>
  <line class="new" x1="170" y1="240" x2="694" y2="240" style="--len:524;--d:.35s"/>
  <line class="new" x1="275" y1="30"  x2="275" y2="200" style="--len:170;--d:.55s"/>
  <line class="new" x1="380" y1="30"  x2="380" y2="200" style="--len:170;--d:.62s"/>
  <line class="new" x1="590" y1="30"  x2="590" y2="200" style="--len:170;--d:.69s"/>
  <line class="new" x1="275" y1="240" x2="275" y2="410" style="--len:170;--d:.76s"/>
  <line class="new" x1="380" y1="240" x2="380" y2="410" style="--len:170;--d:.83s"/>
  <line class="new" x1="590" y1="240" x2="590" y2="410" style="--len:170;--d:.9s"/>
  <g class="tag" text-anchor="middle" font-size="13">
    <text class="fade" style="--d:1.15s" x="222" y="120">Blue</text>
    <text class="fade" style="--d:1.19s" x="327" y="120">Green</text>
    <text class="fade" style="--d:1.23s" x="432" y="120">Yellow</text>
    <text class="fade" style="--d:1.27s" x="537" y="120">Orange</text>
    <text class="fade" style="--d:1.31s" x="642" y="120">Violet</text>
    <text class="fade" style="--d:1.35s" x="222" y="335">Indigo</text>
    <text class="fade" style="--d:1.39s" x="327" y="335">Gold</text>
    <text class="fade" style="--d:1.43s" x="432" y="335">Silver</text>
    <text class="fade" style="--d:1.47s" x="537" y="335">Bronze</text>
    <text class="fade" style="--d:1.51s" x="642" y="335">Brass</text>
  </g>
  <text class="note fade" style="--d:1.65s" x="360" y="226" text-anchor="middle">shared hall</text>
  <text class="fade" style="--d:1.65s" transform="translate(105,310) rotate(-90)" font-size="13">kitchen &#183; living &#183; laundry</text>
  <text class="note fade" style="--d:1.8s" x="26" y="440">existing walls</text>
  <text class="tag fade" style="--d:1.8s" x="170" y="440">new walls</text>
</svg>"""


PLANS = [
    ("plan-ash", "Ash &#183; 8 bedrooms, 7 bathrooms"),
    ("plan-colors", "Ten bedrooms named by colour, around a shared kitchen and living room"),
    ("plan-ten-room", "Ten-room conversion, 2,011 sq ft"),
    ("plan-harmony", "Harmony &#183; 2,074 sq ft"),
    ("plan-rooms", "Ten bedrooms, 1,926 sq ft"),
    ("plan-pepper", "Pepper &#183; 1,863 sq ft"),
]

HOMES = [
    ("kitchen-navy", "Shared kitchen"),
    ("common-green", "Common area"),
    ("kitchen-green", "Shared kitchen"),
    ("dining-bar", "Dining and living"),
    ("living-open", "Living room"),
    ("common-seating", "Common seating"),
    ("bedroom-eight", "Room 8"),
    ("bedroom-yellow", "Bedroom"),
    ("bedroom-desert", "Bedroom"),
    ("bedroom-two", "Bedroom"),
    ("harmony-kitchen", "Harmony &#183; kitchen"),
    ("harmony-common", "Harmony &#183; common area"),
    ("pepper-kitchen", "Pepper &#183; kitchen"),
    ("pepper-common", "Pepper &#183; common area"),
    ("howe-kitchen", "Howe &#183; kitchen"),
    ("howe-bedroom", "Howe &#183; bedroom"),
    ("laundry", "Shared laundry"),
]

def shots(items, folder, limit=None):
    out = ""
    for slug, alt in (items[:limit] if limit else items):
        out += ('<figure class="shot" data-full="images/%s/%s.jpg">'
                '<img src="images/%s/%s-thumb.jpg" alt="%s" loading="lazy" decoding="async">'
                '<figcaption>%s</figcaption></figure>\n' % (folder, slug, folder, slug, alt, alt))
    return out

STATS = """<section class="band">
  <div class="wrap">
    <div class="stats">
      <div class="stat"><div class="n">450+</div><div class="l">Doors produced</div></div>
      <div class="stat"><div class="n">26+</div><div class="l">Years in the trades</div></div>
      <div class="stat"><div class="n">AZ</div><div class="l">Built and sold in the Valley</div></div>
    </div>
  </div>
</section>"""

NAVLINKS = [
    ("index.html", "Home"),
    ("how-it-works.html", "Build with us"),
    ("for-buyers.html", "Buy a property"),
    ("homes.html", "Homes we've built"),
    ("faq.html", "FAQ"),
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
    <a class="btn" href="apply.html">Become a student</a>
  </div>
</nav>""" % items

FOOTER = """<footer>
  <div class="wrap">
    <div>
      <h4>Green Light Buying Machine</h4>
      <p class="fine" style="margin:0 0 .6rem">The infrastructure behind certified co-living assets.</p>
      <p style="margin:0"><a href="mailto:info@greenlightbuyingmachine.com">info@greenlightbuyingmachine.com</a></p>
    </div>
    <div>
      <h4>Pages</h4>
      <ul>
        <li><a href="how-it-works.html">Build with us</a></li>
        <li><a href="is-it-for-you.html">Is the program for you</a></li>
        <li><a href="for-buyers.html">Buy a finished property</a></li>
        <li><a href="homes.html">Homes we&#8217;ve built</a></li>
        <li><a href="faq.html">FAQ</a></li>
        <li><a href="the-book.html">The book</a></li>
        <li><a href="about.html">About</a></li>
        <li><a href="apply.html">Apply to become a student</a></li>
        <li><a href="submit-a-property.html">Submit a property</a></li>
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

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged image">
  <button class="close" id="lightboxClose" aria-label="Close">&times;</button>
  <img id="lightboxImg" src="" alt="">
  <div class="cap" id="lightboxCap"></div>
</div>

<script>
/* Gallery lightbox. Thumbnails carry the full-size path in data-full so the
   grid stays light and the big file only loads when someone asks for it. */
(function () {
  var box = document.getElementById('lightbox');
  var img = document.getElementById('lightboxImg');
  var cap = document.getElementById('lightboxCap');
  var shots = document.querySelectorAll('.shot');
  if (!shots.length) return;
  var last = null;

  function open(shot) {
    var thumb = shot.querySelector('img');
    last = shot;
    img.src = shot.dataset.full || thumb.src;
    img.alt = thumb.alt;
    cap.textContent = thumb.alt;
    box.classList.add('open');
    document.getElementById('lightboxClose').focus();
  }
  function close() {
    box.classList.remove('open');
    img.src = '';
    if (last) last.focus();
  }

  Array.prototype.forEach.call(shots, function (shot) {
    shot.setAttribute('tabindex', '0');
    shot.setAttribute('role', 'button');
    shot.addEventListener('click', function () { open(shot); });
    shot.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(shot); }
    });
  });
  document.getElementById('lightboxClose').addEventListener('click', close);
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && box.classList.contains('open')) close();
  });
})();
</script>

<script>
/* Handles every form marked .js-form. Posts JSON to the form's action,
   which forwards to GoHighLevel server-side. Messages come from data
   attributes on the form so each one can speak for itself. */
(function () {
  var FALLBACK = 'info@greenlightbuyingmachine.com';

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
    <h2>Think you're a fit? Tell us about your work.</h2>
    <p>We're looking for operators with 10 to 15 flips behind them and a crew already running. Send us your background and we'll tell you straight whether the program makes sense for you right now.</p>
    <div class="cta-row">
      <a class="btn" href="apply.html">Apply to become a student</a>
      <a class="btn ghost" href="is-it-for-you.html">Read the fit list first</a>
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
        <h1 style="font-size:clamp(2.9rem,1.5rem + 6vw,5.6rem)">One house.<br>Eight doors.</h1>
        <p class="lede">Institutional-grade deal flow for PadSplit investors. The Green Light Way underwrites Arizona houses by the room &mdash; so operators build the right conversion and investors buy a finished one.</p>
        <div class="cta-row">
          <a class="btn" href="how-it-works.html">I build</a>
          <a class="btn ghost" href="for-buyers.html">I buy</a>
        </div>
      </div>
      <div>
        <figure class="shot hero-plan" data-full="images/plans/plan-ash.jpg">
          <img src="images/plans/plan-ash.jpg" alt="Floor plan of the Ash conversion: eight bedrooms and seven bathrooms around a shared kitchen, great room, dining area and second sitting area">
        </figure>
        <p class="plan-cap">Ash &#183; 8 bedrooms, 7 baths. Nearly every room ensuite.</p>
      </div>
    </div>
  </div>
</header>

""" + STATS + """

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
    <h2>What a finished one looks like</h2>
    <p>Not renderings. Houses we&#8217;ve converted, furnished, and put into service.</p>
    <div class="grid-homes">
""" + shots(HOMES, "homes", 8) + """</div>
    <div class="cta-row">
      <a class="btn ghost" href="homes.html">See all the homes and floor plans</a>
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
        <p>Same as any flip &mdash; you buy it, finance it, run your crew. We bring the deal flow, hold you to the standard, and identify your buyer while you're still building.</p>
        <p style="opacity:.75;font-size:.95rem"><b>Requires:</b> 10&#8211;15 completed flips, your own crew, your own capital.</p>
        <div class="cta-row">
          <a class="btn" href="how-it-works.html">See how the program works</a>
        </div>
      </div>
      <div class="door buy">
        <div class="who">If you buy</div>
        <h3>Buy a finished property</h3>
        <p>Converted, furnished, and launched on PadSplit &mdash; without running the renovation yourself. We qualify buyers ahead of inventory so we can match early.</p>
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
    <h2>It's a flip. The exit is what changes.</h2>
    <p>You buy the distressed house and finance it the way you always do &mdash; first, second, hard money, your usual stack. You run your crew, you hold the budget, you own the risk. Nothing about the acquisition or the buildout is unfamiliar.</p>
    <p>What changes is who you sell to. A retail buyer prices your house against comps down the street. A co-living investor prices it against what the finished house produces by the room, and that's a different number. You're buying for the potential the property will have, and selling to someone who's paying for exactly that.</p>
    <p>The other change is that we're identifying your buyer while you're still working. You're not listing and hoping.</p>
    <div class="split thirds" style="margin-top:2.5rem">
      <div class="roles">
        <span class="who">We bring</span>
        <h3>Deal flow</h3>
        <p>Distressed wholesale properties, already underwritten the Green Light way &mdash; on rentable rooms rather than bedroom count.</p>
      </div>
      <div class="roles">
        <span class="who">You own</span>
        <h3>The whole buildout</h3>
        <p>You buy it, you finance it, you run your crew. We hand-hold the build to make sure it hits the standard our buyers expect &mdash; because your exit depends on it.</p>
      </div>
      <div class="roles">
        <span class="who">We bring</span>
        <h3>The buyer</h3>
        <p>We guarantee to present your finished house to our qualified buyer list &mdash; investors who've bought from us before and are waiting on the next one. Whether one of them buys yours depends on the house and the market.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>The Green Light Way</h2>
    <p style="margin-bottom:2rem"><b>The floor is eight bedrooms and two bathrooms.</b> We don't build below it, because room count is where the economics come from. Everything above that floor is a decision the numbers make for you.</p>
    <div class="split">
      <div>
        <p>Bedrooms don't tell you what a co-living house is worth. Rentable rooms do &mdash; and not every room is worth the same. PadSplit reports what rooms actually rent for by submarket, and a room with its own ensuite bathroom prices differently than one sharing down the hall.</p>
        <p>That turns bathroom count into an underwriting decision rather than a finish preference. We run that math on distressed inventory before anyone walks a property, so students see houses already screened for room count, ensuite potential, and margin instead of guessing at a listing.</p>
      </div>
      <div>
        <p>It's also why we start from scratch rather than converting an existing rental. Adding bathrooms is the kind of thing you can only plan from the first wall &mdash; retrofit it later and you're working around plumbing that was never meant to be there.</p>
        <p>That's the Green Light Way: buy on what the house can become, build it to the standard the buyer expects, and know who that buyer is before you finish. The margin lives in the specific deal, not in an average we could print here.</p>
      </div>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Financing that already understands the asset</h2>
    <div class="split" style="margin-top:1.5rem">
      <div>
        <p>Rachelle Coffey is the lender we work with, and she finances PadSplit conversions specifically &mdash; both the acquisition side for operators and the purchase side for buyers.</p>
      </div>
      <div>
        <p>That matters more than it sounds. A lender who prices this asset on room income rather than residential comps removes the friction that stalls these deals at the appraisal.</p>
        <p><a href="https://go.homeownersfg.com/home/rachelle-coffey" target="_blank" rel="noopener noreferrer">Talk to Rachelle &rarr;</a></p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Ten stages, start to close</h2>
    <p>Every student runs the same sequence, tracked in your portal so you always know what's next and what's waiting on you.</p>
    <ol class="stages">
      <li><div><b>Qualification</b><span>We confirm your experience, capital, and capacity before you enroll.</span></div></li>
      <li><div><b>Market brief</b><span>Where co-living works in the Valley, and why &mdash; submarket by submarket.</span></div></li>
      <li><div><b>Deal sourced</b><span>We bring you a property already screened for co-living use and room count.</span></div></li>
      <li><div><b>Room-count underwriting</b><span>Pricing a house on rentable rooms instead of bedrooms.</span></div></li>
      <li><div><b>You buy it</b><span>Your offer, your financing, your name on the deed.</span></div></li>
      <li><div><b>Scope and design</b><span>Floor plan, partition strategy, and finish standard.</span></div></li>
      <li><div><b>Renovation</b><span>Your crew executes. We hand-hold to the standard and review at checkpoints.</span></div></li>
      <li><div><b>Standards inspection</b><span>The property is checked against operator requirements before listing.</span></div></li>
      <li><div><b>Furnish and launch</b><span>We furnish the house and get it live on PadSplit, ready to produce income on day one.</span></div></li>
      <li><div><b>You sell</b><span>We bring the buyer we've been working to line up while you built.</span></div></li>
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
        <li>Your finished house presented to our qualified buyer list</li>
      </ul>
      <ul class="plain">
        <li>The full course library and module handouts</li>
        <li>A student portal tracking your deal through all ten stages</li>
        <li>Renovation scope and co-living build standards</li>
        <li>A copy of <i>The Green Light Buying Machine</i> when it publishes</li>
      </ul>
    </div>
    <div class="stepbox" style="margin-top:2.5rem;border-top-color:var(--green)">
      <div class="n">BECOMING A STUDENT</div>
      <h3 style="font-size:clamp(1.3rem,1.1rem + .8vw,1.75rem);font-weight:800">$15,000, once you're accepted</h3>
      <p>You apply first. We review your background, and if it's a fit we talk. Payment comes after you're accepted &mdash; not before, and not as a way in.</p>
      <p style="margin-bottom:0">As a student you get access to everything: we walk you through every step, from the first deal we bring you to the buyer at the end. The full curriculum, the coaching, the deal flow, the standards, the buyer side. It doesn't include the house &mdash; you buy and finance that yourself, the way you would any flip.</p>
    </div>
  </div>
</section>

""" + CTA_BAND)

# ---------------------------------------------------------------- fit
PAGES["is-it-for-you.html"] = dict(
title="Is it for you — Green Light Buying Machine",
desc="An honest fit list for the program: who it works for, who it doesn't, and what we expect from students.",
main=phead("Before you apply", "Is it for you?",
  "We're looking for operators with 10 to 15 flips behind them and a crew already working. Being honest about that up front saves everyone a hard conversation three weeks in.") + """

<section>
  <div class="wrap">
    <div class="fit">
      <div class="col">
        <h3>A fit if you</h3>
        <ul>
          <li>Have 10 to 15 completed flips behind you</li>
          <li>Already run your own crew &mdash; not trades you'd have to go find</li>
          <li>Buy and finance your own deals: first, second, hard money, however you normally stack it</li>
          <li>Are ready to own the entire buildout, start to finish</li>
          <li>Want a different exit, not a different hobby</li>
          <li>Can work an Arizona property &mdash; that's where our deal flow and buyers are today</li>
          <li>Can invest $15,000 in the program, if accepted, on top of the deal itself</li>
        </ul>
      </div>
      <div class="col not">
        <h3>Not a fit if you</h3>
        <ul>
          <li>Are early in your flipping career</li>
          <li>Would need to assemble a crew first</li>
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

<section class="band">
  <div class="wrap">
    <h2>Not in Arizona?</h2>
    <div class="split" style="margin-top:1.5rem">
      <div>
        <p>Arizona is where we operate today. The deal flow, the lender, the buyer list, and twenty-six years of knowing which streets work &mdash; all of it is here, and that's most of what makes the program worth $15,000.</p>
        <p>We're building toward other markets. We'd rather do that properly than plant a flag somewhere we can't yet source a deal or bring you a buyer.</p>
      </div>
      <div>
        <p>So apply anyway. Tell us where you operate, and we'll put you on the list for your market. Where we go next is going to be decided by where the qualified operators are &mdash; which means the applications we get.</p>
        <div class="cta-row"><a class="btn" href="apply.html">Apply and name your market</a></div>
      </div>
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
      <p>We guarantee we'll present your finished property to our qualified buyer list &mdash; investors who have already bought from us and are waiting on the next one. What we can't guarantee is that one of them buys yours. That comes down to the house, your execution, and the market when you finish. <span class="todo">Confirm this wording matches the MSA before launch.</span></p>
    </div>
    <div class="qa">
      <h3>Do I have to be in Arizona?</h3>
      <p>You don't have to live here, but today the property does. Cohorts are Arizona-based because that's where our deal flow, our lender and our buyers are. We're working toward other markets, and applications from out-of-state operators are how we decide which one comes next &mdash; so apply and tell us where you are.</p>
    </div>
    <div class="qa">
      <h3>What if the renovation runs long?</h3>
      <p>Same as any flip &mdash; it's your holding cost and your schedule. What changes is that your buyer is being lined up while you work rather than after you list, so the back end of the timeline isn't sitting on a market you can't control.</p>
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
title="Apply to the program — Green Light Buying Machine",
desc="For Arizona fix-and-flip operators with 10 to 15 projects behind them and a crew already running.",
main=phead("For operators", "Apply to the program",
  "We take a small number of operators who already know how to build. Tell us about your work and we'll tell you honestly whether this is the right move for you now.") + """

<section>
  <div class="wrap">
    <div class="split">
      <div>
        <p>Nothing here is a commitment. It's how we find out whether your experience, your crew, and your capital line up with what the program actually requires &mdash; before either of us spends time on a call.</p>
        <p style="margin-bottom:1.75rem">Applying costs nothing. If you're accepted, the program is <b>$15,000</b>, separate from the house &mdash; you buy and finance the property yourself. We'd rather you know the number now than three conversations from now.</p>
        <form class="js-form" action="/api/apply" method="post" novalidate
              data-source="program application"
              data-sending="Sending your application&#8230;"
              data-success="Got it. We&#8217;ll review your background and come back to you either way.">
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="pair">
            <div class="field">
              <label for="a-name">Your name</label>
              <input id="a-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="a-phone">Phone</label>
              <input id="a-phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field">
            <label for="a-email">Email</label>
            <input id="a-email" name="email" type="email" autocomplete="email" required>
          </div>
          <div class="field">
            <label for="a-flips">Flips you've completed</label>
            <select id="a-flips" name="flips" required>
              <option value="">Select one</option>
              <option>Fewer than 5</option>
              <option>5 to 9</option>
              <option>10 to 15</option>
              <option>More than 15</option>
            </select>
            <p class="hint">We're looking for 10 to 15 or more. Fewer is not a no forever, just a no for now.</p>
          </div>
          <div class="field">
            <label for="a-crew">Your crew</label>
            <select id="a-crew" name="crew" required>
              <option value="">Select one</option>
              <option>I run my own crew</option>
              <option>I use the same trades on every job</option>
              <option>I hire per project</option>
              <option>I'd need to build one</option>
            </select>
          </div>
          <div class="field">
            <label for="a-financing">How you fund your deals</label>
            <select id="a-financing" name="financing" required>
              <option value="">Select one</option>
              <option>Cash</option>
              <option>Hard money, first and second</option>
              <option>Private lenders</option>
              <option>Line of credit</option>
              <option>Still arranging financing</option>
            </select>
          </div>
          <div class="pair">
            <div class="field">
              <label for="a-market">Where you operate</label>
              <select id="a-market" name="market" required>
                <option value="">Select one</option>
                <option>The Phoenix valley</option>
                <option>Elsewhere in Arizona</option>
                <option>Out of state, would work an Arizona deal</option>
                <option>Out of state, want it in my market</option>
              </select>
            </div>
            <div class="field">
              <label for="a-timeline">When you'd start</label>
              <select id="a-timeline" name="timeline" required>
                <option value="">Select one</option>
                <option>Next available cohort</option>
                <option>Next 3 months</option>
                <option>3 to 6 months</option>
                <option>Just exploring</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="a-city">Your city and state</label>
            <input id="a-city" name="city" type="text" placeholder="Mesa, AZ" required>
            <p class="hint">We run Arizona cohorts today. We're planning where to open next, and applications are how we decide.</p>
          </div>
          <div class="field">
            <label for="a-recent">Your last project</label>
            <textarea id="a-recent" name="recent" placeholder="Where it was, what the scope was, how it went. A few lines is fine."></textarea>
          </div>
          <button class="submit" type="submit">Send my application</button>
        </form>
      </div>
      <div>
        <h3 style="margin-bottom:1rem">What happens next</h3>
        <ul class="plain">
          <li>We read it &mdash; a person, not a filter</li>
          <li>If it's a fit, we set up a call</li>
          <li>If we both want to go ahead, you're accepted</li>
          <li>Payment comes after that, not before</li>
          <li>If it isn't a fit yet, we'll tell you what would change that</li>
        </ul>

        <h3 style="margin:2rem 0 1rem">Before you apply</h3>
        <p>The <a href="is-it-for-you.html">fit list</a> is blunt about who this works for. Reading it first will save you five minutes if the answer is no.</p>

        <h3 style="margin:2rem 0 1rem">Not an operator?</h3>
        <p>If you have a property you think would convert well, <a href="submit-a-property.html">send it to us</a> instead. If you're looking to buy a finished home, <a href="for-buyers.html">start here</a>.</p>
      </div>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- submit a property
PAGES["submit-a-property.html"] = dict(
title="Submit a property — Green Light Buying Machine",
desc="Wholesalers, agents and owners: send us an Arizona property you think converts to co-living.",
main=phead("Deal flow", "Submit a property",
  "Have an Arizona house you think would make a good co-living conversion? Send it over. We'll underwrite it the Green Light way and tell you what we see.") + """

<section>
  <div class="wrap">
    <div class="split">
      <div>
        <p>We're always looking at distressed inventory for our operators. If you're a wholesaler, an agent, or an owner sitting on something that might work, this is the fastest way to get it in front of us.</p>
        <p style="margin-bottom:1.75rem">We underwrite by rentable room rather than bedroom count, so houses that look unremarkable on the MLS sometimes work very well &mdash; and some that look perfect don't. Send it either way.</p>
        <form class="js-form" action="/api/property" method="post" novalidate
              data-source="property submission"
              data-sending="Sending the property&#8230;"
              data-success="Got it. We&#8217;ll take a look and come back to you.">
          <div class="hp" aria-hidden="true">
            <label for="company">Company</label>
            <input id="company" name="company" type="text" tabindex="-1" autocomplete="off">
          </div>
          <div class="pair">
            <div class="field">
              <label for="p-name">Your name</label>
              <input id="p-name" name="name" type="text" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="p-phone">Phone</label>
              <input id="p-phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="pair">
            <div class="field">
              <label for="p-email">Email</label>
              <input id="p-email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="p-role">You are</label>
              <select id="p-role" name="role" required>
                <option value="">Select one</option>
                <option>Wholesaler</option>
                <option>Agent</option>
                <option>Owner</option>
                <option>Investor</option>
                <option>Other</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="p-address">Property address</label>
            <input id="p-address" name="address" type="text" required>
            <p class="hint">Arizona properties for now. An MLS or listing link works too.</p>
          </div>
          <div class="pair">
            <div class="field">
              <label for="p-price">Asking or contract price</label>
              <input id="p-price" name="price" type="text">
            </div>
            <div class="field">
              <label for="p-specs">Beds, baths, square footage</label>
              <input id="p-specs" name="specs" type="text" placeholder="3 / 2 / 1,650">
            </div>
          </div>
          <div class="field">
            <label for="p-notes">Anything we should know</label>
            <textarea id="p-notes" name="notes" placeholder="Condition, lot, timing, why you think it works."></textarea>
          </div>
          <button class="submit" type="submit">Send the property</button>
        </form>
      </div>
      <div>
        <h3 style="margin-bottom:1rem">What we look for</h3>
        <ul class="plain">
          <li>Distressed or dated &mdash; we'd rather do the work</li>
          <li>A footprint that can carry at least eight bedrooms</li>
          <li>Somewhere residents actually want to live</li>
          <li>Numbers that leave room for a conversion budget</li>
        </ul>
        <p style="margin-top:1.75rem">Not every property works, and we'll tell you why when one doesn't. Send the next one anyway.</p>

        <h3 style="margin:2rem 0 1rem">Want to build them instead?</h3>
        <p>If you're an operator with 10 to 15 flips behind you, <a href="apply.html">apply to become a student</a>.</p>
      </div>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- buyers
PAGES["for-buyers.html"] = dict(
title="Buy a finished co-living property — Green Light Buying Machine",
desc="Qualified investors get first look at Arizona co-living properties, converted and built to operator standard.",
main=phead("For investors", "Buy a finished property",
  "Converted, furnished, and built to PadSplit standard. We work to match inventory with pre-qualified buyers before a renovation finishes &mdash; which is why getting qualified comes first.") + """

<section>
  <div class="wrap">
    <h2>What you're actually buying</h2>
    <div class="split">
      <div>
        <p>A single-family house in the Valley, reconfigured into individually rented rooms with shared kitchen and living space, listed and managed through PadSplit. Built to the standard the platform's residents expect rather than to whatever a contractor thought was close enough.</p>
        <p>Every property in our inventory was renovated by an operator inside our program, to a scope we set, with review at defined checkpoints. That's the difference between this and buying somebody's first attempt at a room conversion.</p>
      </div>
      <div>
        <p>Every house we build has at least eight bedrooms and two bathrooms, and often considerably more bathrooms than that. Ensuite rooms command higher rent on PadSplit and turn over less, so where the numbers support the extra baths we build them &mdash; and it's far cheaper to do that during a gut renovation than to add them later.</p>
        <p>The house comes furnished. We handle the furnishings as part of the buildout, so you're not sourcing eight or ten bedrooms' worth of beds and desks after closing.</p>
        <p>We also help you launch it on PadSplit &mdash; getting the listing live and the rooms ready to fill. That holds whether you bring in a property manager or run it yourself.</p>
        <p><span class="todo">Confirm whether properties are tenanted or vacant at close, and disclose any buyer-side fee here.</span></p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>After you close</h2>
    <div class="split">
      <div>
        <p>A finished house still has to get listed and filled. We help you launch on PadSplit rather than handing you keys and a login &mdash; the listing, the room setup, and getting live in front of residents.</p>
        <p>From there PadSplit is the engine. It markets the rooms and drives the applicant flow, so you're not advertising a bedroom or fielding calls. It screens too: background checks, income verification, eviction history, and week-to-week payments, with no credit check on residents.</p>
      </div>
      <div>
        <p>What's left is the physical house &mdash; turnovers, repairs, keeping common areas right. That part is your call: some buyers bring in a property manager, others handle it themselves. Both work, and we'll walk you through what each involves before you decide.</p>
        <p>Worth knowing going in: co-living earns from multiple rooms, so vacancy and turnover behave differently than they do on a single-tenant rental. One empty room isn't an empty house.</p>
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
      <li><div><b>We work to match you early</b><span>We aim to pair inventory with buyers while the renovation is underway rather than after it lists.</span></div></li>
      <li><div><b>You tour and diligence</b><span>Your inspector, your lender, your timeline. We don't rush this part.</span></div></li>
      <li><div><b>You close</b><span>On a property that was built to be exactly what it is.</span></div></li>
    </ol>
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
          <li>Expect an asset with no management decisions at all</li>
        </ul>
      </div>
    </div>
    <p style="margin-top:2rem;opacity:.8;font-size:.95rem">Co-living properties produce income from multiple rooms, which means vacancy, turnover, and management work differently than they do on a standard rental. We'll walk you through how before you buy, not after.</p>
  </div>
</section>

<section class="band" id="qualify">
  <div class="wrap">
    <h2>Getting qualified is two steps</h2>
    <p>We can't bring you a deal until you're pre-qualified. When a house goes live it moves fast, and we need to know you can close &mdash; not that you're interested.</p>

    <div class="steps2">
      <div class="stepbox">
        <div class="n">STEP ONE</div>
        <h3>Talk to Rachelle</h3>
        <p>Rachelle Coffey is the lender we work with, and she finances PadSplit properties specifically &mdash; which matters, because a lender pricing this house against ordinary residential comps will undervalue what you're buying. Getting pre-qualified is how we know you can close when a home comes available. It costs nothing and takes one conversation.</p>
        <div class="cta-row">
          <a class="btn" href="https://go.homeownersfg.com/home/rachelle-coffey" target="_blank" rel="noopener noreferrer">Get pre-qualified with Rachelle &rarr;</a>
        </div>
      </div>
      <div class="stepbox">
        <div class="n">STEP TWO</div>
        <h3>Tell us you're ready</h3>
        <p>Once Rachelle confirms you're pre-qualified, fill in the form below. That's what puts you on the list &mdash; and pre-qualified buyers get first access when a deal goes live.</p>
        <div class="cta-row">
          <a class="btn ghost" href="#ready">Go to the form &darr;</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section id="ready">
  <div class="wrap">
    <h2>Let us know you&#8217;re ready</h2>
    <p>Already pre-qualified? This is how we know to put you on the list. When a property goes live, this is who we call first.</p>
    <p class="todo">The embedded form is currently the one named &#8220;Rachelle Test&#8221; &mdash; confirm the production form ID before launch.</p>
    <div class="embed">
      <iframe
        src="https://api.leadconnectorhq.com/widget/form/cIkTFxnNpva0nNDICpQx?notrack=true"
        id="inline-cIkTFxnNpva0nNDICpQx"
        data-layout="{'id':'INLINE'}"
        data-trigger-type="alwaysShow"
        data-activation-type="alwaysActivated"
        data-deactivation-type="neverDeactivate"
        data-form-name="Buyer readiness"
        data-height="800"
        data-layout-iframe-id="inline-cIkTFxnNpva0nNDICpQx"
        data-form-id="cIkTFxnNpva0nNDICpQx"
        title="Buyer readiness form"
        loading="lazy"
        allowfullscreen></iframe>
    </div>
    <script src="https://link.msgsndr.com/js/form_embed.js"></script>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>What you&#8217;d be buying</h2>
    <p>Finished conversions, furnished by us and launched on PadSplit. The floor plans and photos are worth looking at before you talk to anyone.</p>
    <div class="grid-homes">
""" + shots(HOMES, "homes", 4) + """</div>
    <div class="cta-row">
      <a class="btn ghost" href="homes.html">See all the homes and plans</a>
    </div>
  </div>
</section>""")

# ---------------------------------------------------------------- homes
PAGES["homes.html"] = dict(
title="Homes we've built — Green Light Buying Machine",
desc="Finished Arizona co-living conversions and the floor plans behind them.",
main=phead("The work", "Homes we&#8217;ve built",
  "Finished conversions and the plans behind them. Every property is held to the same standard, whoever renovated it.") + """

""" + STATS + """

<section>
  <div class="wrap">
    <h2>Floor plans</h2>
    <p>Eight bedrooms minimum, on footprints that started as three or four, with ensuite bathrooms wherever the numbers support them. Rooms are named rather than numbered where we can &mdash; it reads better to residents and keeps the plan legible for the crew.</p>
    <div class="grid-plans">
""" + shots(PLANS, "plans") + """</div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Finished houses</h2>
    <p>Shared kitchens, common areas, laundry, and private rooms &mdash; furnished and in service.</p>
    <div class="grid-homes">
""" + shots(HOMES, "homes") + """</div>
    <div class="cta-row">
      <a class="btn" href="for-buyers.html">Get on the buyer list</a>
      <a class="btn ghost" href="how-it-works.html">Build one with us</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>More of the construction work</h2>
    <p>Brian and Gina's construction company has a wider portfolio than the co-living conversions shown here.</p>
    <p><a class="btn ghost" href="https://trinitydesignconstruction.com/" target="_blank" rel="noopener noreferrer">See Trinity Design and Construction &rarr;</a></p>
  </div>
</section>""")

# ---------------------------------------------------------------- faq
PAGES["faq.html"] = dict(
title="FAQ — Green Light Buying Machine",
desc="Co-living, PadSplit, who actually lives in these homes, and how the numbers compare to traditional flipping.",
main=phead("Questions", "Frequently asked questions",
  "The infrastructure behind certified co-living assets. Start here if co-living or PadSplit is new to you.") + """

<section>
  <div class="wrap">
    <div class="qa">
      <h3>What is co-living?</h3>
      <p>Unrelated adults sharing a house, each renting their own private, furnished bedroom while the kitchen, living room and laundry stay common. A lot of co-living houses run three or four residents. Ours don't &mdash; we build to a minimum of eight bedrooms, because the economics that make this worth doing come from room count.</p>
    </div>
    <div class="qa">
      <h3>What is PadSplit?</h3>
      <p>A marketplace that connects residents with hosts, in the way Airbnb connects guests with owners. PadSplit does the marketing and brings the applicants, then screens them &mdash; background checks, income verification, eviction history, no credit check &mdash; and runs the management system for week-to-week rentals. As the owner you're not advertising rooms or chasing rent.</p>
    </div>
    <div class="qa">
      <h3>Who actually lives in these homes?</h3>
      <p>Not students. In the Kingdeskis' houses the average resident is between 45 and 50 years old, and many stay for years rather than weeks. Affordable housing for working adults is what this is, and it's worth setting the stereotype aside early.</p>
    </div>
    <div class="qa">
      <h3>How do the numbers compare to a traditional flip?</h3>
      <p>Retail flip margins have thinned as rates rose, and you're competing for the same houses as everyone else. A co-living conversion sells to a buyer pricing the property on what it produces by the room rather than on comps down the street, and that spread is meaningfully wider than a retail exit. What any individual deal returns depends on the house, the market, and how you execute &mdash; we'll walk you through the math on a real property rather than quote you an average.</p>
    </div>
    <div class="qa">
      <h3>What makes the Green Light approach different?</h3>
      <p>Most operators convert an existing rental or short-term property and work around what's already there &mdash; which usually means rooms sharing a hall bathroom, because adding baths to a finished house is expensive and awkward. We buy distressed properties and design for PadSplit from the first wall, which lets us build ensuite rooms where the numbers support them. Designing for the model instead of retrofitting it is what produces a house that holds rent and keeps residents.</p>
    </div>
    <div class="qa">
      <h3>How many bedrooms and bathrooms?</h3>
      <p>Eight bedrooms and two bathrooms is the floor &mdash; we don't build below it. Above that floor, bathrooms are an underwriting decision rather than a finish upgrade: a room with its own ensuite bathroom rents for more than one sharing down the hall, and PadSplit's data shows how much more by submarket. Where the numbers support the extra baths, we build them. The plan on our home page is eight bedrooms and seven bathrooms for exactly that reason.</p>
    </div>
    <div class="qa">
      <h3>What is the Green Light Way?</h3>
      <p>How we underwrite. We price a house by rentable room rather than by bedroom count, using PadSplit's room-level rent data and accounting for which rooms can be built ensuite. That calculation is what decides whether a conversion works, and it's what turns a pile of wholesale addresses into deal flow an investor can act on.</p>
    </div>
    <div class="qa">
      <h3>What is the Green Light Buying Machine?</h3>
      <p>The system and training program Brian and Gina built to teach operators how to find, buy, and convert distressed homes into co-living properties &mdash; using 26 years of trade knowledge rather than theory.</p>
    </div>
    <div class="qa">
      <h3>Is there real demand for the finished homes?</h3>
      <p>Demand for affordable housing in the Valley is the reason this model works at all, and it's why we qualify buyers before inventory rather than after. How quickly any particular house finds its buyer depends on the property and the market at the time.</p>
    </div>
  </div>
</section>

<section class="band">
  <div class="wrap">
    <h2>Still deciding which side you're on</h2>
    <div class="doors">
      <div class="door">
        <div class="who">If you build</div>
        <h3>Build one with us</h3>
        <p>You have completed renovations and a crew. We source the deal, coach the conversion, and bring the buyer.</p>
        <div class="cta-row"><a class="btn" href="how-it-works.html">How the program works</a></div>
      </div>
      <div class="door buy">
        <div class="who">If you buy</div>
        <h3>Buy a finished property</h3>
        <p>Converted, furnished, built to standard. Pre-qualified buyers are matched to inventory before the renovation finishes.</p>
        <div class="cta-row"><a class="btn" href="for-buyers.html">Get on the buyer list</a></div>
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
