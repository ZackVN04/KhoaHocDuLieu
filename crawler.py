from urllib.parse import urljoin
import requests
from parsel import Selector

BASE_URL = "https://vieclamcantho.com.vn"
LIST_URL = "https://vieclamcantho.com.vn/viec-lam-can-tho-moi-nhat?page={}"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def get_html(url):
    return requests.get(url, headers=HEADERS, timeout=10).text


def crawl_job_links(max_pages=20):
    job_links = set()

    for page in range(1, max_pages + 1):
        url = LIST_URL.format(page)
        print("Crawling:", url)

        html = get_html(url)
        selector = Selector(html)

        links = selector.xpath("//a/@href").getall()

        for link in links:
            full_link = urljoin(BASE_URL, link)

            if "-tuyen-dung-" in full_link and full_link.endswith(".html"):
                job_links.add(full_link)

    return list(job_links)