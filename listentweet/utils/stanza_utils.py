import stanza
from stanza.pipeline.core import ResourcesFileNotFoundError


def init_stanza_model(lang: str = "en"):
    try:
        snlp = stanza.Pipeline(lang)
    except ResourcesFileNotFoundError:
        stanza.download(lang)
        snlp = stanza.Pipeline(lang)
    return snlp
