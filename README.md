![This is an image](https://github.com/AntonSpark/foodgram-project-react/actions/workflows/foodgram-workflow.yml/badge.svg)

### Опиание проекта.
Сайт Foodgram, «Продуктовый помощник». Это онлайн-сервис и API для него. На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Проект доступен по ссылкам: 


```
http://51.250.20.187/admin/
http://51.250.20.187/recipes/
```
```
Учетная запись админа/юзера: логин: admin, почта:admin@mail.ru, пароль: admin12345
```

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

### Подготовка к запуску проекта на удаленном сервере

1. Cоздать и заполнить .env файл в головной директории backend
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=foodgram
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```
2. Запушить образы бэкенда и фронтенда в DockerHub
```
docker build -t логин  DockerHub/название образа для бэкенда/фронтенда) .
docker login
docker push логин на DockerHub/название образа для бэкенда/фронтенда
```
3. Изменить в файле \foodgram-project-react\infra\docker-compose.yml
поля backend/fronted image на свои образы в DockerHub
4. Выполнить вход на сервер
5. Установить Docker и docker-compose
```
sudo apt install docker.io
sudo apt-get update
sudo apt install docker-compose
```
6.  Перенести docker-compose.yml и nginx.conf из директории infra на сервер
```
scp <filename> <username>@<host>:/home/<username>/
```
7. Добавить в Secrets GitHub переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY= ваш ключ

DOCKER_PASSWORD=<пароль DockerHub>
DOCKER_USERNAME=<имя пользователя DockerHub>

USER=<username удаленного сервера>
HOST=<публичный  IPv4 сервера>
PASSPHRASE=<пароль для сервера>
SSH_KEY= <SSH ключ>

TELEGRAM_TO=<ID телеграм-аккаунта>
TELEGRAM_TOKEN=<токен бота>
```
8. После успешного выполнения workflow, на сервере:
создать и запустить миграции,
создать суперпользователя, 
подгружаем статику
загрузить тэги и ингредиенты
```
sudo docker exec -it anton_backend_1 bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
python manage.py ingredients_loader
python manage.py tags_loader
```
9. Проект готов и доступен по адресу:
```
http://ваш_ip/recipes/
```

### Над проектом работал:

Антон Искров


![This is an image](https://github.com/AntonSpark/foodgram-project-react/actions/workflows/foodgram-workflow.yml/badge.svg)