### Опиание проекта.
Сайт Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Мануал по устновке проекта

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/AntonSpark/foodgram-project-react.git
```
```
cd foodgram-project-react
```
2. Установить виртуальное окружение
```
python -m venv venv
```
3. Запустить виртуальное окружение
```
venv\Scripts\activate
```
4. Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
5. Выполнить миграции:
```
python manage.py migrate
```
6. Запустить проект:
```
python manage.py runserver
```
7. Запустить frontened:
```
cd frontend
```
```
npm run start
```
```
перейти на http://localhost:3000/recipes
```

## Шаблон наполнения .env файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```
### Над проектом работал:

Антон Искров