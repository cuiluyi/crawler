# Wikipedia Crawler

A lightweight Python crawler for fetching and cleaning article text from English and Chinese Wikipedia. The crawler uses a single-threaded, request-based approach with session resumption and retry mechanisms. Cleaned text is suitable for downstream analysis like entropy or Zipf's law.

## Requirements

- Python 3
- Third-party libraries:
  - `requests` for HTTP requests and handling timeouts/exceptions
  - `beautifulsoup4` for HTML parsing and DOM extraction
  - `jieba` for Chinese word segmentation in analysis
- Install dependencies: `pip install requests beautifulsoup4 jieba`

Constants like `USER_AGENT` are defined in `constants.py` to simulate a common browser user agent.

## Quick Start

Run the bash scripts to start crawling:

- Chinese Wikipedia: `bash scripts/zh_scrawler.sh`
- English Wikipedia: `bash scripts/en_scrawler.sh`

These scripts call `wikipedia_crawler.py` with predefined parameters.

## Usage

The main script is `wikipedia_crawler.py`. Run it with:

```bash
python wikipedia_crawler.py --initial_url <URL> --articles <N> --interval <SECONDS> --output <DIR>
```

- `--initial_url`: Starting Wikipedia page URL (required).  
  Example for English: `https://en.wikipedia.org/wiki/Donald_Trump`  
  Example for Chinese (URL-encoded): `https://zh.wikipedia.org/wiki/%E5%94%90%E7%B4%8D%C2%B7%E5%B7%9D%E6%99%AE`

- `--articles`: Maximum number of articles to fetch (default: no limit).

- `--interval`: Sleep time between requests in seconds (default: 5) to reduce server load.

- `--output`: Output directory (default: current directory).

### Crawling Strategy

- Uses BFS-style traversal starting from the initial URL.
- Filters links: Only `/wiki/` paths, excluding those with `:`, image suffixes (`.png`, `.jpg`, `.jpeg`, `.svg`), or non-article pages.
- Extracts text from `<div id="mw-content-text">` paragraphs, cleans by removing bracketed content and citations via regex.
- Session management: Loads/ saves visited URLs from `session.txt` to resume and avoid duplicates.

### Robustness

- Retries up to 10 times on failures with exponential backoff (max 30s).
- Customizable interval to avoid rate limiting.

**Note for Chinese Wikipedia:** To fetch simplified Chinese, add `"Accept-Language": "zh-CN,zh-Hans;q=0.9"` to request headers in the script.

## Output

- `text.txt`: Cleaned paragraph text (paragraphs separated by blank lines).
- `session.txt`: List of visited URLs for resumption.

English output in `data/en`, Chinese in `data/zh` by default.

## Analysis

To compute statistics on the crawled data (e.g., entropy, word/character probability distributions, and Zipf's law plots for English and Chinese), run:

```bash
python main.py
```

This processes up to 10,000,000 characters from the output text files, using spaces for English tokenization and `jieba` for Chinese. Results include tables and figures saved in `figures/en` and `figures/zh`. For example:

![image-20251106121126850](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106122833248.png)

![image-20251106121008533](https://tianchou.oss-cn-beijing.aliyuncs.com/img/20251106122833206.png)

## Repository Structure

- `scripts/`: Bash starters (`en_scrawler.sh`, `zh_scrawler.sh`).
- `constants.py`: User agent and other constants.
- `data/`: Output folders (`en/`, `zh/`).
- `figures/`: Analysis output folders (`en/`, `zh/`).
- `wikipedia_crawler.py`: Core crawler script.
- `main.py`: Analysis script for computing experiment results.
