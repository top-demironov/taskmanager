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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
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
4. *Конфигурация* - выбираем самую простую, много не потребуется, кому не жалко можно по-лучше взять)
5. *Сеть* - пропускаем
6. *Настройка приложения* - в `Команда запуска` устанавливаем `gunicorn taskmanager.wsgi:application`, здесь `taskmanager` это название папки, где находиться `settings.py`
7. *Инофрмация о приложении* - для удобства можно назвать приложение и дать ему комментарий

Нажимаем `Запустить деплой`. 

python3 manage.py runserver 0.0.0.0:8000