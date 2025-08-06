from typing import List, Tuple, Any
import re
from pydantic import BaseModel
import psycopg2
from fastapi import FastAPI

from loadenv import load_env
from queries import get_query
import addteam

app = FastAPI()


class Team(BaseModel):
    title: str
    author: str
    mons: List[str]
    url: str


@app.get("/get_team/")
def get_team(
    onlyone: bool = True,
    title: str | None = None,
    author: str | None = None,
    mons: str | None = None,
    gen: int | None = 9,
    format: str | None = "OU",
) -> List[Team] | None:
    config = load_env()
    connection = psycopg2.connect(config.DB_URL)
    cursor = connection.cursor()
    query: str = get_query(title, author, mons, gen, format)
    cursor.execute(query)
    results: List[Tuple[Any, ...]] = cursor.fetchall()
    print(results)
    cursor.close()
    connection.close()

    if len(results) == 0:
        return None

    if onlyone:
        return selectone(results)

    teams: List[Team] = []
    for result in results:
        teams.append(
            Team(author=result[0], title=result[1], mons=result[2], url=result[3])
        )
    return teams


@app.post("/add_team/")
def add_team(url: str, gen: int = 9, format: str = "OU"):
    config = load_env()
    connection = psycopg2.connect(config.DB_URL)

    if re.match(r"^https://pokepast\.es/[a-z0-9]*$", url) is None:
        return {"message": "provide valid URL", "status_code": 400}

    inserted: bool = addteam.addteam(connection, url, gen, format)
    connection.close()
    if inserted:
        return {"message": "team added successfully", "status_code": 201}
    else:
        return {"message": "team already exists in database", "status_code": 400}


@app.get("/")
def read_root():
    return {"Hello": "World"}


def selectone(results: List[Tuple[Any, ...]]) -> List[Team]:
    size = len(results)
    index = randint(0, size - 1)
    result = results[index]
    return [Team(author=result[0], title=result[1], mons=result[2], url=result[3])]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
