from fastapi import FastAPI
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


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
