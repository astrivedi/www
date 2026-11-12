(() => {
  const key = 'appearance';
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference;
  try { preference = localStorage.getItem(key); } catch {}
  if (preference !== 'light' && preference !== 'dark') preference = null;
  let button;
  function apply() {
    const dark = preference ? preference === 'dark' : system.matches;
    document.documentElement.dataset.theme = dark ? 'dark' : 'light';
    if (button) {
      button.setAttribute('aria-pressed', String(dark));
      button.title = `Switch to ${dark ? 'light' : 'dark'} mode`;
    }
  }
  apply();
  system.addEventListener('change', apply);
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = ['light', 'dark'].includes(event.newValue) ? event.newValue : null;
    apply();
  });
  document.addEventListener('DOMContentLoaded', () => {
    button = document.querySelector('.theme-toggle');
    if (!button) return;
    button.hidden = false;
    button.addEventListener('click', () => {
      preference = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem(key, preference); } catch {}
      apply();
    });
    apply();
  });
})();
