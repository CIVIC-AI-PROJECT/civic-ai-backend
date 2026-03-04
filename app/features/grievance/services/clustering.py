from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def cluster_complaints(texts, n_clusters=5):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )

    X = vectorizer.fit_transform(texts)

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42
    )

    labels = model.fit_predict(X)

    terms = vectorizer.get_feature_names_out()
    cluster_keywords = {}

    for i in range(n_clusters):
        center = model.cluster_centers_[i]
        top_indices = center.argsort()[-10:][::-1]
        cluster_keywords[i] = [terms[ind] for ind in top_indices]

    return labels, cluster_keywords
