import re
import requests
from parsel import Selector

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})


def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def clean_html(text):
    if not text:
        return ""

    # xóa tag HTML
    text = re.sub(r"<.*?>", " ", text)

    # xóa khoảng trắng dư
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_company_from_url(url):
    try:
        slug = url.split("/")[-1]
        company_part = slug.split("-tuyen-dung-")[0]
        company = company_part.replace("-", " ")
        return company.title()
    except:
        return "Không rõ"


def scrape_job_detail(url):
    try:
        html = session.get(url, timeout=10).text
        selector = Selector(html)

        # ===== JOB TITLE =====
        job_title = clean_text(selector.xpath("//h1/text()").get())

        # ===== COMPANY =====
        company = clean_text(
            selector.xpath("//h1/following::h2[1]//text()").get()
        )

        # fallback từ HTML
        if not company:
            company = clean_text(
                selector.xpath("//*[contains(text(),'Công ty')]/following::text()[1]").get()
            )

        # fallback từ URL (quan trọng nhất)
        if not company:
            company = extract_company_from_url(url)

        # ===== FULL TEXT =====
        full_text = clean_text(selector.xpath("string(.)").get())

        # ===== SALARY =====
        salary = ""
        m = re.search(r"Mức lương:\s*(.+?)\s*(Hạn nộp|Kinh nghiệm)", full_text, re.S)
        if m:
            salary = clean_text(m.group(1))

        # ===== DESCRIPTION =====
        description = ""
        m = re.search(r"Mô tả công việc\s*(.+?)\s*(Yêu cầu công việc|Quyền lợi)", full_text, re.S)
        if m:
            description = m.group(1)

        if not description:
            desc = selector.xpath(
                "//*[contains(text(),'Mô tả công việc')]/following::div[1]//text()"
            ).getall()
            description = " ".join(desc)

        description = clean_html(description)

        return {
            "job_title": job_title,
            "company": company,
            "salary": salary,
            "description": description,
            "url": url
        }

    except Exception as e:
        print("Lỗi:", url, e)
        return None