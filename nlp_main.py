# nlp_main.py

import json
from preprocess import preprocess_text
from keyword_extractor import extract_keywords


# =========================
# LOAD DATA
# =========================
def load_jobs(file_path="data/jobs.json"):
    # đọc file JSON chứa job từ crawler
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# PROCESS NLP
# =========================
def process_jobs(jobs):
    results = []

    for i, job in enumerate(jobs, 1):
        # lấy description từ dữ liệu web
        text = job.get("description", "")

        if not text:
            continue

        # preprocess
        tokens = preprocess_text(text)

        # chuyển list → string để extract
        clean_text = " ".join(tokens)

        # extract keyword
        keywords = extract_keywords(clean_text, top_n=10)

        results.append({
            "job_id": f"job-{i}",
            "job_title": job.get("job_title"),
            "keywords": keywords
        })

    return results


# =========================
# SAVE OUTPUT
# =========================
def save_results(data, file_path="data/keywords_output.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =========================
# MAIN
# =========================
def main():
    print("🚀 START NLP...\n")

    jobs = load_jobs()

    results = process_jobs(jobs)

    save_results(results)

    print("✅ DONE! Check data/keywords_output.json")


if __name__ == "__main__":
    main()