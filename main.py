from utils import load_jobs, save_keywords
from preprocess import preprocess_text
from keyword_extractor import extract_keywords

def main():
    print("🚀 BẮT ĐẦU PIPELINE TRÍCH XUẤT TỪ KHÓA...\n")

    # 1. Load dữ liệu từ jobs.json
    jobs = load_jobs("data/jobs.json")
    if not jobs:
        print("❌ Không có dữ liệu để xử lý.")
        return

    print(f"📦 Đã nạp {len(jobs)} công việc.\n")

    results = []

    # 2. Loop qua từng job để xử lý
    for i, job in enumerate(jobs, 1):
        # Ưu tiên lấy 'description' (nội dung chi tiết)
        raw_text = job.get("description", "")
        
        if not raw_text:
            continue

        # 3. Gọi Pipeline: Preprocess -> Tokenize -> Extract
        # Lưu ý: preprocess_text trả về list tokens
        tokens = preprocess_text(raw_text)
        clean_text = " ".join(tokens)
        
        # 4. Trích xuất và xếp hạng keyword
        keywords = extract_keywords(clean_text, top_n=10)

        # Lưu kết quả
        results.append({
            "job_id": f"job-{i:03d}",
            "job_title": job.get("job_title"),
            "company": job.get("company"),
            "keywords": keywords
        })

        if i % 10 == 0:
            print(f"✅ Đã xử lý {i}/{len(jobs)} jobs...")

    # 5. Lưu kết quả ra file JSON
    save_keywords(results, "data/keywords_output.json")
    
    print("\n✨ HOÀN THÀNH GIAI ĐOẠN 7 & 8!")
    print(f"📝 Kết quả cuối cùng tại: data/keywords_output.json")

if __name__ == "__main__":
    main()
