# 🛡 Proxy Telegram Bot (модульная версия)

Управление Squid-прокси через Telegram с удобным меню, генерацией логинов/паролей, мониторингом и бэкапом.

---

## 📁 Структура проекта

```
proxy_bot/
├── proxy_bot.py            # Главный файл запуска
├── .env                    # Переменные окружения (НЕ загружать в git)
├── handlers/               # Обработчики команд и кнопок
├── utils/                  # Утилиты: работа с creds, system info и т.п.
├── keyboards/              # Генерация inline-клавиатур
├── README.md
```

---

## ⚙️ Переменные в `.env` (пример)

```env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
AUTHORIZED_USER_ID=123456789
SHARE_IP=1.2.3.4
SHARE_PORT=3128
PASSWD_FILE=/etc/squid/passwd
CREDS_FILE=/root/final-proxy-stack/squid/creds.json
ACCESS_LOG=/var/log/squid/access.log
GPG_PASS=
TIMEOUT_SEC=1
```

---

## 🚀 Запуск

### ▶️ Ручной запуск:

```bash
cd proxy_bot
python3 proxy_bot.py
```

### 🛠 Через systemd:

Создай файл `/etc/systemd/system/proxy_bot.service`:

```ini
[Unit]
Description=Proxy Telegram Bot
After=network.target

[Service]
WorkingDirectory=/root/proxy_bot
ExecStart=/usr/bin/python3 /root/proxy_bot/proxy_bot.py
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Далее:

```bash
sudo systemctl daemon-reload
sudo systemctl enable proxy_bot.service
sudo systemctl start proxy_bot.service
```

---

## 🔧 Возможности

- 👥 Управление пользователями: добавление, удаление, просмотр паролей
- 📈 Мониторинг: трафик по логам Squid, загрузка CPU/RAM/Disk
- 📦 Бэкап: /etc, /var, список пакетов, бот + скрипты
- ♻️ Восстановление из архива
- 🧨 Очистка старых и всех бэкапов
- 📤 Отправка IP и порта прокси

---

## 📌 Важно

- `.env` **НЕ добавляй в публичный репозиторий**
- При тестах с curl всегда используйте строчные логины (Squid чувствителен к регистру)
- После добавления пользователя используется `systemctl reload squid` для скорости

