from re import split
from typing import List, Tuple, Any
from random import randint

from main import Team

create_query = """
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    mons TEXT[]
    );
"""

insert_query = """
INSERT INTO teams (author, title, mons, url, gen, format)
VALUES (%s, %s, %s, %s, %s, %s);
"""

addteam_query = """
    EXECUTE addteam (%s, %s, %s, %s, %s, %s)
"""

check_query = """
SELECT * FROM teams WHERE url=%s;
"""


def get_query(
    title: str | None, author: str | None, mons: str | None,
        gen: int | None, format: str | None
) -> str:
    query = f"SELECT * FROM teams"
    whereflag: bool = False
    if title:
        query += f" WHERE title LIKE '{title}'"
        whereflag = True
    if author:
        query += " AND" if whereflag else " WHERE"
        query += f" author LIKE '{author}'"
        whereflag = True
    if mons:
        monlist = split(r"\s*,\s*", mons)
        query += " AND" if whereflag else " WHERE"
        query += f" '{monlist[0]}' = ANY(mons)"
        for mon in monlist[1:]:
            query += f" AND '{mon}' = ANY(mons)"
        whereflag = True
    if gen:
        query += " AND" if whereflag else " WHERE"
        query += f" gen LIKE '{gen}'"
        whereflag = True
    if format:
        query += " AND" if whereflag else " WHERE"
        query += f" format LIKE '{format}'"

    return query


def selectone(results: List[Tuple[Any, ...]]) -> List[Team]:
    size = len(results)
    index = randint(0, size - 1)
    result = results[index]
    return [Team(author=result[0], title=result[1], mons=result[2], url=result[3])]
