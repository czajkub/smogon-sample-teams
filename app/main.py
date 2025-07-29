from fastapi import FastAPI
import psycopg2
from loadenv import load_env

app = FastAPI()

config = load_env()
connection = config.connect()

@app.get("/team")
def get_team():
    cursor = connection.cursor()
    cursor.execute("SELECT team FROM teams")
    team = cursor.fetchall()
    cursor.close()
    print(team)
    return team