from typing import List
from collections import Counter, defaultdict
from scipy.stats import hmean, norm
from numpy import std, mean


class ScaledFScore:
    def __init__(self, texts: List[str]):
        self.processed_corpus = [text.lower().split() for text in texts]
        self.wordcount = defaultdict(int)
        self.wordcount.update(
            Counter([word for text in self.processed_corpus for word in text])
        )

    def filter_subcorpus(self, keyword: str):
        keyword = keyword.lower()
        return [text for text in self.processed_corpus if keyword in text]

    @staticmethod
    def normcdf(x):
        mean_ = mean(x)
        std_ = std(x)
        return norm.cdf(x, mean_, std_)

    def get_precision(self, sub_wordcount):
        precision = {
            word: sub_wordcount[word] / count
            for word, count in self.wordcount.items()
        }
        normalized = self.normcdf(list(precision.values()))
        return {k: v for k, v in zip(precision.keys(), normalized)}

    def get_frequency(self, sub_wordcount):
        total_sub_corpus_word = sum(sub_wordcount.values())

        freq = {
            word: count / total_sub_corpus_word
            for word, count in sub_wordcount.items()
        }
        normalized = self.normcdf(list(freq.values()))
        return {k: v for k, v in zip(freq.keys(), normalized)}

    def get_f1_score(self, keyword, max_terms=-1):
        subcorpus = self.filter_subcorpus(keyword)

        sub_wordcount = defaultdict(int)
        sub_wordcount.update(
            Counter([word for text in subcorpus for word in text])
        )

        precision = self.get_precision(sub_wordcount)
        frequency = self.get_frequency(sub_wordcount)
        sfs = {
            word: hmean([precision[word], frequency[word]])
            for word in sub_wordcount.keys()
        }

        return {
            k: v
            for k, v in sorted(
                sfs.items(), key=lambda item: item[1], reverse=True
            )[:max_terms]
            if v > 0
        }
