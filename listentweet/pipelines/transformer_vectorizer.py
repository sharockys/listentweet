from transformers import AutoTokenizer, AutoModel
from typing import List, Union

Strs = Union[List[str], str]


class TransformersVectorizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def __call__(self, sentences: str):
        return self.vectorize_sentence(sentences)

    def vectorize_sentences(self, sentences: Strs):
        inputs = self.tokenizer(sentences, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs[1]

    def vectorize_sentences_by_average_pool(self, sentences: Strs):
        inputs = self.tokenizer(sentences, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs[0].mean(axis=1)
