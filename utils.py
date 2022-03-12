import requests
from gzip import decompress
from warcio.archiveiterator import ArchiveIterator


def url_is_trustworthy(url: str) -> bool:
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
        "who.int",
        "kff.org",
        "cdc.org",
        "usa.org",
    ]
    for source in trustworthy_sources:
        if source in url:
            return True
    return False


def get_warc_urls(time: str) -> list[str]:
    """
    Fetch the warc file paths in the specified year and number, decompress it,
    and return the warc urls

    get_warc_paths("2020-05")
    """

    file_name = (
        f"https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-{time}/warc.paths.gz"
    )

    # Fetch and decompress the gzip file
    gzip_file = requests.get(file_name).content

    # Convert bytes to string
    file_contents = decompress(gzip_file).decode("utf-8")

    # Add "https://commoncrawl.s3.amazonaws.com/" before each url
    return list(
        map(
            lambda path: "https://commoncrawl.s3.amazonaws.com/" + path,
            file_contents.split("\n"),
        )
    )


def get_warc_urls_multiple(times: list[str]) -> list[str]:
    urls = []
    for time in times:
        urls = urls + get_warc_urls(time)
    return urls
