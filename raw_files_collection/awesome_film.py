import re  # noqa: D100

import requests
from bs4 import BeautifulSoup

SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)


def get_movie_names_and_links_awesome_film(URL_AWESOME_FILM: str) -> dict:
    """Retreive script titles and links and append to a dictionary."""
    awesome_film_names_and_links = {}
    content = requests.get(URL_AWESOME_FILM).text
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.body.find_all("table")[15:18]
    for table in tables:
        tds = table.find_all("td", class_="tbl")
        for td in tds:
            try:
                movie_link = "http://www.awesomefilm.com/" + td.a["href"]
            except Exception:
                movie_link = "Not Found"
            movie_title = td.text.replace("\n", "").strip()
            if ":" in movie_title:
                movie_title = movie_title.replace(":", ": ")
            if movie_title.endswith(", The"):
                movie_title = movie_title.replace(", The", "")
                movie_title = "The " + movie_title
            if movie_title.endswith(", A"):
                movie_title = movie_title.replace(", A", "")
                movie_title = "A " + movie_title
            if re.search(SCRIPT_TYPE_MATCH, movie_title):
                movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()
            if re.search(EXTRA_SPACES_MATCH, movie_title):
                movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)
            if movie_title.endswith("-"):
                movie_title = movie_title[:-1].strip()
            if (
                "pdf" not in movie_title
                and "doc" not in movie_title
                and movie_title != "email"
                and movie_title != ""
            ):
                awesome_film_names_and_links[movie_title] = movie_link
    return awesome_film_names_and_links


def get_raw_files_awesome_film(awesome_film_names_and_links: dict) -> None:
    """Retrieve html structure from script links and write raw html to files."""
    for movie_title in awesome_film_names_and_links:
        script_url = awesome_film_names_and_links[movie_title]
        content = requests.get(script_url).text
        soup = BeautifulSoup(content, "html.parser")
        file_name = "_".join(movie_title.strip().split()) + ".html"
        with open(f"rawfiles/{file_name}", "w", encoding="utf-8") as f:
            f.write(str(soup).strip())


awesome_film_names_and_links = get_movie_names_and_links_awesome_film(
    "http://www.awesomefilm.com/"
)
get_raw_files_awesome_film(awesome_film_names_and_links)
