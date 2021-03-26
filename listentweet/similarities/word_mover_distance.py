import torch
import numpy as np
from pyemd import emd
from numpy import zeros, sum as np_sum, double
from gensim.corpora import Dictionary


class WordMoverDistanceTransformers:
    def __init__(self, transformer_vectorizer):
        self.vectorizer = transformer_vectorizer

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
    from listentweet.pipelines.transformer_vectorizer import (
        TransformersVectorizer,
    )

    vectorizer = TransformersVectorizer("camembert-base")
    wmd = WordMoverDistanceTransformers(vectorizer)
    dst = wmd.wmdistance(sent1, sent2)
    print(dst)
