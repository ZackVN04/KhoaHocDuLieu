import json
import matplotlib.pyplot as plt
from collections import Counter


def plot_top_keywords(file_path="data/keywords_output.json"):

    # ===== LOAD FILE =====
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ===== GOM KEYWORD =====
    all_keywords = []

    for job in data:
        for kw in job.get("keywords_frequency", []):
            all_keywords.append(kw["keyword"])

    # ===== ĐẾM =====
    counter = Counter(all_keywords)

    top = counter.most_common(10)

    words = [w for w, _ in top]
    scores = [s for _, s in top]

    # ===== VẼ =====
    plt.figure()
    plt.bar(words, scores)

    plt.xticks(rotation=45)
    plt.title("Top Keywords (Frequency)")
    plt.xlabel("Keywords")
    plt.ylabel("Count")

    plt.tight_layout()
    plt.show()