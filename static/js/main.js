const TOGGLE_URL_BASE = '/favorites/toggle/';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function showToast(msg, accent = false) {
  let toast = document.getElementById('global-toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'global-toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.toggle('toast--accent', accent);
  toast.classList.add('toast--show');
  setTimeout(() => toast.classList.remove('toast--show'), 2200);
}

document.addEventListener('click', function(e) {
  const btn = e.target.closest('.fav-btn, .fav-btn-detail');
  if (!btn) return;
  const bookId = btn.dataset.bookId;
  if (!bookId) return;

  fetch(TOGGLE_URL_BASE + bookId + '/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Accept': 'application/json',
    }
  })
  .then(res => {
    if (res.status === 401) {
      window.location.href = '/accounts/login/';
      return null;
    }
    return res.json();
  })
  .then(data => {
    if (!data) return;
    const isActive = data.status === 'added';
    document.querySelectorAll(`[data-book-id="${bookId}"]`).forEach(b => {
      b.classList.toggle('fav-btn--active', isActive);
      const svg = b.querySelector('path[d^="M20.84"]');
      if (svg) svg.setAttribute('fill', isActive ? '#FF6B35' : 'none');
      if (b.classList.contains('fav-btn-detail')) {
        b.textContent = '';
        b.innerHTML = `
          <svg width="18" height="18" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="${isActive ? '#FF6B35' : 'none'}">
            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
          </svg>
          ${isActive ? 'Убрать из избранного' : 'В избранное'}
        `;
      }
    });
    showToast(isActive ? '❤️ Добавлено в избранное' : 'Удалено из избранного', isActive);
  })
  .catch(() => showToast('Ошибка соединения'));
});
