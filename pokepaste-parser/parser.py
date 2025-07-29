import sys
import json
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


def pasteJson(url: str):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"url returned status {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string
    print(f"title = {title}")

    cos = soup.find_all("span", attrs={"class": "type-electric"})
    cos2 = soup.find_all("span", attrs={"class": re.compile("type-*")})
    # print(cos2)
    author = soup.h2.text[4:]
    print(author)

    mons = []
    for span in cos2:
        if span.text == "-":
            continue
        if span.text in types:
            continue
        mons.append(span.text)

    print({"mons": mons, "author": author, "title": title})


if __name__ == "__main__":
    if sys.argv.__len__() != 2:
        print("Provide only 1 argument: pokepaste url")
        sys.exit(1)
    url = sys.argv[1]
    pasteJson(url)
