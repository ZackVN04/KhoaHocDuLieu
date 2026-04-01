from underthesea import word_tokenize
import re
from stopwords import STOPWORDS


def to_lowercase(text: str) -> str:
    return text.lower()


def remove_special_characters(text: str) -> str:
    return re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", " ", text)


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def tokenize(text: str) -> list:
    text = word_tokenize(text, format="text")
    return text.split()


def remove_stopwords(tokens: list) -> list:
    filtered_tokens = []

    for token in tokens:
        clean_token = token.replace("_", " ")

        # 🔥 FIX: lọc stopwords đúng + bỏ từ ngắn
        if clean_token not in STOPWORDS and len(clean_token) > 2:
            filtered_tokens.append(token)

    return filtered_tokens


def preprocess_text(text: str) -> list:
    text = to_lowercase(text)
    text = remove_special_characters(text)
    text = normalize_whitespace(text)

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)

    return tokens