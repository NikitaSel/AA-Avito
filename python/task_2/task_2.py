from typing import Iterable
from helper import count_vocab_clear, count_vocab_fast

class CountVectorizer:
    def __init__(self):
        self._vocabulary = [] 
        self.lower = True

    def _count_vocab(self, corpus: Iterable) -> tuple[dict, list[list[int]]]:
        """
        Gets vocabulary and matrix
        """
        return count_vocab_fast(corpus, self._processing)


    def fit_transform(self, corpus: Iterable) -> list[list[int]]:
        """
        Gets vocabulary and matrix
        """

        vocabulary, X =  self._count_vocab(corpus)
        self._vocabulary = vocabulary
        return X

    def get_feature_names(self):
        """
        Gets vocabulary
        """

        return self._vocabulary

    def _processing(self, text: str) -> list[str]:
        """
        Splits and lowerises the text
        """

        if self.lower:
            text = text.lower()

        words = text.split()
        return words
