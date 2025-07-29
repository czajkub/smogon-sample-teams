import sys
import re

from bs4 import BeautifulSoup
import requests

from .utils import *
# from utils import *

def toJSON(url: str) -> dict[str, str]:
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
        if span.text in items:
            continue
        mons.append(span.text)

    return {"mons": mons, "author": author, "title": title}


def main():
    if sys.argv.__len__() != 2:
        print("Provide only 1 argument: pokepaste url")
        sys.exit(1)
    url = sys.argv[1]
    print(toJSON(url))


if __name__ == "__main__":
    main()
