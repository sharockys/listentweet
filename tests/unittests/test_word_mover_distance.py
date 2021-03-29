def test_word_mover_disntace():
    from listentweet.pipelines.transformer_vectorizer import (
        TransformersVectorizer,
    )
    from listentweet.similarities.word_mover_distance import (
        WordMoverDistanceTransformers,
    )

    vectorizer = TransformersVectorizer("camembert-base")
    wmd = WordMoverDistanceTransformers(vectorizer)

    sent5 = "Je vous aime"
    sent6 = "Je vous déteste"
    sent7 = "Je vous adore"
    love_sim = wmd(sent5, sent7)
    hate_mild = wmd(sent6, sent7)
    hate_strong = wmd(sent5, sent6)

    assert love_sim < hate_mild
    assert love_sim < hate_strong
    assert hate_mild < hate_strong
