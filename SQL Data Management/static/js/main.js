// Basic frontend JS
console.log('PWA loaded');

export function showSpinner() {
  document.querySelectorAll('.spinner').forEach(el => el.style.display = 'block');
}

export function hideSpinner() {
  document.querySelectorAll('.spinner').forEach(el => el.style.display = 'none');
}

export function validateForm(form) {
  for (const input of form.querySelectorAll('input[required]')) {
    if (!input.value) {
      input.classList.add('error');
      return false;
    }
    input.classList.remove('error');
  }
  return true;
}
