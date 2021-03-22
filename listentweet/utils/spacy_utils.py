import spacy
import logging
from spacy import Language

from wasabi import msg
from spacy.cli.download import get_compatibility

available_models = get_compatibility()

logger = logging.getLogger(__file__)


def init_spacy_model(
    lang: str = "en", size: str = "md", model_type: str = "core"
) -> Language:
    name = ""
    for model_name in available_models:
        if (
            lang in model_name
            and size in model_name
            and model_type in model_name
        ):
            msg.good(f"Found model {model_name}")
            name = model_name
            break
        else:
            msg.fail("No compatible model of your choice.")
    model = load_spacy_model(name)
    return model


def load_spacy_model(model_name: str = "en_core_web_md") -> Language:
    try:
        nlp = spacy.load(model_name)
    except OSError:
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
    return nlp
