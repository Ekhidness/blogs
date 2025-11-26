# Blogs

Простой микроблог на Django.

В приложении можно регистрироваться, создавать посты, ставить лайки, писать комментарии и настраивать свой профиль (менять имя, биографию и аватарку).

## Установка и запуск

**1. Установка библиотек и бд**
```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**2. Запуск
```bash
python manage.py runserver
```
