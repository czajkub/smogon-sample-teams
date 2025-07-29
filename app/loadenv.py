import os
from dotenv import load_dotenv
import psycopg2

class DBConfig:
    def __init__(self, DB_URL: str, DB_HOSTNAME: str, DB_PORT: int, DB_USER: str, DB_PASS: str):
        self.DB_URL = DB_URL
        self.DB_HOSTNAME = DB_HOSTNAME
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS
    def connect(self):
        connection = None
        try:
            connection = psycopg2.connect(
                dbname=self.DB_URL,
                host=self.DB_HOSTNAME,
                port=self.DB_PORT,
                user=self.DB_USER,
                password=self.DB_PASS,
            )
        except psycopg2.OperationalError as e:
            print(e)
        return connection


def load_env() -> DBConfig:
    load_dotenv()
    DB_URL = os.getenv("DB_URL")
    if DB_URL is None:
        raise ValueError("Database URL not set")
    DB_HOSTNAME = os.getenv("DB_HOSTNAME")
    if DB_HOSTNAME is None:
        raise ValueError("Database hostname not set")
    DB_PORT = int(os.getenv("DB_PORT"))
    if DB_PORT is None:
        raise ValueError("Database port not set")
    DB_USERNAME = os.getenv("DB_USERNAME")
    if DB_USERNAME is None:
        raise ValueError("Database username not set")
    DB_PASS = os.getenv("DB_PASSWORD")
    if DB_PASS is None:
        raise ValueError("Database password not set")
    return DBConfig(DB_URL, DB_HOSTNAME, DB_PORT, DB_USERNAME, DB_PASS)