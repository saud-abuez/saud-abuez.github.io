(function () {
  var norm = function (s) {
    return s.replace(/[\u064B-\u0652\u0640]/g, '').replace(/[أإآٱ]/g, 'ا').replace(/ى/g, 'ي')
            .replace(/ة/g, 'ه').replace(/ؤ/g, 'و').replace(/ئ/g, 'ي').toLowerCase();
  };
  var q = document.getElementById('q'), out = document.getElementById('results');
  if (q && out && window.DIWAN_INDEX) {
    var idx = window.DIWAN_INDEX.map(function (p) { return { p: p, n: norm(p.t + ' | ' + p.x) }; });
    q.addEventListener('input', function () {
      var terms = norm(q.value.trim()).split(/\s+/).filter(Boolean);
      out.textContent = '';
      if (!terms.length) return;
      var hits = idx.filter(function (e) { return terms.every(function (t) { return e.n.indexOf(t) > -1; }); }).slice(0, 20);
      if (!hits.length) {
        var d = document.createElement('div'); d.className = 'empty'; d.textContent = 'لا توجد نتائج مطابقة.'; out.appendChild(d); return;
      }
      hits.forEach(function (e) {
        var a = document.createElement('a'); a.href = e.p.u;
        var lines = e.p.x.split(' | '), snip = lines.filter(function (l) { return norm(l).indexOf(terms[0]) > -1; })[0] || lines[0];
        var b = document.createElement('b'); b.textContent = snip;
        var s = document.createElement('small'); s.textContent = e.p.s + ' — ' + e.p.t;
        a.appendChild(b); a.appendChild(s); out.appendChild(a);
      });
    });
  }
  var c = document.getElementById('copy-link');
  if (c) c.addEventListener('click', function () {
    var done = function () { c.textContent = 'تم النسخ ✓'; setTimeout(function () { c.textContent = 'نسخ رابط القصيدة'; }, 2000); };
    if (navigator.clipboard) navigator.clipboard.writeText(location.href).then(done); else done();
  });
})();
