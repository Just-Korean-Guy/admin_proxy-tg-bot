# 🛡 Аdmin Proxy Telegram Bot (модульная версия)

По сути это по сути gui для Squid-прокси реализованное через бота в Telegram: генерация логинов/паролей, мониторинг, бэкапы.

---

## 📦 Возможности

- 👥 Управление пользователями: добавление, удаление, просмотр паролей
- 📈 Мониторинг: трафик по логам Squid, загрузка CPU, RAM и диска
- 📦 Бэкап: /etc, /var, список пакетов, скрипты
- ♻️ Восстановление из архива
- 🧨 Очистка старых и всех бэкапов
- 📤 Быстрая выдача IP и порта прокси

---

## ⚙️ Установка

```bash
# Клонируем репозиторий
git clone https://github.com/Just-Korean-Guy/admin_proxy-tg-bot.git
cd proxy_bot

# Устанавливаем зависимости
pip install -r requirements.txt
```

Создай файл `.env` в корне и добавь в него (пример):

```env
BOT_TOKEN=  # <-- сюда вставь токен своего Telegram-бота
AUTHORIZED_USER_ID=123456789
SHARE_IP=your.public.ip.address
SHARE_PORT=3128

PASSWD_FILE=/etc/squid/passwd
CREDS_FILE=/opt/proxy_bot/data/creds.json
ACCESS_LOG=/var/log/squid/access.log
GPG_PASS=
TIMEOUT_SEC=1
```

---

## 🚀 Запуск

### 🔧 Вручную

```bash
python3 proxy_bot.py
```

### 🛠 Через systemd (Linux)

Создай юнит `/etc/systemd/system/proxy_bot.service`:

```ini
[Unit]
Description=Proxy Telegram Bot
After=network.target

[Service]
WorkingDirectory=/opt/proxy_bot
ExecStart=/usr/bin/python3 /opt/proxy_bot/proxy_bot.py
Restart=always
User=proxy
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

Запусти:

```bash
sudo systemctl daemon-reload
sudo systemctl enable proxy_bot.service
sudo systemctl start proxy_bot.service
```

---

## 🛡 Безопасность

- Не загружай `.env` в публичный репозиторий
- Приводим логины к нижнему регистру (для совместимости с Squid)
- Пароли создаются без спецсимволов — 100% совместимы

---

## 📄 Лицензия

MIT — используй как хочешь. Будет приятно, если оставишь ссылку на оригинал. 😉
