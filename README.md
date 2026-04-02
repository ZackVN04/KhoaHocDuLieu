# 🚀 PROJECT NLP: PHÂN TÍCH TIN TUYỂN DỤNG & TRÍCH XUẤT KEYWORD 

---

# 🎯 1. DỰ ÁN NÀY LÀ GÌ?

Đây là một hệ thống hoàn chỉnh gồm **3 giai đoạn chính liên kết với nhau**:

```text
1. Crawl dữ liệu việc làm từ website thật
2. Xử lý văn bản tiếng Việt (NLP pipeline)
3. Trích xuất keyword + phân tích + trực quan hóa
```

👉 Mục tiêu:

* Hiểu **job đang cần gì (kỹ năng, yêu cầu, công việc)**
* So sánh 2 phương pháp:

  * **Frequency (đếm tần suất)**
  * **TF-IDF (độ quan trọng theo toàn bộ dataset)**



---

# 🧠 2. LUỒNG HOẠT ĐỘNG 

```text
Website
   ↓
Crawler (main.py)
   ↓
jobs.json (data thô)
   ↓
NLP (nlp_main.py)
   ↓
keywords_output.json
   ↓
Visualization (biểu đồ)
```

👉 Chi tiết hơn:

```text
description
→ preprocess (làm sạch)
→ tokenize (underthesea)
→ remove stopwords
→ keyword (frequency)
→ keyword (TF-IDF)
→ so sánh
→ lưu JSON
→ vẽ biểu đồ
```

---

# 📂 3. CẤU TRÚC THƯ MỤC 

```text
project/
│
├── crawler.py              # crawl link job
├── scraper.py              # scrape chi tiết job
├── main.py                 # chạy crawler (đa luồng)
│
├── preprocess.py           # xử lý text tiếng Việt
├── stopwords.py            # danh sách từ rác
├── keyword_extractor.py    # keyword theo frequency
├── tfidf_extractor.py      # keyword theo TF-IDF
├── nlp_main.py             # pipeline NLP chính
│
├── visualize.py            # vẽ biểu đồ keyword
├── test_visualize.py       # file test riêng cho biểu đồ
│
├── utils.py                # đọc/ghi JSON (hỗ trợ)
│
├── data/
│   ├── jobs.json           # dữ liệu raw từ crawler
│   └── keywords_output.json # kết quả NLP cuối
│
├── requirements.txt        # danh sách thư viện
└── README.md
```

---

# 🔍 4. GIẢI THÍCH TỪNG FILE (THEO LUỒNG THỰC TẾ)

---

## 🔹 crawler.py — LẤY LINK JOB

👉 nhiệm vụ:

* gửi request tới website
* parse HTML
* lấy tất cả link job

```text
OUTPUT → list URL
```

---

## 🔹 scraper.py — LẤY NỘI DUNG JOB

👉 với mỗi URL:

```text
Lấy:
- job_title
- company
- salary
- description (QUAN TRỌNG NHẤT)
```

👉 description = input chính của NLP

---

## 🔹 main.py — ĐIỀU PHỐI CRAWL

👉 làm 3 việc:

```text
1. crawl links
2. scrape song song (multi-thread)
3. lưu data/jobs.json
```

👉 dùng ThreadPoolExecutor → tăng tốc crawl

---

## 🔹 data/jobs.json — DỮ LIỆU THÔ

```json
{
  "job_title": "...",
  "description": "..."
}
```

👉 chưa xử lý → còn rất nhiều nhiễu

---

## 🔹 preprocess.py — LÀM SẠCH TEXT (CỰC QUAN TRỌNG)

Pipeline:

```text
1. lowercase
2. remove special characters
3. normalize whitespace
4. tokenize (underthesea)
5. remove stopwords
```

👉 ví dụ:

```text
"máy móc ngành mộc"
→ "máy_móc ngành_mộc"
```

👉 giúp giữ đúng nghĩa tiếng Việt

---

## 🔹 stopwords.py — LỌC TỪ RÁC

👉 loại bỏ:

```text
và, của, theo, làm việc, công ty, liên quan...
```

👉 giúp:

* giảm nhiễu
* tăng chất lượng keyword

---

## 🔹 keyword_extractor.py — FREQUENCY

👉 logic:

```text
đếm số lần xuất hiện (Counter)
+ bigram (2 từ)
+ scoring:
   unigram → freq
   bigram → freq * 1.5
```

👉 thêm:

* lọc từ ngắn
* loại từ rác
* tránh trùng nghĩa

---

## 🔹 tfidf_extractor.py — NÂNG CAO

👉 dùng:

```text
TfidfVectorizer (sklearn)
```

👉 tác dụng:

```text
✔ giữ từ đặc trưng
✔ loại từ phổ biến
```

👉 ví dụ:

```text
"công việc" → bỏ
"kế toán" → giữ
```

---

## 🔹 nlp_main.py — TRÁI TIM HỆ THỐNG

👉 thực hiện toàn bộ:

```text
load jobs
→ preprocess toàn bộ
→ tạo docs list
→ chạy TF-IDF (toàn dataset)
→ extract frequency từng job
→ gộp kết quả
→ lưu JSON
```

👉 output:

```json
{
  "keywords_frequency": [...],
  "keywords_tfidf": [...]
}
```

---

## 🔹 visualize.py — PHÂN TÍCH DỮ LIỆU

👉 làm:

```text
gom keyword toàn bộ job
→ đếm frequency
→ vẽ biểu đồ (bar chart)
```

👉 giúp:

* thấy kỹ năng hot
* phân tích xu hướng

---

## 🔹 test_visualize.py — CHẠY BIỂU ĐỒ

```python
from visualize import plot_top_keywords
plot_top_keywords()
```

👉 tách riêng để:

* code sạch
* dễ test

---

## 🔹 utils.py — PHỤ TRỢ

👉 đọc / ghi JSON
👉 không ảnh hưởng logic chính

---

# ⚙️ 5. LUỒNG CHẠY THỰC TẾ (THEO FILE)

---

## 🔥 BƯỚC 1 — CRAWL

```bash
python main.py
```

👉 tạo:

```text
data/jobs.json
```

---

## 🔥 BƯỚC 2 — NLP

```bash
python nlp_main.py
```

👉 tạo:

```text
data/keywords_output.json
```

---

## 🔥 BƯỚC 3 — VISUALIZE

```bash
python test_visualize.py
```

👉 hiển thị biểu đồ

---

# 📊 6. SO SÁNH 2 PHƯƠNG PHÁP

| Method    | Ý nghĩa                          |
| --------- | -------------------------------- |
| Frequency | từ xuất hiện nhiều               |
| TF-IDF    | từ quan trọng trong toàn dataset |

👉 ví dụ thực tế:

```text
Frequency → "làm việc"
TF-IDF → "kế toán", "bảo trì", "cơ khí"
```

---

# 📦 7. THƯ VIỆN CẦN CÀI

```bash
pip install requests
pip install parsel
pip install underthesea
pip install scikit-learn
pip install matplotlib
```

---

# 🧪 8. KẾT QUẢ ĐẠT ĐƯỢC

✔ Crawl dữ liệu thật từ website
✔ Xử lý tiếng Việt đúng (underthesea)
✔ Keyword hợp lý (clean + meaningful)
✔ So sánh 2 phương pháp
✔ Có biểu đồ trực quan

---

# 🚀 9. KẾT LUẬN

```text
Hệ thống hoàn chỉnh gồm:
Crawler → NLP → Phân tích → Visualization
```



* có dữ liệu thật
* có phân tích
* có insight

---

# 🔥 10. ĐÁNH GIÁ

```text
✔ Full pipeline NLP
✔ Có TF-IDF (nâng cao)
✔ Có visualization





---

# 🤝 13. ĐÓNG GÓP

* Fork repo
* Tạo branch
* Pull request

---

# 🎯 14. TỔNG KẾT 

```text
Đây là hệ thống NLP mini nhưng đầy đủ: crawl → xử lý → phân tích → trực quan
```


