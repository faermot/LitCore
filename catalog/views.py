from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Book, Genre, Author, Favorite


PAGE_SIZE = 24


def pluralize_books(n):
    n = abs(n) % 100
    n1 = n % 10
    if 11 <= n <= 19:
        return f'{n} книг'
    if n1 == 1:
        return f'{n} книга'
    if 2 <= n1 <= 4:
        return f'{n} книги'
    return f'{n} книг'


def home(request):
    genre_slug = request.GET.get('genre', '').strip()
    genres = Genre.objects.all().order_by('name')
    books_qs = Book.objects.prefetch_related('authors', 'genres').order_by('-created_at')
    if genre_slug:
        books_qs = books_qs.filter(genres__slug=genre_slug)
    paginator = Paginator(books_qs, PAGE_SIZE)
    page = paginator.get_page(1)
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    return render(request, 'catalog/home.html', {
        'books': page,
        'genres': genres,
        'favorite_ids': favorite_ids,
        'has_next': page.has_next(),
        'active_genre': genre_slug,
    })


def load_books(request):
    page_num = int(request.GET.get('page', 1))
    genre_slug = request.GET.get('genre', '').strip()
    books_qs = Book.objects.prefetch_related('authors', 'genres').order_by('-created_at')
    if genre_slug:
        books_qs = books_qs.filter(genres__slug=genre_slug)
    paginator = Paginator(books_qs, PAGE_SIZE)
    page = paginator.get_page(page_num)
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    books_data = []
    for book in page:
        authors = ', '.join(a.name for a in book.authors.all())
        cover_url = book.cover.url if book.cover else ''
        books_data.append({
            'id': book.id,
            'title': book.title,
            'slug': book.slug,
            'authors': authors,
            'cover': cover_url,
            'rating': float(book.rating),
            'description': book.description[:200] if book.description else '',
            'is_favorite': book.id in favorite_ids,
        })
    return JsonResponse({
        'books': books_data,
        'has_next': page.has_next(),
        'next_page': page_num + 1,
    })


def genres_list(request):
    genres = Genre.objects.annotate(book_count=Count('books')).order_by('name')
    for g in genres:
        g.book_count_str = pluralize_books(g.book_count)
    return render(request, 'catalog/genres.html', {'genres': genres})


def genre_detail(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    books = Book.objects.filter(genres=genre).prefetch_related('authors').order_by('-created_at')
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    book_count_str = pluralize_books(books.count())
    return render(request, 'catalog/genre_detail.html', {
        'genre': genre,
        'books': books,
        'favorite_ids': favorite_ids,
        'book_count_str': book_count_str,
    })


def authors_list(request):
    authors = Author.objects.annotate(book_count=Count('books')).order_by('name')
    for a in authors:
        a.book_count_str = pluralize_books(a.book_count)
    return render(request, 'catalog/authors.html', {'authors': authors})


def author_detail(request, slug):
    author = get_object_or_404(Author, slug=slug)
    books = Book.objects.filter(authors=author).prefetch_related('authors', 'genres').order_by('-created_at')
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    book_count_str = pluralize_books(books.count())
    return render(request, 'catalog/author_detail.html', {
        'author': author,
        'books': books,
        'favorite_ids': favorite_ids,
        'book_count_str': book_count_str,
    })


def book_detail(request, slug):
    book = get_object_or_404(Book.objects.prefetch_related('authors', 'genres', 'buy_links'), slug=slug)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    return render(request, 'catalog/book_detail.html', {
        'book': book,
        'is_favorite': is_favorite,
    })


@login_required
def favorites(request):
    fav_books = Book.objects.filter(
        favorited_by__user=request.user
    ).prefetch_related('authors').order_by('-favorited_by__added_at')
    return render(request, 'catalog/favorites.html', {'books': fav_books})


def toggle_favorite(request, book_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'login_required'}, status=401)
    book = get_object_or_404(Book, id=book_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, book=book)
    if not created:
        fav.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


def search(request):
    q = request.GET.get('q', '').strip()
    books = []
    if q:
        books = Book.objects.filter(
            Q(title__icontains=q) |
            Q(authors__name__icontains=q) |
            Q(description__icontains=q)
        ).prefetch_related('authors').distinct()
    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    count_str = pluralize_books(len(books)) if q else ''
    return render(request, 'catalog/search.html', {
        'books': books,
        'query': q,
        'favorite_ids': favorite_ids,
        'count_str': count_str,
    })
