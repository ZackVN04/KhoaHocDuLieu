# nlp_main.py

import json
from preprocess import preprocess_text
from keyword_extractor import extract_keywords
from tfidf_extractor import extract_tfidf_keywords


# =========================
# 1. LOAD DATA
# =========================
def load_jobs(file_path="data/jobs.json"):
    """
    Đọc file jobs.json từ crawler
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# 2. PROCESS NLP
# =========================
def process_jobs(jobs):
    """
    Xử lý toàn bộ danh sách job:
    - preprocess
    - extract keywords (frequency)
    - extract keywords (TF-IDF)
    """

    results = []
    docs = []
    valid_jobs = []

    # =====================
    # B1: PREPROCESS ALL JOBS
    # =====================
    for job in jobs:
        text = job.get("description", "")

        if not text:
            continue

        tokens = preprocess_text(text)

        if not tokens:
            continue

        clean_text = " ".join(tokens)

        docs.append(clean_text)
        valid_jobs.append(job)

    #  tránh crash nếu không có dữ liệu
    if not docs:
        print(" No valid documents after preprocessing")
        return []

    print(f"✔ Valid jobs after preprocess: {len(valid_jobs)}")

    # =====================
    # B2: TF-IDF
    # =====================
    tfidf_results = extract_tfidf_keywords(docs, top_n=10)

    # =====================
    # B3: COMBINE RESULT
    # =====================
    for i, job in enumerate(valid_jobs):

        # 🔹 Frequency
        freq_keywords = extract_keywords(docs[i], top_n=10)

        # 🔹 TF-IDF ( FIX 2: tránh lỗi index)
        tfidf_keywords = tfidf_results[i] if i < len(tfidf_results) else []

        results.append({
            "job_id": f"job-{i+1}",
            "job_title": job.get("job_title", ""),

            #  SO SÁNH 2 CÁCH
            "keywords_frequency": freq_keywords,
            "keywords_tfidf": tfidf_keywords
        })

    return results


# =========================
# 3. SAVE OUTPUT
# =========================
def save_results(data, file_path="data/keywords_output.json"):
    """
    Ghi kết quả ra file JSON
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,  # giữ tiếng Việt
            indent=2             # format đẹp
        )


# =========================
# 4. MAIN
# =========================
def main():
    print(" START NLP...\n")

    # load dữ liệu
    jobs = load_jobs()
    print(f" Loaded {len(jobs)} jobs")

    # xử lý NLP
    results = process_jobs(jobs)
    print(f" Processed {len(results)} jobs")

    # lưu file
    save_results(results)

    print("\n DONE! Check: data/keywords_output.json")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    main()