# 🚀 Dự án Trích xuất Từ khóa Tuyển dụng (Vietnamese Job Keyword Extraction)

Dự án này là một hệ thống tự động hóa hoàn chỉnh (Pipeline) từ việc thu thập dữ liệu tuyển dụng từ website đến việc sử dụng xử lý ngôn ngữ tự nhiên (NLP) để trích xuất các kỹ năng, yêu cầu công việc quan trọng dưới dạng từ khóa.

---

## 🏗️ Kiến trúc Hệ thống

Dự án được chia làm 2 giai đoạn chính:

### 1. Thu thập dữ liệu (Crawler & Scraper)
- **Crawler:** Truy cập danh sách việc làm, tự động phân trang và lấy link chi tiết.
- **Scraper:** Truy cập từng link để lấy tiêu đề, công ty, lương và mô tả công việc (Job Description).
- **Công nghệ:** `requests`, `parsel` (XPath), `ThreadPoolExecutor` (chạy đa luồng để tăng tốc).

### 2. Xử lý ngôn ngữ tự nhiên (NLP Pipeline)
- **Preprocess:** Làm sạch văn bản, xóa ký tự đặc biệt, chuyển về chữ thường.
- **Tokenize:** Sử dụng thư viện `underthesea` để tách từ tiếng Việt chuẩn (ví dụ: "kinh doanh" thay vì "kinh", "doanh").
- **Filtering:** Loại bỏ từ dừng (Stopwords) và các từ rác phổ biến trong tuyển dụng.
- **Keyword Extraction:** 
    - Kết hợp **Unigram** (từ đơn) và **Bigram** (từ ghép).
    - **Scoring:** Chấm điểm dựa trên tần suất xuất hiện (Frequency). Bigram được nhân hệ số ưu tiên (x1.5) để lấy được các cụm từ có nghĩa hơn.
    - **Ranking:** Sắp xếp và lấy Top N từ khóa đặc trưng nhất cho mỗi công việc.

---

## 📁 Cấu trúc Thư mục

```text
KhoaHocDuLieu/
├── crawler_runner.py     # File chạy chính của phần cào dữ liệu
├── main.py               # File chạy chính của phần NLP (Trích xuất từ khóa)
├── crawler.py            # Logic lấy link từ danh sách
├── scraper.py            # Logic lấy nội dung chi tiết từng job
├── preprocess.py         # Các hàm làm sạch văn bản & tokenize
├── keyword_extractor.py  # Thuật toán tính điểm & trích xuất keyword
├── stopwords.py          # Danh sách từ dừng tiếng Việt
├── utils.py              # Hàm bổ trợ đọc/ghi file JSON
├── data/                 # Thư mục chứa dữ liệu
│   ├── jobs.json             # Dữ liệu thô sau khi cào
│   └── keywords_output.json  # Kết quả từ khóa sau khi xử lý
└── requirements.txt      # Danh sách thư viện cần thiết
```

---

## 🛠️ Hướng dẫn Cài đặt

1. **Yêu cầu:** Máy đã cài Python 3.8 trở lên.

2. **Cài đặt thư viện:**
```bash
pip install requests parsel underthesea
```

---

## 🚀 Cách Vận hành

Dự án chạy theo 2 bước:

### Bước 1: Thu thập dữ liệu mới
Lệnh này sẽ cào dữ liệu từ web và lưu vào `data/jobs.json`.
```bash
python crawler_runner.py
```

### Bước 2: Trích xuất từ khóa
Lệnh này sẽ đọc dữ liệu từ `data/jobs.json`, xử lý NLP và lưu kết quả vào `data/keywords_output.json`.
```bash
python main.py
```

---

## 📊 Kết quả đạt được
Mỗi công việc trong file kết quả sẽ bao gồm các từ khóa chất lượng cao như:
- Kỹ năng: `giao tiếp`, `bán hàng`, `quản lý`, `vận hành`.
- Công cụ/Kiến thức: `phần mềm`, `bản vẽ kỹ thuật`, `tiếng anh`.
- Thái độ: `trung thực`, `năng động`, `chịu khó`.

---
*Dự án được xây dựng phục vụ mục đích học tập và nghiên cứu dữ liệu tuyển dụng.*
