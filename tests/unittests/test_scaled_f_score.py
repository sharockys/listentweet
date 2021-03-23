import nltk


def test_ScaledFScore():
    # primitive test only.
    from listentweet.keyword_extraction.scaled_f_score import ScaledFScore

    nltk.download("gutenberg")
    emma = nltk.corpus.gutenberg.open("austen-emma.txt").readlines()
    sfs = ScaledFScore(emma)
    characteristic_words = sfs.get_f1_score(keyword="emma", max_terms=30)
    assert "emma" in characteristic_words
