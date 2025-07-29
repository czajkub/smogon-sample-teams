create_query = """
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    author TEXT NOT NULL,
    title TEXT NOT NULL,
    mons TEXT[]
    );
"""

insert_query = """
INSERT INTO teams (author, title, mons, url)
VALUES (%s, %s, %s, %s);
"""

check_query = """
SELECT * FROM teams WHERE title=%s;
"""
