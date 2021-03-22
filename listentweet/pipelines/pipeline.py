from listentweet.utils.spacy_utils import init_spacy_model
from listentweet.utils.stanza_utils import init_stanza_model


class LTPpipeline:
    def __init__(
        self,
        lang: str = "en",
        backend: str = "spacy",
        model_size: str = "md",
        model_type: str = "core",
    ) -> None:
        self.lang = lang
        self.model_type = model_type
        self.nlp = self._load_backend(lang, backend, model_size, model_type)

    def _load_backend(self, lang, backend, model_size, model_type):
        if backend == "spacy":
            return init_spacy_model(lang, model_size, model_type)
        elif backend == "stanza":
            return init_stanza_model(lang)
        else:
            raise ValueError('Only "stanza" or "spacy" backend supported.')

    def get_pipelines(self) -> list[str]:
        if self.model_type == "spacy":
            return self.nlp.pipe_names
        if self.model_type == "stanza":
            return self.nlp.processors

    def _add_stanza_to_pipeline(self):
        pass

    def _add_transformers_to_pipeline(self):
        pass
