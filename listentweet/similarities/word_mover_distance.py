import numpy as np
from scipy.optimize import linprog


class WordMoverDistanceTransformers:
    def __init__(self, transformer_vectorizer):
        self.vectorizer = transformer_vectorizer

    def __call__(self, text1: str, text2: str):
        vector1 = (
            self.vectorizer.vectorize_sentences_by_token(text1)[:, 1:-1, :]
            .flatten(start_dim=0, end_dim=1)
            .numpy()
        )

        vector2 = (
            self.vectorizer.vectorize_sentences_by_token(text2)[:, 1:-1, :]
            .flatten(start_dim=0, end_dim=1)
            .numpy()
        )

        p = np.ones(vector1.shape[0]) / vector2.shape[0]
        q = np.ones(vector2.shape[0]) / vector2.shape[0]
        D = np.sqrt(np.square(vector1[:, None] - vector2[None, :]).mean(axis=2))
        dist = self.wasserstein_distance(p, q, D)

        return dist

    @staticmethod
    def wasserstein_distance(p, q, D):
        """Wasserstein distance with linear programming in scipy
        p.shape=[m], q.shape=[n], D.shape=[m, n]
        p.sum()=1, q.sum()=1, p∈[0,1], q∈[0,1]
        """
        A_eq = []
        for i in range(len(p)):
            A = np.zeros_like(D)
            A[i, :] = 1
            A_eq.append(A.reshape(-1))
        for i in range(len(q)):
            A = np.zeros_like(D)
            A[:, i] = 1
            A_eq.append(A.reshape(-1))
        A_eq = np.array(A_eq)
        b_eq = np.concatenate([p, q])
        D = D.reshape(-1)
        result = linprog(D, A_eq=A_eq[:-1], b_eq=b_eq[:-1])
        return result.fun
