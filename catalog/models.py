import os
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify



def cover_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'covers/cover_{instance.slug or "book"}{ext}'


def author_photo_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'authors/photo_{instance.slug or "author"}{ext}'


def genre_image_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'genres/genre_{instance.slug or "genre"}{ext}'


def store_icon_upload_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    safe = instance.store.lower().replace(' ', '_')[:30]
    return f'stores/icon_{safe}{ext}'


class Genre(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField('Описание', blank=True)
    color = models.CharField('Цвет фона (запасной)', max_length=20, default='#2c3e50',
                             help_text='CSS-цвет если нет картинки')
    image = models.ImageField('Фоновая картинка', upload_to=genre_image_upload_path,
                               blank=True, null=True,
                               help_text='Рекомендуется 1200×400 px')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self): return self.name

    def get_absolute_url(self):
        if not self.slug:
            return "#"
        return reverse('catalog:genre_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField('Имя', max_length=200)
    slug = models.SlugField(unique=True, blank=False, null=False)
    photo = models.ImageField('Фото', upload_to=author_photo_upload_path, blank=True, null=True)
    bio   = models.TextField('Биография', blank=True)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']

    def __str__(self): return self.name

    def get_absolute_url(self):
        return reverse('catalog:author_detail', kwargs={'slug': self.slug})


class Book(models.Model):
    title   = models.CharField('Название', max_length=300)
    slug    = models.SlugField(max_length=300, unique=True)
    authors = models.ManyToManyField(Author, verbose_name='Авторы', related_name='books')
    genres  = models.ManyToManyField(Genre,  verbose_name='Жанры',  related_name='books')
    cover   = models.ImageField('Обложка', upload_to=cover_upload_path, blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    year    = models.PositiveIntegerField('Год издания', null=True, blank=True)
    rating  = models.DecimalField('Рейтинг', max_digits=3, decimal_places=1, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

    def __str__(self): return self.title

    def get_absolute_url(self):
        return reverse('catalog:book_detail', kwargs={'slug': self.slug})


class BuyLink(models.Model):
    book  = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='buy_links')
    store = models.CharField('Название кнопки', max_length=100,
                             help_text='Например: Литрес, Ozon, Яндекс Книги')
    url   = models.URLField('Ссылка')
    color = models.CharField('Цвет кнопки', max_length=20, default='#FF6B35',
                             help_text='HEX-цвет, например #005bff')
    icon  = models.FileField('Иконка (SVG/PNG)', upload_to=store_icon_upload_path,
                              blank=True, null=True,
                              help_text='Необязательно. SVG или PNG, ~24×24 px')

    class Meta:
        verbose_name = 'Ссылка на покупку'
        verbose_name_plural = 'Ссылки на покупку'
        ordering = ['id']

    def __str__(self):
        return f'{self.book.title} — {self.store}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.user.username} — {self.book.title}'
