import yake
from yake.highlight import TextHighlighter
from typing import Dict, List, Tuple, Union

Strs = Union[List[str], str]

parameters = {
    "lan": "en",
    "n": 3,
    "dedupLim": 0.9,
    "dedupFunc": "seqm",
    "windowsSize": 1,
    "top": 20,
    "features": None,
}


def yake_keyword_extraction(
    text: str, parameters: Dict = parameters
) -> List[Tuple[str, float]]:
    custom_kw_extractor = yake.KeywordExtractor(**parameters)
    keywords = custom_kw_extractor.extract_keywords(text)

    return keywords


def yake_highlight(
    text: str,
    keywords: List[Tuple[str, float]],
    prefix: str = "<kw>",
    suffix: str = "</kw>",
) -> str:
    th = TextHighlighter(
        max_ngram_size=3, highlight_pre=prefix, highlight_post=suffix
    )
    highlighted_text = th.highlight(text, keywords)
    return highlighted_text
