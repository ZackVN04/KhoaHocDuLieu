import json


def load_jobs(file_path="data/jobs.json"):
    """
    Đọc danh sách jobs từ file JSON
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Lỗi: Không tìm thấy file {file_path}")
        return []
    except Exception as e:
        print(f"❌ Lỗi đọc file: {e}")
        return []


def save_keywords(results, file_path="data/keywords_output.json"):
    """
    Lưu kết quả keyword extraction vào file JSON
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"✅ Đã lưu kết quả vào {file_path}")
    except Exception as e:
        print(f"❌ Lỗi lưu file: {e}")
