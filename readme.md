```sh
docker-compose run web python3 manage.py migrate
```

```sh
docker-compose up
```

http://127.0.0.1:8000/upload/  - страница загрузки типовых файлов deals.csv.

http://127.0.0.1:8000/result/ - страница с результатами обработки последнего файла.

Загруженные файлы сохраняются в папке Upload.
