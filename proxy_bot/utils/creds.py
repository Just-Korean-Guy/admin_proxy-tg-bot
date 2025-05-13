from config import PASSWD_FILE, GPG_PASS
import os
import json
import logging
import secrets
import string
from dotenv import load_dotenv
import subprocess

# — Загрузка .env вручную (на случай, если запускается не из корня)
load_dotenv("/root/proxy_bot/.env")
CREDS_FILE = os.getenv("CREDS_FILE")

# — УТИЛИТЫ ————————————————————————————

def generate_password(length: int = 12) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def save_creds(final_data: dict):
    with open(CREDS_FILE, "w") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    logging.info("✅ creds.json сохранён.")

    if GPG_PASS:
        os.system(f'gpg --quiet --batch --yes --symmetric --cipher-algo AES256 --passphrase "{GPG_PASS}" {CREDS_FILE}')
        logging.info("🔐 creds.json зашифрован в .gpg")

    sync_with_squid(final_data)

def load_creds() -> dict:
    try:
        if os.path.isfile(CREDS_FILE + ".gpg") and GPG_PASS:
            os.system(f'gpg --quiet --batch --yes --decrypt --passphrase "{GPG_PASS}" -o {CREDS_FILE} {CREDS_FILE}.gpg')

        if os.path.isfile(CREDS_FILE):
            with open(CREDS_FILE, "r") as f:
                return json.load(f)

    except Exception as e:
        logging.warning(f"❌ Ошибка загрузки creds: {e}")
    return {}

def sync_with_squid(creds: dict, path=PASSWD_FILE):
    if os.path.exists(path):
        os.rename(path, path + ".bak")

    for idx, (user, pwd) in enumerate(creds.items()):
        args = ["htpasswd", "-b", "-m"]
        if idx == 0:
            args.append("-c")  # создать новый файл
        args += [path, user, pwd]
        subprocess.run(args, check=True)

    logging.info("🦑 Squid credentials обновлены.")
    os.system("systemctl reload squid")
