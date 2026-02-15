from typing import List, Tuple, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def top_k_chunks(query: str, chunks: List[Dict[str, Any]], k: int = 3) -> List[Tuple[Dict[str, Any], float]]:
    if not query or not chunks:
        return []

    texts = [c.get("text", "") for c in chunks]
    if all(not t.strip() for t in texts):
        return []

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(texts)
    q = vectorizer.transform([query])

    sims = cosine_similarity(q, X).flatten()
    ranked = sims.argsort()[::-1]

    results: List[Tuple[Dict[str, Any], float]] = []
    for i in ranked[:k]:
        score = float(sims[i])
        if score <= 0:
            continue
        results.append((chunks[i], score))

    return results
