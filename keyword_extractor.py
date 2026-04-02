from collections import Counter
from stopwords import STOPWORDS


BAD_WORDS = {
    "theo", "và", "của", "trong", "cho", "với", "được",
    "ms", "cv", "nv", "vp",
    "yêu cầu", "công ty", "công việc", "làm việc", "thực hiện"
}


def generate_ngrams(tokens, n=2):
    return [" ".join(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]


def extract_keywords(text: str, top_n=10):

    tokens = text.split()

    unigram_counter = Counter(tokens)
    bigram_counter = Counter(generate_ngrams(tokens, 2))

    combined = {}

    # =====================
    # UNIGRAM
    # =====================
    for word, freq in unigram_counter.items():

        clean_word = word.replace("_", " ")

        if (
            len(clean_word) < 3
            or clean_word in BAD_WORDS
            or clean_word in STOPWORDS
        ):
            continue

        combined[word] = freq

    # =====================
    # BIGRAM
    # =====================
    for phrase, freq in bigram_counter.items():

        #  bỏ bigram rác
        if freq < 2:
            continue

        words = phrase.split()
        clean_words = [w.replace("_", " ") for w in words]

        #  chứa stopwords hoặc từ rác
        if any(
            w in BAD_WORDS or w in STOPWORDS or len(w) < 3
            for w in clean_words
        ):
            continue

        #  cụm không có nghĩa (toàn từ ngắn)
        if all(len(w) <= 3 for w in clean_words):
            continue

        combined[phrase] = freq * 1.5

    # =====================
    # SORT
    # =====================
    ranked = sorted(combined.items(), key=lambda x: x[1], reverse=True)

    # =====================
    # FILTER TRÙNG NGHĨA
    # =====================
    final_keywords = []
    used_words = set()

    for k, s in ranked:
        words = k.split()
        clean_words = [w.replace("_", " ") for w in words]

        # ưu tiên bigram
        if len(words) == 2:
            final_keywords.append((k, s))
            used_words.update(clean_words)

        # unigram nếu không bị trùng
        elif len(words) == 1:
            if clean_words[0] in used_words:
                continue
            final_keywords.append((k, s))

        if len(final_keywords) >= top_n:
            break

    # fallback
    if not final_keywords:
        return [
            {"keyword": k.replace("_", " "), "score": float(v)}
            for k, v in unigram_counter.most_common(top_n)
        ]

    return [
        {"keyword": k.replace("_", " "), "score": float(s)}
        for k, s in final_keywords
    ]