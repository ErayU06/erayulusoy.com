/* Runs before the page renders: enables motion styles and picks the visitor's language. */
(function () {
  var d = document.documentElement;
  d.classList.add('js');
  var pref = null;
  try { pref = localStorage.getItem('lang'); } catch (e) {}
  var onTr = location.pathname.indexOf('/tr') === 0;
  if (!pref && !onTr) {
    var langs = navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ''];
    if (String(langs[0] || '').toLowerCase().indexOf('tr') === 0) location.replace('/tr/' + location.hash);
  }
})();
