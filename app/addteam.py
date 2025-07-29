import sys
import psycopg2

from loadenv import load_env
from pokeparser import parser


create_query = """
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    mons TEXT[]
    );
"""

insert_query = """
INSERT INTO teams (author, title, mons)
VALUES (%s, %s, %s);
"""

check_query = """
SELECT * FROM teams WHERE title=%s;
"""


def isduplicate(connection, title: str) -> bool:
    cursor = connection.cursor()
    query = cursor.execute(check_query, (title,))
    cursor.close()
    return query is not None


def insert(connection, json: dict[str, str]) -> None:
    if isduplicate(connection, json["title"]):
        print(f"Team {json['title']} from url {url} already exists")
        return

    cursor = connection.cursor()
    cursor.execute(insert_query, (json["author"], json["title"], json["mons"]))

    cursor.close()
    connection.commit()


if __name__ == "__main__":
    if sys.argv.__len__() == 1:
        print("Provide urls as arguments to add team")
        sys.exit(1)
    urls = sys.argv[1:]
    config = load_env()
    connection = psycopg2.connect(config.DB_URL)
    for url in urls:
        json = parser.pasteJSON(url)
        insert(connection, json)
    connection.close()
