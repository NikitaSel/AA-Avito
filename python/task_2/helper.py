from typing import Iterable, Callable
from collections import Counter


def count_vocab_clear(corpus: Iterable, processing: Callable) -> tuple[dict, list[list[int]]]:
        """
        Gets vocabulary and matrix
        """

        feature_counters = [Counter(processing(text)) for text in corpus]

        unique_features = set()
        for unique_words in feature_counters:
            unique_features.update(unique_words)

        vocabulary = sorted(list(unique_features))

        X = [[counter[word] for word in vocabulary] for counter in feature_counters]
        return vocabulary, X

def count_vocab_fast(corpus: Iterable, processing: Callable) -> tuple[dict, list[list[int]]]:
        """
        Gets vocabulary and matrix
        """
        
        X = []
        vocabulary = []
        unique_features = {}

        for text in corpus:
            words = processing(text)
            feature_counter = Counter(words)
            unique_features.update(feature_counter)
            vocabulary.extend([word for word in feature_counter.keys()])
            X.append([feature_counter[word] for word in vocabulary])

        len_vocab = len(vocabulary)
        for row in X:
            zeros_extend = [0] * (len_vocab - len(row))
            row.extend(zeros_extend)
        return vocabulary, X
