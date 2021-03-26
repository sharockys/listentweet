from transformers import AutoTokenizer, AutoModel
from typing import List, Union

Strs = Union[List[str], str]


class TransformersVectorizer:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def __call__(self, sentences: Strs):
        return self.vectorize_sentences(sentences)

    def tokenize(self, sentences: Strs, return_tensor: bool = True):
        if return_tensor:
            return self.tokenizer(
                sentences,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            )
        else:
            return self.tokenizer.tokenize(sentences)

    def vectorize_sentences(self, sentences: Strs):
        inputs = self.tokenize(sentences)
        outputs = self.model(**inputs)
        return outputs[1].detach()

    def vectorize_sentences_by_average_pool(self, sentences: Strs):
        inputs = self.tokenize(sentences)
        outputs = self.model(**inputs)
        return outputs[0].mean(axis=1).detach()

    def vectorize_sentences_by_token(self, sentences: Strs):
        inputs = self.tokenize(sentences)
        outputs = self.model(**inputs)
        return outputs[0].detach()
