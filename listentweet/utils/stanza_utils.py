import stanza
from stanza.pipeline.core import ResourcesFileNotFoundError
import spacy_stanza


def init_stanza_model(lang: str = "en"):
    try:
        snlp = stanza.Pipeline(lang)
    except ResourcesFileNotFoundError:
        stanza.download(lang)
        snlp = spacy_stanza.Pipeline(lang)
    return snlp
