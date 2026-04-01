# stopwords.py

STOPWORDS = {

    # =====================
    # 1. TỪ NỐI / HƯ
    # =====================
    "và", "là", "của", "một", "các", "những",
    "được", "cho", "với", "trong", "có", "cần",

    # =====================
    # 2. TRỢ TỪ
    # =====================
    "đã", "đang", "sẽ", "này", "kia", "đó",
    "tại", "vì", "nên", "rằng", "thì",

    # =====================
    # 3. TỪ RÁC TRONG JOB
    # =====================
    "công", "ty", "ứng", "viên", "nhân", "việc",

    # =====================
    # 4. TỪ CHUNG CHUNG
    # =====================
    "yêu", "cầu", "khả", "năng", "tốt",
    "làm", "có",

    # =====================
    # 5. NHIỄU THỰC TẾ (DATASET)
    # =====================
    "theo", "quy", "thuật", "đảm", "bảo",
    "lên", "xuống", "cấp", "tiền", "nghiệp",

    # =====================
    # 6. TOKEN LỖI
    # =====================
    "người", "bộ", "phận",

    # =====================
    # 🔥 7. FIX QUAN TRỌNG (UNIGRAM)
    # =====================
    "liên", "quan", "phối", "hợp",
    "lập", "việc", "ưu", "tiên",
    "không", "thứ",

    # =====================
    # 🔥 8. FIX QUAN TRỌNG (BIGRAM)
    # =====================
    "yêu cầu",
    "công ty",
    "công việc",
    "làm việc",
    "thực hiện",
    "liên quan",
    "phối hợp",
    "ưu tiên ứng viên"
}