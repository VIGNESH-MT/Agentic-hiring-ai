from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class SkillIndexer:
    """
    Lightweight semantic skill matcher using TF-IDF + cosine similarity.
    """

    def __init__(self, skills):
        self.skills = list(skills)

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words=None
        )

        self.skill_vectors = self.vectorizer.fit_transform(self.skills)

    def search(self, text, top_k=5):
        text_vec = self.vectorizer.transform([text])
        sims = cosine_similarity(text_vec, self.skill_vectors)[0]

        top_idx = sims.argsort()[-top_k:][::-1]

        return [
            {
                "skill": self.skills[i],
                "similarity": float(sims[i])
            }
            for i in top_idx
            if sims[i] > 0.2
        ]
