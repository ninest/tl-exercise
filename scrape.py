import requests
from datetime import datetime
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup

from file import append_to_file, create_file
from utils import get_warc_urls_multiple, url_is_trustworthy

warc_paths = get_warc_urls_multiple(
    [
        "2020-05",
        "2020-10",
        "2020-16",
        "2020-24",
        "2020-29",
        "2020-34",
        "2020-40",
        "2020-45",
        "2020-50",
    ]
)


def find_articles(warc_paths: list[str]):
    """
    Fetch each warc path provided and find all records following the provided conditions
    """

    for path in warc_paths:
        stream = requests.get(path, stream=True).raw
        for record in ArchiveIterator(stream):
            if record.rec_type == "warcinfo":
                continue

            url = record.rec_headers.get_header("WARC-Target-URI")

            if not url_is_trustworthy(url):
                continue

            if not "2020" in url:
                continue

            contents = record.content_stream().read().decode("utf-8", "replace").lower()
            soup = BeautifulSoup(contents)
            article = soup.find("article")
            if not article:
                continue
            article_text = article.text

            # conditions for COVID-19 and economic effects
            conditions = ("covid" in article_text) and (
                ("economic" in article_text)
                or ("economy" in article_text)
                or ("gdp" in article_text)
                or ("job" in article_text)
                or ("employ" in article_text)
            )

            if not conditions:
                continue

            # Find the month of crawl
            date_string = record.rec_headers.get_header("WARC-Date").split("T")[0]
            date = datetime.fromisoformat(date_string)

            string = f"{date.strftime('%B %Y')} {url}"

            # Append the result to the file
            print(string)
            append_to_file("results.txt", string)


create_file("results.txt")
find_articles(warc_paths)
print("Done.")