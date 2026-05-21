# LitCore

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)

Электронный каталог книг с авторами, жанрами и избранным.  
Написано на Django + PostgreSQL.

<img width="1388" height="870" alt="image" src="https://github.com/user-attachments/assets/d30e1201-e210-42ea-9285-043ed99584bb" />


## Возможности

- Просмотр книг (обложка, авторы, рейтинг)
- Фильтр по жанру (GET-параметр `genre`)
- Поиск по названию / автору / описанию
- Страница автора (фото, биография, его книги)
- Страница жанра (баннер, цвет фона, список книг)
- Регистрация и вход
- Избранное (сердечко, AJAX, только для авторизованных)
- Админ-панель на `django-jazzmin`  
  — инлайн-редактор ссылок на магазины  
  — кроппер изображений (Pillow)

<img width="1161" height="615" alt="image" src="https://github.com/user-attachments/assets/2ff89e00-882c-4135-b0f9-976b00b888a4" />

## Технологии

- Python 3.12
- Django 5.x
- PostgreSQL (можно и SQLite для разработки)
- Gunicorn + Nginx (на сервере)
- Pillow, django-jazzmin, python-decouple
