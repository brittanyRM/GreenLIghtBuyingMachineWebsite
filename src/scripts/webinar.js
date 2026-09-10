(function () {
  /* Webinar starts 2:00 PM Arizona time on 29 Sep 2026. Arizona doesn't
     observe DST, so that's a fixed UTC-7 offset — 21:00 UTC. */
  var START = new Date('2026-09-29T21:00:00Z');
  var el = document.getElementById('count');

  function tick() {
    var ms = START - new Date();
    if (ms <= 0) { el.textContent = 'The webinar is underway.'; return; }
    var d = Math.floor(ms / 864e5),
        h = Math.floor(ms % 864e5 / 36e5),
        m = Math.floor(ms % 36e5 / 6e4);
    el.innerHTML = 'Starts in <b>' + d + 'd ' + h + 'h ' + m + 'm</b>';
    el.hidden = false;
  }
  tick();
  setInterval(tick, 30000);

  var form = document.getElementById('webinarForm');
  var ok = document.getElementById('ok');
  var note = document.getElementById('formnote');
  var submit = form.querySelector('[type=submit]');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }

    var payload = {};
    new FormData(form).forEach(function (v, k) { payload[k] = v; });
    payload.page = window.location.pathname;

    submit.disabled = true;
    submit.textContent = 'Registering\u2026';
    note.classList.remove('err');

    fetch('/api/webinar-register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      form.style.display = 'none';
      ok.classList.add('on');
      ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }).catch(function () {
      submit.disabled = false;
      submit.textContent = 'Register for the webinar';
      note.classList.add('err');
      note.textContent = 'That didn\u2019t go through. Try once more, or email ' +
        'info@greenlightbuyingmachine.com and we\u2019ll register you by hand.';
    });
  });

  document.getElementById('ics').addEventListener('click', function () {
    var ics = [
      'BEGIN:VCALENDAR', 'VERSION:2.0',
      'PRODID:-//Green Light Buying Machine//Webinar//EN',
      'BEGIN:VEVENT',
      'UID:webinar-2026-09-29@greenlightbuyingmachine.com',
      'DTSTAMP:20260909T000000Z',
      'DTSTART:20260929T210000Z',
      'DTEND:20260929T223000Z',
      'SUMMARY:Green Light Buying Machine live webinar',
      'DESCRIPTION:Brian and Gina Kingdeski on finding\\, funding\\, and flipping co-living properties. Join link was emailed to you.',
      'URL:https://greenlightbuyingmachine.com/webinar',
      'END:VEVENT', 'END:VCALENDAR'
    ].join('\r\n');

    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([ics], { type: 'text/calendar' }));
    a.download = 'green-light-buying-machine-webinar.ics';
    a.click();
    URL.revokeObjectURL(a.href);
  });
})();
