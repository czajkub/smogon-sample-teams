import sys
import re

from bs4 import BeautifulSoup
import requests


types = [
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel",
    "Fairy",
    "Stellar",
]


def pasteJSON(url: str) -> dict[str, str]:
    response = requests.get(url)

    if response.status_code != 200:
        print(f"url returned status {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string
    author = soup.h2.text[4:]

    mons = []
    spans = soup.find_all("span", attrs={"class": re.compile("type-*")})

    for span in spans:
        if span.text == "-":
            continue
        if span.text in types:
            continue
        mons.append(span.text)

    return {"mons": mons, "author": author, "title": title}


if __name__ == "__main__":
    if sys.argv.__len__() != 2:
        print("Provide only 1 argument: pokepaste url")
        sys.exit(1)
    url = sys.argv[1]
    pasteJSON(url)
