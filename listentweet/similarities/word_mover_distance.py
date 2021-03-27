import torch
import numpy as np
from pyemd import emd
from numpy import zeros, sum as np_sum, double
from gensim.corpora import Dictionary


def word_mover_distance(x, y):
    """WMD（Word Mover's Distance with pymed
    x.shape=[m,d], y.shape=[n,d]
    """
    total_len = x.shape[0] + y.shape[0]
    p = np.ones(x.shape[0], dtype=double) / x.shape[0]
    q = np.ones(y.shape[0], dtype=double) / y.shape[0]
    p_padded = np.concatenate([p, np.zeros(y.shape[0])])
    q_padded = np.concatenate([q, np.zeros(x.shape[0])])
    D = np.sqrt(np.square(x[:, None] - y[None, :]).mean(axis=2))
    D = np.array(D, dtype=double)
    D_padded = np.zeros((total_len, total_len), dtype=double)
    D_padded[0 : D.shape[0], 0 : D.shape[1]] += D

    # print(p_padded.shape, q_padded.shape, D_padded.shape, total_len)

    return emd(p_padded, q_padded, D_padded)


class WordMoverDistanceTransformers:
    def __init__(self, transformer_vectorizer):
        self.vectorizer = transformer_vectorizer

    def np_wmd(self, text1: str, text2: str):
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

        dist = word_mover_distance(vector1, vector2)
        return dist

    def wmdistance(self, text1: str, text2: str):
        tokens1 = self.vectorizer.tokenize(text1, return_tensor=False)
        tokens2 = self.vectorizer.tokenize(text2, return_tensor=False)

        dictionary = Dictionary(documents=[tokens1, tokens2])
        vocab_len = len(dictionary)

        vector1 = self.vectorizer.vectorize_sentences_by_token(text1)[
            :, 1:-1, :
        ].flatten(start_dim=0, end_dim=1)
        vector2 = self.vectorizer.vectorize_sentences_by_token(text2)[
            :, 1:-1, :
        ].flatten(start_dim=0, end_dim=1)

        vectors = torch.vstack([vector1, vector2]).numpy()
        all_tokens = tokens1 + tokens2
        # bugs here, bert can give the same token different vectors.
        # Avoid vstack. use two dictionaries.
        keyed_vectors = dict(zip(all_tokens, vectors))

        if vocab_len == 1:
            # Both documents are composed of a single unique token => zero distance.
            return 0.0
        # Sets for faster look-up.
        docset1 = set(tokens1)
        docset2 = set(tokens2)

        # Compute distance matrix.
        distance_matrix = zeros((vocab_len, vocab_len), dtype=double)
        for i, t1 in dictionary.items():
            if t1 not in docset1:
                continue

            for j, t2 in dictionary.items():
                if t2 not in docset2 or distance_matrix[i, j] != 0.0:
                    continue
                # Compute Euclidean distance between (potentially unit-normed) word vectors.
                distance_matrix[i, j] = distance_matrix[j, i] = np.sqrt(
                    np_sum(keyed_vectors[t1] - keyed_vectors[t2]) ** 2
                )

        def nbow(document):
            d = zeros(vocab_len, dtype=double)
            nbow = dictionary.doc2bow(document)  # Word frequencies.
            doc_len = len(document)
            for idx, freq in nbow:
                d[idx] = freq / float(doc_len)  # Normalized word frequencies.
            return d

        # Compute nBOW representation of documents. This is what pyemd expects on input.
        d1 = nbow(tokens1)
        d2 = nbow(tokens2)
        # Compute WMD.
        return emd(d1, d2, distance_matrix)


if __name__ == "__main__":
    sent1 = "je ne veux pas travailler"
    sent2 = "mais je travaille"
    sent3 = "Je suis un chat"
    sent4 = "Il est une légume"
    from listentweet.pipelines.transformer_vectorizer import (
        TransformersVectorizer,
    )

    vectorizer = TransformersVectorizer("camembert-base")
    wmd = WordMoverDistanceTransformers(vectorizer)
    import time

    start1 = time.time()
    dst1 = wmd.wmdistance(sent1, sent2)
    start2 = time.time()
    dst2 = wmd.np_wmd(sent1, sent2)
    end = time.time()
    print(f"First execution {start2 - start1}, Second execution {end - start2}")
    print(f"distance 1 {dst1} , disntace 2 {dst2} .")
    dst3 = wmd.wmdistance(sent1, sent4)
    dst4 = wmd.np_wmd(sent1, sent4)

    # print(dst2, dst3)

    print(f"disntace 3 {dst3} distance 4 {dst4}")
    print(dst1 / dst3, dst2 / dst4)
