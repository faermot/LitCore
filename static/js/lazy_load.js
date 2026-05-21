(function () {
  'use strict';

  const btn     = document.getElementById('load-more');
  const grid    = document.getElementById('books-grid');
  const spinner = document.getElementById('spinner');
  if (!btn || !grid) return;

  let loading = false;

  function escHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderCard(book) {
    const isFav = !!book.is_favorite;

    const coverHtml = book.cover
      ? `<img class="book-card__cover"
              src="${escHtml(book.cover)}"
              alt="${escHtml(book.title)}"
              loading="lazy">`
      : `<div class="book-card__no-cover">
           <svg width="40" height="40" viewBox="0 0 24 24"
                fill="none" stroke="currentColor" stroke-width="1.5">
             <path d="M4 19.5A2.5 2.5 0 016.5 17H20"/>
             <path d="M6.5 2H20v20H6.5A2.5 2.5 0 014 19.5v-15A2.5 2.5 0 016.5 2z"/>
           </svg>
         </div>`;

    const ratingHtml = book.rating > 0
      ? `<div class="book-card__rating">
           <svg width="14" height="14" viewBox="0 0 24 24" fill="#FF6B35" stroke="none">
             <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02
                              12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
           </svg>
           ${escHtml(String(book.rating))}
         </div>`
      : '';

    return `
      <div class="book-card" data-id="${book.id}">
        <a href="/books/${escHtml(book.slug)}/" class="book-card__link">
          <div class="book-card__cover-wrap">
            ${coverHtml}
            <div class="book-card__overlay">
              <p class="book-card__desc">${escHtml(book.description)}</p>
            </div>
          </div>
          <div class="book-card__info">
            <h3 class="book-card__title">${escHtml(book.title)}</h3>
            <p class="book-card__authors">${escHtml(book.authors)}</p>
            ${ratingHtml}
          </div>
        </a>
        <button class="fav-btn${isFav ? ' fav-btn--active' : ''}"
                data-book-id="${book.id}"
                title="${isFav ? 'Убрать из избранного' : 'В избранное'}">
          <svg width="18" height="18" viewBox="0 0 24 24"
               stroke="currentColor" stroke-width="2"
               fill="${isFav ? '#FF6B35' : 'none'}">
            <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67
                     l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06
                     L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z"/>
          </svg>
        </button>
      </div>`;
  }

  function loadMore() {
    if (loading) return;
    loading = true;
    btn.style.display = 'none';
    spinner.style.display = 'block';

    const page  = btn.dataset.page;
    const genre = btn.dataset.genre || '';
    const url   = `/books/load/?page=${encodeURIComponent(page)}${genre ? '&genre=' + encodeURIComponent(genre) : ''}`;

    fetch(url)
      .then(r => {
        if (!r.ok) throw new Error('Network error ' + r.status);
        return r.json();
      })
      .then(data => {
        data.books.forEach(book => {
          grid.insertAdjacentHTML('beforeend', renderCard(book));
        });

        spinner.style.display = 'none';

        if (data.has_next) {
          btn.dataset.page = data.next_page;
          btn.style.display = 'inline-flex';
        } else {
          btn.remove();
          observer.disconnect();
        }
        loading = false;
      })
      .catch(() => {
        spinner.style.display = 'none';
        btn.style.display = 'inline-flex';
        loading = false;
      });
  }

  const observer = new IntersectionObserver(
    (entries) => { if (entries[0].isIntersecting) loadMore(); },
    { rootMargin: '400px', threshold: 0 }
  );

  btn.addEventListener('click', loadMore);
  observer.observe(btn);
})();
