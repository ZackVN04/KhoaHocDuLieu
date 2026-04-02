import json
from concurrent.futures import ThreadPoolExecutor, as_completed  
from crawler import crawl_job_links
from scraper import scrape_job_detail

# =========================
# VALIDATE DATA
# =========================
def is_valid_job(data):
    """
    Kiểm tra job có hợp lệ hay không
    → tránh dữ liệu rác
    """
    if not data:
        return False
    if not data["job_title"]:
        return False
    if data["company"] and "bài viết" in data["company"].lower():
        return False
    return True

# =========================
# MAIN CRAWLER
# =========================
def main():
    print("🚀 START CRAWLING...\n")

    # =====================
    # B1: LẤY LINK JOB
    # =====================
    job_links = crawl_job_links(max_pages=20)
    print(f"\n📌 Tổng link thu được: {len(job_links)}")

    jobs = []

    # =====================
    # B2: SCRAPE SONG SONG (MULTI-THREAD)
    # =====================
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [
            executor.submit(scrape_job_detail, link)
            for link in job_links
        ]

        for i, future in enumerate(as_completed(futures), 1):
            try:
                data = future.result()
                if is_valid_job(data):
                    jobs.append(data)
                print(f"[OK] {i}/{len(job_links)}")
            except Exception as e:
                print("[ERR]", e)

    # =====================
    # B3: LƯU FILE JSON
    # =====================
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(
            jobs,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(f"\n✅ DONE! Lưu {len(jobs)} jobs vào data/jobs.json")

if __name__ == "__main__":
    main()
