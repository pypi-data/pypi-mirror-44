import argparse
import concurrent.futures
from collections import deque
import threading
import requests
from bs4 import BeautifulSoup

DEFAULT_PARALLELISM = 25

lock = threading.Lock()


class WebCrawler:

    def __init__(self, base_url, parallelism=DEFAULT_PARALLELISM):

        self.base_url = base_url + '/' if not base_url.endswith('/') else base_url
        self.parallelism = parallelism
        self.to_be_processed = set()
        self.to_be_processed.add(self.base_url)
        self.urls_dq = deque([[self.base_url]])

    def load_url(self, url, timeout):
        response = requests.get(url, timeout=timeout)
        if not response or response.status_code != 200 or not response.text:
            return []
        return self.collect_urls_from_page(response.text)

    def collect_urls_from_page(self, rich_text):
        # Collect all url from the current page, and add them to the queue

        # lxml parser
        soup = BeautifulSoup(rich_text, 'lxml')
        urls_to_crawl = []
        for a_href in (a for a in soup.find_all('a', href=True) if a['href'].startswith('http')):
            with lock:
                href = a_href['href'] + '/' if not a_href['href'].endswith('/') else a_href['href']
                if href not in self.to_be_processed:
                    urls_to_crawl.append(href)
                    self.to_be_processed.add(href)

        return urls_to_crawl

    @staticmethod
    def process_urls(crawled_url, urls_to_crawl):
        print(crawled_url)
        if urls_to_crawl:
            for url_to_crawl in urls_to_crawl:
                print('{spacer}{url_to_crawl}'.format(spacer='\t', url_to_crawl=url_to_crawl))

    def crawl(self):
        """
        Crawls links embedded within webpages in parallel and then print to stdout
        """
        while True:
            try:
                # pops out list of urls to crawl
                urls_list = self.urls_dq.popleft()
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.parallelism) as executor:
                    future_to_url = {executor.submit(self.load_url, url, 60): url for url in urls_list}
                    for future in concurrent.futures.as_completed(future_to_url):
                        crawled_url = future_to_url[future]
                        try:
                            urls_to_crawl = future.result()
                        except Exception as exc:
                            print('%r generated an exception: %s' % (crawled_url, exc))
                        else:
                            WebCrawler.process_urls(crawled_url, urls_to_crawl)
                            if urls_to_crawl:
                                # append list of urls to crawl to deque
                                self.urls_dq.append(urls_to_crawl)
            except IndexError:
                # no more urls to crawl
                break


def get_args(parser):
    parser.add_argument(
        'base_url',
        type=str,
        action='store',
        help='The base url')
    parser.add_argument(
        '--parallelism',
        action='store',
        type=int,
        help='The number of worker threads to run in parallel',
        default=DEFAULT_PARALLELISM)
    return parser.parse_args()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Web crawler')
    parsed_args = get_args(arg_parser)
    WebCrawler(parsed_args.base_url, parsed_args.parallelism).crawl()
