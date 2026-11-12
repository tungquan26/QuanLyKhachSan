document.body.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
menu?.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
    menu.click();
    menu.focus();
  }
});
document.querySelectorAll('[data-entry-form]').forEach(form => {
  form.addEventListener('submit', event => {
    if (form.dataset.submitting) { event.preventDefault(); return; }
    form.dataset.submitting = 'true';
    form.setAttribute('aria-busy', 'true');
    // Keep the submitter's name/value in the POST when showing progress.
    if (event.submitter) {
      event.submitter.textContent = 'Đang xử lý…';
      event.submitter.setAttribute('aria-disabled', 'true');
    }
  });
});
window.addEventListener('pageshow', event => { if (event.persisted) window.location.reload(); });
