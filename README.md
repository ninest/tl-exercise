# COVID-19's Economic Impact

## Goal

Find pages from the [common crawl archive](https://commoncrawl.org/) that discuss or are relevant to COVID-19’s economic impact.

### Assumptions

- Finding news articles from trustworthy sources related to COVID-19's economic impact

## Steps

### 1. Extracting data from Common Crawl

The [Common Crawl dataset](https://commoncrawl.org/the-data/get-started/) is stored per month and year, with each of these timeframes containing WARC files. These WARC files are in the `.gz` format, and can be decompressed to get a list of a WARC files containing content.

To extract data from the `.gz` files, I used Python's `gzip` library. Decompressing. I created a function `get_warc_urls` for this task.

Next, we need to to go through the content in the WARC files. We can do this with the `warcio` library. For example:

```python
warc_paths = get_warc_urls("2020-05")
path = warc_paths[1] # Only get the first path for this example

stream = requests.get(s, stream=True).raw

for record in ArchiveIterator(stream):
  ...
```

Using examples from the [provided code](https://github.com/code402/warc-benchmark/blob/master/python/go.py), I was able to find the contents of the crawled pages:

```python
for record in ArchiveIterator(stream):
  if record.rec_type == "warcinfo":
    continue
  url = record.rec_headers.get_header("WARC-Target-URI")
  contents = record.content_stream().read().decode("utf-8", "replace").lower()
  print(url)
```

### 2. Filtering articles based on content

I thought that searching for specific words would help us filter through the articles appropriately. For example, searching for "covid" along with either "economic", "economy", "gdp", or similar words should fetch us articles related to the economic impacts of COVID-19. However, non-news websites also contained these words. Additionally, even if a specific article was not related to COVID-19, they may have navigational elements containing words we are looking for.

```python
for record in ArchiveIterator(stream):
  ...
  contents = record.content_stream().read().decode("utf-8", "replace").lower()
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
```

To reduce the number of incorrect results, I found a list of the most trustworthy news sites and created a function `url_is_trustworthy`, which determines if a website is trustworthy.

While this did provide some useful results, the problem of having words like "covid" in navigational elements or other elements that are not part of the news article persisted. One possible solution to this is to only search for the words in the website's `article` HTML tag.

```python
soup = BeautifulSoup(contents)
article = soup.find("article")
article_text = article.text
...
```

This change definitely displayed for relevant results. Another issue was articles published before 2020 were being shown too, likely because they were crawled again in 2020. The `WARC-Date` field shows the date the webpage was crawled rather than its actual publish date.

Finding the page's publish data would require finding abd extracting the date in the HTML. This is, however, a different process for each website. One solution would be to use a pre-existing library such as [Mercury Parse](https://github.com/postlight/mercury-parser). However, there is only a Nodejs version.

Another method would be to simply check if "2020" is in the article URL. This works for the set of news sources, but will not work across all webpages if they do not have the publishing date in the URL.

## Extending the project

If I had more time to work on this assignment, I would explore the following:

- Include more words relating to COVID-19 and economic impacts to better search for articles on the topic. I would manually find articles and find out the most common words across them.
- Differentiate between articles and "listing pages" (web pages that only link to other pages but do not provide information on their own)