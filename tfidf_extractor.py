from sklearn.feature_extraction.text import TfidfVectorizer


def extract_tfidf_keywords(docs, top_n=10):
    """
    docs: list các document (string)
    """

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(docs)

    feature_names = vectorizer.get_feature_names_out()

    results = []

    for doc_index in range(len(docs)):
        row = X[doc_index].toarray()[0]

        # lấy top keyword
        top_indices = row.argsort()[::-1][:top_n]

        keywords = []
        for idx in top_indices:
            keywords.append({
                "keyword": feature_names[idx],
                "score": float(row[idx])
            })

        results.append(keywords)

    return results