from typing import List
import pytest
from garbage_translator.main import ElasticCorpus


@pytest.mark.parametrize("corpus_words", (["a", "b", "c"], ["a", "e", "f"], ["e", "f"]))
@pytest.mark.parametrize("extras", (["d"], ["e"], ["f"], ["a"], ["a", "e", "f"]))
def test_elastic_corpus(corpus_words: List[str], extras: List[str]):
    corpus_words.sort()
    corpus = ElasticCorpus(corpus_words, False, {}, corpus_words)
    original_corpus_words = corpus_words.copy()
    with corpus.extra_words_inserted(set(extras)) as bloated:
        assert bloated._sorted_words == sorted(bloated._sorted_words)
        assert set(bloated._sorted_words) == set(
            original_corpus_words + extras
        ) and len(set(bloated._sorted_words)) == len(bloated._sorted_words)
    assert corpus._sorted_words == original_corpus_words
