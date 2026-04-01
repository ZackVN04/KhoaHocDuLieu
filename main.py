import json  # dùng để lưu dữ liệu ra file JSON
from concurrent.futures import ThreadPoolExecutor, as_completed  
# ThreadPoolExecutor: chạy đa luồng → crawl nhanh hơn

from crawler import crawl_job_links  # lấy danh sách link job
from scraper import scrape_job_detail  # lấy chi tiết từng job


# =========================
# VALIDATE DATA
# =========================
def is_valid_job(data):
    """
    Kiểm tra job có hợp lệ hay không
    → tránh dữ liệu rác
    """

    # nếu data rỗng → bỏ
    if not data:
        return False

    # nếu không có tiêu đề → bỏ
    if not data["job_title"]:
        return False

    # loại bài viết không phải job thật
    # ví dụ: "bài viết chia sẻ..."
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

    jobs = []  # danh sách job sau khi scrape

    # =====================
    # B2: SCRAPE SONG SONG (MULTI-THREAD)
    # =====================
    # max_workers=10 → chạy 10 luồng cùng lúc
    with ThreadPoolExecutor(max_workers=10) as executor:

        # tạo danh sách task
        futures = [
            executor.submit(scrape_job_detail, link)
            for link in job_links
        ]

        # xử lý từng kết quả khi hoàn thành
        for i, future in enumerate(as_completed(futures), 1):
            try:
                data = future.result()  # lấy kết quả scrape

                # kiểm tra dữ liệu hợp lệ
                if is_valid_job(data):
                    jobs.append(data)

                print(f"[OK] {i}/{len(job_links)}")

            except Exception as e:
                # nếu lỗi → in ra nhưng không crash chương trình
                print("[ERR]", e)

    # =====================
    # B3: LƯU FILE JSON
    # =====================
    # ⚠️ lưu vào thư mục data/
    with open("data/jobs.json", "w", encoding="utf-8") as f:
        json.dump(
            jobs,
            f,
            ensure_ascii=False,  # giữ tiếng Việt
            indent=2             # format đẹp
        )

    print(f"\n✅ DONE! Lưu {len(jobs)} jobs vào data/jobs.json")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()