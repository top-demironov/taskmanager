# Уже что-то похожее на взрослый деплой

## Шаг 0. Покупаем сервер, получаем ssh доступ
Ну взрослый уже должен с этим справиться.

И также изменяем ALLOWED_HOSTS

## Шаг 1. Подключаемся и ставим нужные штуки
```bash
ssh username@your.server.ip
```

Обновляем и ставим:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y
```

## Шаг 2. Загружаем проект

```bash
mkdir ~/taskmanager
cd ~/taskmanager
git clone https://github.com/top-demironov/taskmanager.git .
```

## Шаг 3. Виртуалка + зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Шаг 4. Настраиваем `.env`

Создаем файл `.env`
```bash
nano .env
```

В файл вставляем:
```ini
SECRET_KEY=<your-very-secret-key>
DEBUG=False
```

Потом поочереди комбинации клавиш:
1. `Ctrl + O`, `Enter` - это мы сохранили файл
2. `Ctrl + X` - вышли из изменения файла

## Шаг 5. Собираем и готовим проект

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser
```

## Шаг 6. Пробуем `gunicorn`
```bash
gunicorn taskmanager.wsgi:application --bind 127.0.0.1:8000
```

Здесь `taskmanager` это папка где находиться `settings.py`

Если запустилось без ошибок — отлично. `Ctrl+C` чтобы выйти.


## Шаг 7. systemd юнит (сервис в Linux) для gunicorn

Создаём сервис:
```bash
sudo nano /etc/systemd/system/taskmanager.service
```

Вставь (замени `root` (если другой пользователь) и `taskmanager` (если другое название проекта)):
```ini
[Unit]
Description=Gunicorn for taskmanager
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/root/taskmanager
Environment="PATH=/root/taskmanager/venv/bin"
ExecStart=/root/taskmanager/venv/bin/gunicorn taskmanager.wsgi:application --bind 127.0.0.1:8000

[Install]
WantedBy=multi-user.target
```

И также `Ctrl + O`, `enter`, `Ctrl + X`.

Далее в консоле, запускаем этот сервис:

```bash
sudo systemctl daemon-reexec
sudo systemctl start taskmanager
sudo systemctl enable taskmanager
```

Проверяем:

```bash
systemctl status taskmanager
```

## Шаг 8. Настраиваем nginx

```bash
sudo nano /etc/nginx/sites-available/taskmanager
```

Пример:
```nginx
server {
    listen 80;
    server_name 194.87.56.199;

    location /static/ {
        root /root/taskmanager;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        include proxy_params;
    }
}
```

Подключаем сайт:
```bash
sudo ln -s /etc/nginx/sites-available/taskmanager /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```


## Должно работать

Если что-то изменили в коде, нужно перезапустить сервис
```bash
sudo systemctl restart taskmanager
```