# utils.py

import json  # thư viện có sẵn của Python để làm việc với JSON


# =========================
# 1. READ JSON FILE
# =========================
def read_json(file_path: str):
    """
    INPUT:
        đường dẫn file JSON

    OUTPUT:
        dữ liệu dạng Python (list/dict)
    """

    # mở file ở chế độ đọc (r = read)
    with open(file_path, "r", encoding="utf-8") as f:

        # json.load → chuyển JSON → Python object
        data = json.load(f)

    # trả về dữ liệu
    return data


# =========================
# 2. WRITE JSON FILE
# =========================
def write_json(file_path: str, data):
    """
    INPUT:
        file_path: nơi lưu file
        data: dữ liệu Python (list/dict)

    OUTPUT:
        file JSON được ghi ra
    """

    # mở file ở chế độ ghi (w = write)
    with open(file_path, "w", encoding="utf-8") as f:

        # json.dump → chuyển Python → JSON
        json.dump(
            data,              # dữ liệu cần ghi
            f,                 # file
            ensure_ascii=False, # giữ tiếng Việt
            indent=2           # format đẹp
        )