/* Runs before the page renders: enables motion styles and picks the visitor's language. */
(function () {
  var d = document.documentElement;
  d.classList.add('js');
  var pref = null;
  try { pref = localStorage.getItem('lang'); } catch (e) {}
  var onHome = location.pathname === '/' || location.pathname === '/index.html';
  if (!pref && onHome) {
    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    if (String(langs[0] || '').toLowerCase().indexOf('tr') === 0) location.replace('/tr/' + location.hash);
  }
})();
