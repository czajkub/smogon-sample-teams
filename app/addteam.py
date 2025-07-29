import sys
import psycopg2

from loadenv import load_env
from pokeparser import parser
import queries as q


def isduplicate(cursor, title: str) -> bool:
    cursor.execute(q.check_query, (title,))
    return cursor.fetchone() is not None


def insert(connection, json: dict[str, str]) -> None:
    cursor = connection.cursor()
    if isduplicate(cursor, json["title"]):
        print(f"Team {json['title']} from url {json['url']} already exists in database")
        return

    cursor.execute(
        q.insert_query, (json["author"], json["title"], json["mons"], json["url"])
    )

    cursor.close()
    connection.commit()
    print(f"Team {json['title']} from url {json['url']} inserted into database")


def main():
    if sys.argv.__len__() == 1:
        print("Provide urls as arguments to add team")
        sys.exit(1)
    urls = sys.argv[1:]
    config = load_env()
    connection = psycopg2.connect(config.DB_URL)
    for url in urls:
        json = parser.toJSON(url)
        json.update({"url": url})
        insert(connection, json)
    connection.close()


if __name__ == "__main__":
    main()
