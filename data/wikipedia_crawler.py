import sys
import time
import argparse
import re
from urllib.parse import urlparse
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from constants import USER_AGENT

visited_urls = set()  # all urls already visited, to not visit twice
pending_urls = []  # queue


def load_urls(session_file):
    """Resume previous session if any, load visited URLs"""

    try:
        with open(session_file) as fin:
            for line in fin:
                visited_urls.add(line.strip())
    except FileNotFoundError:
        pass


def scrap(base_url, article, output_file, session_file):
    """Represents one request per article"""

    full_url = base_url + article
    headers = {"User-Agent": USER_AGENT}
    if "zh" in base_url:
        headers["Accept-Language"] = "zh-CN,zh-Hans;q=0.9"

    # Try the request up to N times before skipping. Use a short
    # exponential backoff between attempts. Do not prompt the user; if
    # all attempts fail, skip this URL automatically.
    max_attempts = 10
    r = None
    for attempt in range(1, max_attempts + 1):
        try:
            # add a timeout so the request fails fast on network issues
            r = requests.get(full_url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            # includes ConnectionError, Timeout, SSLError, etc.
            print(
                f"Request attempt {attempt}/{max_attempts} failed for {full_url}: {e}"
            )
            if attempt == max_attempts:
                print(
                    f"Skipping {full_url} after {max_attempts} failed attempts."
                )
                return
            # exponential backoff (cap at 30s)
            backoff = min(2 ** (attempt - 1), 30)
            time.sleep(backoff)
            continue

        # If we got a response but an unexpected status code, retry too
        if r.status_code not in (200, 404):
            print(
                f"Request attempt {attempt}/{max_attempts} for {full_url} returned status {r.status_code}"
            )
            if attempt == max_attempts:
                print(
                    f"Skipping {full_url} after {max_attempts} attempts (last status: {r.status_code})."
                )
                return
            backoff = min(2 ** (attempt - 1), 30)
            time.sleep(backoff)
            continue

        # success (status 200 or 404) -> proceed
        break

    soup = BeautifulSoup(r.text, "html.parser")
    content_list = soup.find_all("div", {"id": "mw-content-text"})

    if not content_list:
        # defensive: if structure changed or a non-article page was returned
        print("No article content found for", full_url)
        return

    with open(session_file, "a") as fout:
        fout.write(full_url + "\n")  # log URL to session file

    # add new related articles to queue
    # check if are actual articles URL
    for content in content_list:
        for a in content.find_all("a"):
            href = a.get("href")
            if not href:
                continue
            if href[0:6] != "/wiki/":  # allow only article pages
                continue
            elif ":" in href:  # ignore special articles e.g. 'Special:'
                continue
            elif (
                href[-4:] in ".png .jpg .jpeg .svg"
            ):  # ignore image files inside articles
                continue
            elif base_url + href in visited_urls:  # already visited
                continue

            if href in pending_urls:  # already added to queue
                continue
            pending_urls.append(href)

    # skip if already added text from this article, as continuing session
    if full_url in visited_urls:
        return
    visited_urls.add(full_url)

    parenthesis_regex = re.compile("\(.+?\)")  # to remove parenthesis content
    citations_regex = re.compile("\[.+?\]")  # to remove citations, e.g. [1]

    # get plain text from each <p>
    p_list = content.find_all("p")
    with open(output_file, "a", encoding="utf-8") as fout:
        for p in p_list:
            text = p.get_text().strip()
            text = parenthesis_regex.sub("", text)
            text = citations_regex.sub("", text)
            if text:
                fout.write(text + "\n\n")  # extra line between paragraphs


def main(initial_url, articles_limit, interval, output_dir):
    """Main loop, single thread"""

    minutes_estimate = interval * articles_limit / 60
    print(
        "This session will take {:.1f} minute(s) to download {} article(s):".format(
            minutes_estimate, articles_limit
        )
    )
    print("\t(Press CTRL+C to pause)\n")

    output_file = output_dir / "text.txt"
    session_file = output_dir / "session.txt"
    load_urls(session_file)  # load previous session (if any)
    base_url = "{uri.scheme}://{uri.netloc}".format(uri=urlparse(initial_url))
    initial_url = initial_url[len(base_url) :]
    pending_urls.append(initial_url)

    counter = 0
    while len(pending_urls) > 0:
        try:
            counter += 1
            if counter > articles_limit:
                break
            try:
                next_url = pending_urls.pop(0)
            except IndexError:
                break

            time.sleep(interval)
            article_format = next_url.replace("/wiki/", "")[:35]
            print("{:<7} {}".format(counter, article_format))
            scrap(base_url, next_url, output_file, session_file)
        except KeyboardInterrupt:
            input("\n> PAUSED. Press [ENTER] to continue...\n")
            counter -= 1

    print("Finished!")
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--initial_url",
        default="https://en.wikipedia.org/wiki/Biology",
        help="Initial Wikipedia article URL",
    )
    parser.add_argument(
        "-a",
        "--articles",
        nargs="?",
        default=1,
        type=int,
        help="Total number articles to be extrated",
    )
    parser.add_argument(
        "-i",
        "--interval",
        nargs="?",
        default=5.0,
        type=float,
        help="Interval between requests (seconds)",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        default="data/",
        help="Output directory",
        type=Path,
    )
    args = parser.parse_args()

    main(
        args.initial_url,
        args.articles,
        args.interval,
        args.output,
    )
