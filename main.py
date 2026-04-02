# main.py (CRAWLER)

import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from crawler import crawl_job_links
from scraper import scrape_job_detail


# =========================
# VALIDATE DATA
# =========================
def is_valid_job(data):
    """
    Kiểm tra dữ liệu job hợp lệ
    """

    #  data None hoặc rỗng
    if not data:
        return False

    #  tránh lỗi KeyError
    job_title = data.get("job_title", "")
    company = data.get("company", "")

    #  không có tiêu đề → bỏ
    if not job_title:
        return False

    #  loại bài viết rác
    if company and "bài viết" in company.lower():
        return False

    return True


# =========================
# MAIN CRAWLER
# =========================
def main():
    print(" START CRAWLING...\n")

    # =====================
    # B1: LẤY LINK JOB
    # =====================
    job_links = crawl_job_links(max_pages=20)

    print(f" Tổng link thu được: {len(job_links)}\n")

    jobs = []

    # =====================
    # B2: SCRAPE SONG SONG
    # =====================
    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = {
            executor.submit(scrape_job_detail, link): link
            for link in job_links
        }

        for i, future in enumerate(as_completed(futures), 1):
            link = futures[future]

            try:
                data = future.result()

                if is_valid_job(data):
                    jobs.append(data)

                print(f"[OK] {i}/{len(job_links)}")

            except Exception as e:
                print(f"[ERR] {link} → {e}")

    # =====================
    # B3: LỌC TRÙNG (OPTIONAL)
    # =====================
    # loại job trùng theo URL
    unique_jobs = []
    seen_urls = set()

    for job in jobs:
        url = job.get("url")

        if url and url not in seen_urls:
            unique_jobs.append(job)
            seen_urls.add(url)

    print(f"\n Sau khi lọc trùng: {len(unique_jobs)} jobs")

    # =====================
    # B4: LƯU JSON
    # =====================
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(
            unique_jobs,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\n DONE! Lưu {len(unique_jobs)} jobs vào data/jobs.json")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()