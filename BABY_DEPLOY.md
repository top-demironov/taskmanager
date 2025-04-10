# Инструкция по деплою Django-проекта на Timeweb Apps через Git

## Шаг 1. Подготовка проекта

Убедитесь, что у вас есть файл `requirements.txt`:
```bash
pip freeze > requirements.txt
```

Убедитесь, что структура проекта стандартная:
```bash
my_project/
├── manage.py
├── requirements.txt
├── .env
└── my_project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

Установите пакет для работы с [переменными окружения](https://habr.com/ru/articles/472674/):
```bash
pip install python-dotenv
pip freeze > requirements.txt
```

Создайте файл `.env` (без названия, только расширение) в корне проекта и добавьте туда:
```ini
SECRET_KEY=<your-very-secret-key>
DEBUG=False
```

`SECRET_KEY` можно найти в `settings.py`.

В `settings.py` подключите `.env` и переменные:
```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'

ALLOWED_HOSTS = ['*']

...
```

Укажите, где будут храниться собранные статические файлы:
```python
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

Убедитесь, что у вас установлен `gunicorn`:
```bash
pip install gunicorn
pip freeze > requirements.txt
```


## Шаг 2. Загрузка проекта на GitHub

Чтобы Timeweb смог забрать проект — он должен быть размещён в Git-репозитории, например, на GitHub.

Загружаем код на GitHub, можно на приватный репозиторий.


## Шаг 3. Развёртывание проекта на Timeweb Apps

Переходим в панель `Apps`.

Нажимаем кнопку `Добавить`.

1. *Тип проекта* - `Django`, находиться во вкладке `backend`
2. *Репозиторий* - нажимаем `Добавить аккаунт`, выбираем GitHub и следуем инструкциям. После если нужно выбираем другую ветку.
3. *Регион* - выбираем регион сервера, если используете какие-то api, которые не работают в России, выбирайте `Нидерланды`.
4. *Конфигурация* - выбираем самую простую, много не потребуется, кому не жалко можно по-лучше взять).
5. *Сеть* - пропускаем.
6. *Настройка приложения* - в `Команда запуска` устанавливаем `python3 manage.py runserver 0.0.0.0:8000`. И добавляем переменные среды, которые у нас в файле `.env`.
7. *Инофрмация о приложении* - для удобства можно назвать приложение и дать ему комментарий.

Нажимаем `Запустить деплой`.

После запуска на странице `Дашбоард` мы видим нашу ссылку на сервис. Копируем ее.

В `settings.py` изменяем:

```python
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', 'top-demironov-taskmanager-4a8d.twc1.net']
CSRF_TRUSTED_ORIGINS = ['https://top-demironov-taskmanager-4a8d.twc1.net',]  # Здесь обязательно с https://
```

## Шаг 4. Делаем миграции и создаем суперпользователя

Где дашбоард приложения (где копировали ссылку), переходим на вкладку Консоль и там прописываем команды для миграций:
```bash
python manage.py makemigrations
python manage.py migrate
```

И также создаем суперпользователя:
```bash
python manage.py createsuperuser
```

## Шаг 5. Вроде работает, но что со статикой?

Так как на Timeweb apps нет встроенного `nginx`, то для обработки статики нужно добавить `WhiteNoise`.

Устанавливаем и добавляем в `requirements.txt`:
```bash
pip install whitenoise
pip freeze > requirements.txt
```

В `settings.py` добавляем:

```python
MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  ...
  'whitenoise.middleware.WhiteNoiseMiddleware',  # вот он
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

## Шаг 6. Должно работать

Если ошибка, ставим `DEBUG=True`, на timeweb и начинаем дебажить.