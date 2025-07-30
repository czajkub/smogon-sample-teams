import sys

from bs4 import BeautifulSoup
import requests


def toJSON(url: str) -> dict[str, str]:
    response = requests.get(url)

    if response.status_code != 200:
        print(f"url returned status {response.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string
    author = soup.h2.text[4:]

    mons = []
    pres = soup.find_all("pre")
    for pre in pres:
        nextelement: str = pre.find_next().text
        if nextelement == "Ability: ":
            line: str = pre.text
            if line.find("@") != -1:
                if line.find("(") != -1:
                    mons.append(line[line.find("(") + 1 : line.find(")")].strip())
                else:
                    mons.append(line[: line.find("@")].strip())
            else:
                if line.find("(") != -1:
                    mons.append(line[line.find("(") : line.find(")")].strip())
                else:
                    mons.append(line[: line.find("\n")].strip())
        else:
            mons.append(nextelement)

    return {"mons": mons, "author": author, "title": title}


def main():
    if sys.argv.__len__() != 2:
        print("Provide only 1 argument: pokepaste url")
        sys.exit(1)
    url = sys.argv[1]
    print(toJSON(url))


if __name__ == "__main__":
    main()
