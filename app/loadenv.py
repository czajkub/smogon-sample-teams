import os
from dotenv import load_dotenv


class DBConfig:
    def __init__(
        self, DB_URL: str, DB_HOSTNAME: str, DB_PORT: int, DB_USER: str, DB_PASS: str
    ):
        self.DB_URL = DB_URL
        self.DB_HOSTNAME = DB_HOSTNAME
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS



def load_env() -> DBConfig:
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    if DB_URL is None:
        raise ValueError("Database URL not set")
    DB_HOSTNAME = os.getenv("DB_HOSTNAME")
    if DB_HOSTNAME is None:
        raise ValueError("Database hostname not set")
    PORT = os.getenv("DB_PORT")
    if PORT is None:
        raise ValueError("Database port not set")
    DB_PORT: int = int(PORT)
    DB_USERNAME = os.getenv("DB_USERNAME")
    if DB_USERNAME is None:
        raise ValueError("Database username not set")
    DB_PASS = os.getenv("DB_PASSWORD")
    if DB_PASS is None:
        raise ValueError("Database password not set")
    return DBConfig(DB_URL, DB_HOSTNAME, DB_PORT, DB_USERNAME, DB_PASS)
