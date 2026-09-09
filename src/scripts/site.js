/* Shared behaviour: gallery lightbox and form submission. */

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
      if (!form.checkValidity()) {
        var bad = form.querySelector(":invalid");
        if (bad) {
          bad.scrollIntoView({ behavior: "smooth", block: "center" });
          try { bad.focus({ preventScroll: true }); } catch (e) { bad.focus(); }
        }
        show("err", "Some fields still need filling in.");
        form.reportValidity();
        return;
      }

      var payload = {};
      new FormData(form).forEach(function (value, key) { payload[key] = value; });
      payload.source = form.dataset.source || 'website';
      payload.page = window.location.pathname;

      /* Referral attribution: /apply?from=azreia arrives tagged, so leads
         can be counted per partner without a separate form. */
      var params = new URLSearchParams(window.location.search);
      var from = params.get('from') || params.get('utm_source');
      if (from) payload.referred_by = from.slice(0, 60);

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
