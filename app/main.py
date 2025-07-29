from typing import List
from pydantic import BaseModel
import psycopg2
from fastapi import FastAPI

from loadenv import load_env

app = FastAPI()


class Team(BaseModel):
    title: str
    author: str
    mons: List[str]
    url: str


@app.get("/team")
def get_team(onlyone: bool = True, title: str | None = None, author: str = None, mons: List[str] = None):
    config = load_env()
    connection = psycopg2.connect(config.DB_URL)
    cursor = connection.cursor()
    query = f"SELECT {1 if onlyone else '*'} FROM teams"
    if title:
        query += f" WHERE title LIKE '{title}'"
    if author:
        query += f" WHERE author LIKE '{author}'"
    if mons:
        for mon in mons:
            query += f" WHERE {mon} = ANY(mons)"
    cursor.execute(query)
    team = cursor.fetchall()
    cursor.close()
    connection.close()
    # print(team)
    return team


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
