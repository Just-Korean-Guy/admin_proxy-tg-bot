import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
SHARE_IP = os.getenv("SHARE_IP")
SHARE_PORT = os.getenv("SHARE_PORT")
PASSWD_FILE = os.getenv("PASSWD_FILE")
CREDS_FILE = os.getenv("CREDS_FILE")
ACCESS_LOG = os.getenv("ACCESS_LOG")
GPG_PASS = os.getenv("GPG_PASS")
TIMEOUT_SEC = int(os.getenv("TIMEOUT_SEC", 2))
