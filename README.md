# COVID-19's Economic Impact 

## Goal

Find pages from the [common crawl archive](https://commoncrawl.org/) that discuss or are relevant to COVID-19’s economic impact.

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