# YaMDB

## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».

## При создании использовался следующий стек технологий:
- Python 3.7
- Django 3.2
- Django_filter 23.2
- Django Rest Framework 3.12.14
- Django Rest Framework SimpleJWT 5.2.2

# Установка проекта: 
Клонируйте этот репозиторий с GitHub:
`git clone git@github.com:k53n8/api_yamdb.git`

Создайте виртуальное окружение:
`python -m venv venv`

Активируйте виртуальное окружение: 
`source venv/Scripts/activate`

Установите зависимости из файла requirements.txt:
`pip install -r requirements.txt`

Перейдите в папку с manage.py:
`cd api_yamdb`

Выполните миграции:
`python manage.py migrate`

Заполните БД данными из csv файлов:
`python manage.py importcsv`

Запустите сервер:
`python manage.py runserver`

Для доступа к документации (ReDoc) в бразуере перейдите по ссылке:
`http://127.0.0.1:8000/redoc/`

# Над проектом работали:
- https://github.com/brozzelerro
- https://github.com/azimovti
- https://github.com/k53n8
