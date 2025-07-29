from loadenv import load_env

config = load_env()
connection = config.connect()

cursor = connection.cursor()
cursor.execute("CREATE TABLE products("
               "id SERIAL PRIMARY KEY,"
               "teamname TEXT NOT NULL,"
               "author TEXT NOT NULL,"
               "mons TEXT[]"
)
cursor.close()
connection.commit()