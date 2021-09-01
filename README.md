# Социальная сеть YaTube.

##### Социальная сеть с возможностью создания, просмотра, редактирования и удаления (CRUD) записей. Реализован механизм подписки на понравившихся авторов и отслеживание их записей. Покрытие тестами. Возможность добавления изображений.





## Инструментарий:
- Django 2.2
- Python 3.8
- Django Unittest
- Django debug toolbar
- Django ORM
- PostgreSQL



## Установка
Клонируем репозиторий.
```sh
$ git clone https://github.com/github_username/hw05_final.git
```
Создаем и активируем виртуальное окружение.
```sh
$ python -m venv venv
$ source venv/scripts/activate
```
Устанавливаем зависимости.
```sh
$ pip install -r requirements.txt
```
Создаем и применяем миграции.
```sh
$ python manage.py makemigrations 
$ python manage.py migrate
```
Запускаем локальный сервер.
```sh
$ python manage.py runserver
```
Адрес локального сервера:
```sh
127.0.0.1:8000
```




**Приятного использования**

