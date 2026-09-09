/* Two-step application. Step 1 posts contact details on its own so an
   abandoned application still leaves a usable lead in the CRM; step 2
   posts the whole thing again and GHL updates the same contact by email. */
(function () {
  var form = document.getElementById('lpForm');
  var step1 = document.getElementById('step1');
  var step2 = document.getElementById('step2');
  var bar2 = document.getElementById('bar2');
  var card = document.getElementById('form-card');
  var next = document.getElementById('toStep2');
  var back = document.getElementById('backTo1');
  var submit = form.querySelector('[type=submit]');
  var partialSent = false;

  function values() {
    var out = {};
    new FormData(form).forEach(function (v, k) { out[k] = v; });
    out.page = window.location.pathname;
    return out;
  }

  function post(payload) {
    return fetch('/api/apply', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  function valid(fields) {
    for (var i = 0; i < fields.length; i++) {
      var el = document.getElementById(fields[i]);
      if (!el.checkValidity()) { el.reportValidity(); return false; }
    }
    return true;
  }

  /* Funnel only: under-10 operators get an information path instead of a
     dead end. The question still gets asked — only the ask changes. */
  var flips = document.getElementById('lp-flips');
  var note = document.getElementById('belowBarNote');
  var intent = document.getElementById('lp-intent');
  if (flips && note && intent) {
    flips.addEventListener('change', function () {
      var below = flips.value.indexOf('more info') !== -1;
      note.hidden = !below;
      intent.value = below ? 'more_info' : 'apply';
      submit.textContent = below ? 'Send me the info' : 'Send my application';
    });
  }

  next.addEventListener('click', function () {
    if (!valid(['lp-name', 'lp-email', 'lp-city'])) return;

    /* Fire and forget — a failed partial save must never block the
       applicant from finishing. Step 2 sends everything anyway. */
    if (!partialSent) {
      var p = values();
      p.stage = 'partial';
      p.source = 'landing page';
      post(p).catch(function () {});
      partialSent = true;
    }

    step1.hidden = true;
    step2.hidden = false;
    bar2.classList.add('on');
    card.scrollIntoView({ behavior: 'smooth', block: 'start' });
    document.getElementById('lp-flips').focus();
  });

  back.addEventListener('click', function () {
    step2.hidden = true;
    step1.hidden = false;
    bar2.classList.remove('on');
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!valid(['lp-flips', 'lp-crew', 'lp-financing', 'lp-market', 'lp-timeline'])) return;

    var payload = values();
    payload.stage = 'complete';
    payload.source = 'landing page';

    submit.disabled = true;
    submit.textContent = 'Sending\u2026';

    post(payload)
      .then(function (r) {
        if (!r.ok) throw new Error(r.status);
        var wantedInfo = intent && intent.value === 'more_info';

        /* The video is the reward for finishing, not a hurdle before it.
           Only rendered on pages that ship the media folder. */
        var video =
          '<div class="video-wrap">' +
            '<video class="vid" controls preload="metadata" playsinline ' +
                   'poster="media/glbm-intro-poster.webp" width="864" height="864">' +
              '<source src="media/glbm-intro.mp4" type="video/mp4">' +
            '</video>' +
            '<p class="vid-cap">Brian and Gina, about two minutes.</p>' +
          '</div>';

        var head = wantedInfo
          ? '<h2>On its way</h2>' +
            '<p>We\u2019ll send you the book and keep you on the list. No sales calls \u2014 ' +
            'when you\u2019ve got ten or more flips behind you, email us and we\u2019ll pick it up from there.</p>' +
            '<p>While you\u2019re here, this is the two-minute version of what we do.</p>'
          : '<h2>Application received</h2>' +
            '<p>Brian or Gina will read it \u2014 a person, not a filter \u2014 and come back to you either way. ' +
            'If it\u2019s a fit we\u2019ll set up a call.</p>' +
            '<p>While you wait, here\u2019s the two-minute version of what we do.</p>';

        card.innerHTML = head + (form.dataset.video === 'off' ? '' : video) +
          '<p style="margin:1.25rem 0 0"><a class="btn" href="homes.html">See the homes we\u2019ve built</a></p>';
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
      })
      .catch(function () {
        submit.disabled = false;
        submit.textContent = 'Send my application';
        var err = document.createElement('p');
        err.className = 'status err';
        err.textContent = 'That didn\u2019t send. Email info@greenlightbuyingmachine.com and we\u2019ll pick it up from there.';
        form.appendChild(err);
      });
  });
})();
