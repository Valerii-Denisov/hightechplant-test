#### Для запуска требуется добавить в файл .env.dev:
```
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
```
#### Собрать образ Docker и docker-compose:
```
$ docker build .
$ docker-compose build
```
#### Запустить контейнеры:
```
docker-compose up -d --build
```
#### Проект будет доступен по адресу:
```
http://localhost:8000/
```