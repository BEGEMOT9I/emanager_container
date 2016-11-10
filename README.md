Event Manager

Порядок установки и найстройки:

1) Создаем базу данных
  - `psql CREATE DATABASE emanager;`

2) Копируем `./emanager_container/settings.py.example` в ту же папку без расширения `.exapmle`. Меняем в нем, в настройках БД, логин и пароль на свой

3) Миграции
  - `python manage.py makemigrations`
  - `python manage.py migrate`

4) Создаем супер-пользователя для админки
  - `python manage.py createsuperuser`