import sys
import psycopg2

from loadenv import load_env
from pokeparser import parser
import queries as q


def isduplicate(cursor, url: str) -> bool:
    cursor.execute(q.check_query, (url,))
    return cursor.fetchone() is not None


def insert(
    connection, json: dict[str, str], gen: int | None = 9, psformat: str | None = "OU"
) -> bool:
    cursor = connection.cursor()
    if isduplicate(cursor, json["url"]):
        print(f"Team {json['title']} from url {json['url']} already exists in database")
        return False

    cursor.execute(
        q.addteam_query,
        (json["author"], json["title"], json["mons"], json["url"], gen, psformat),
    )

    cursor.close()
    connection.commit()
    print(f"Team {json['title']} from url {json['url']} inserted into database")
    return True


def addteam(connection, url: str, gen: int, psformat: str) -> bool:
    json = parser.toJSON(url)
    json.update({"url": url})
    return insert(connection, json, gen, psformat)


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
