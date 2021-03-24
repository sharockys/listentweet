import nltk


def test_yake_keyword_extraction():
    from listentweet.keyword_extraction.yake_extractor import (
        yake_keyword_extraction,
    )
    from listentweet.keyword_extraction.yake_extractor import yake_highlight

    nltk.download("gutenberg")
    emma = nltk.corpus.gutenberg.open("austen-emma.txt").read()
    keywords = yake_keyword_extraction(emma)
    assert len(keywords) == 20
    assert isinstance(keywords[0][0], str)
    assert isinstance(keywords[0][1], float)

    text = "I am a Doctor on the moon."
    keywords = yake_keyword_extraction(text)
    highlighted_text = yake_highlight(text, keywords)
    assert "<kw>" + keywords[0][0] + "</kw>" in highlighted_text
