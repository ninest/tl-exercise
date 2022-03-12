from concurrent import futures
import requests
from gzip import decompress
from warcio.archiveiterator import ArchiveIterator
from bs4 import BeautifulSoup

from utils import get_warc_urls, get_warc_urls_multiple

# warc_paths = get_warc_urls("2020-05")
warc_paths = get_warc_urls_multiple(
    [
        # "2020-05",
        # "2020-10",
        # "2020-16",
        # "2020-24",
        # "2020-29",
        "2020-34",
        "2020-40",
        "2020-45",
        "2020-50",
    ]
)


trustworthy_sources = [
    "economist.com",
    "nytimes.com",
    "forbes.com",
    "apnews.com",
    "bbc.com",
    "usatoday.com",
    "wsj.com",
    "reuters.com",
    "foxnews.com",
    "cnn.com",
    "npr.com",
    "pbs.com",
    "cbsnews.com",
    "theguardian.com",
    "nbcnews.com",
    "latimes.com",
    "wikinews.org",
    "therealnews.com",
    "c-span.org",
]


def url_is_trustworthy(url: str) -> bool:
    for source in trustworthy_sources:
        if source in url:
            return True
    return False


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

            # if not ((".com/" in url) or (".org/" in url)):
            # continue
            if not url_is_trustworthy(url):
                continue

            contents = record.content_stream().read().decode("utf-8", "replace").lower()
            soup = BeautifulSoup(contents)
            body = soup.body
            if not body:
                continue
            article_text = body.text

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

            print(url)


find_articles(warc_paths)
