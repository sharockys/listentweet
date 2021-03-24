import transformers


def test_transformer_vectorizer():
    from listentweet.pipelines.transformer_vectorizer import (
        TransformersVectorizer,
    )

    # test loading
    vectorizer = TransformersVectorizer("camembert-base")
    assert isinstance(
        vectorizer.tokenizer,
        transformers.models.camembert.tokenization_camembert_fast.CamembertTokenizerFast,
    )

    assert isinstance(
        vectorizer.model,
        transformers.models.camembert.modeling_camembert.CamembertModel,
    )

    # test samples
    sentences = ["Je ne veux pas travailler", "mais je n'ai pas d'argent"]

    # test tokenizer

    tokens = vectorizer._tokenize(sentences[0])
    assert len(tokens) == 2

    # test basic vectorization on one sentence
    single_vector = vectorizer(sentences[0])
    assert single_vector.shape == (1, 768)

    # test basic vectorization on batch
    batch_vector = vectorizer(sentences)
    assert batch_vector.shape == (2, 768)

    # test averaged vector on one sentence
    mean_single_vector = vectorizer.vectorize_sentences_by_average_pool(
        sentences[0]
    )
    assert mean_single_vector.shape == (1, 768)

    # test averaged vector on batch
    batch_mean_vector = vectorizer.vectorize_sentences_by_average_pool(
        sentences
    )
    assert batch_mean_vector.shape == (2, 768)
