from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('genres/', views.genres_list, name='genres'),
    path('genres/<slug:slug>/', views.genre_detail, name='genre_detail'),
    path('authors/', views.authors_list, name='authors'),
    path('authors/<slug:slug>/', views.author_detail, name='author_detail'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/toggle/<int:book_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search, name='search'),
    path('books/load/', views.load_books, name='load_books'),
]
