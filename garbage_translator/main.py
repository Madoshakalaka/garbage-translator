from abc import ABC, abstractmethod
from bisect import bisect_left
from collections import defaultdict
from contextlib import contextmanager
from functools import update_wrapper
from string import ascii_letters
from typing import List, Dict, DefaultDict, Iterable, Optional, Type, Set

from unidecode import unidecode

from garbage_translator.fuzzy_searcher import (
    OrderedIterableCorpus,
    SupportsStr,
    FuzzySearcher,
)


# not exposed
class ElasticCorpus(OrderedIterableCorpus[str]):
    _extra_word_indexes: Dict[str, int]
    _words: Set[str]
    _extra_words: List[str]
    _unaccented_to_accented: Dict[str, List[str]]

    def __init__(
        self,
        sorted_words: List[str],
        is_accented_language: bool,
        unaccented_to_accented: Dict[str, List[str]],
    ):
        self._is_accented = is_accented_language
        self._words = set(sorted_words)
        self._sorted_words = sorted_words
        self._unaccented_to_accented = unaccented_to_accented
        self._extra_words = []

    def _in_corpus(self, word: str):
        return word in self._words

    def _insert_extra_words(self, inserted_words: Set[str]):
        self._extra_words = [
            extra for extra in inserted_words if not self._in_corpus(extra)
        ]
        for extra in self._extra_words:
            pos = bisect_left(self._sorted_words, extra)
            self._sorted_words.insert(pos, extra)

    def _remove_extra_words(self):
        for w in self._extra_words:
            pos = bisect_left(self._sorted_words, w)
            self._sorted_words.pop(pos)

    @contextmanager
    def extra_words_inserted(self, words: Set[str]) -> Iterable["ElasticCorpus"]:
        try:
            self._insert_extra_words(words)
            yield self
        finally:
            self._remove_extra_words()

    def get_next_smaller(self, lookup_string: str) -> Optional[SupportsStr]:
        pos = bisect_left(self._sorted_words, lookup_string)
        if pos < len(self._sorted_words):
            return self._sorted_words[pos]
        else:
            return None

    def strings_to_elements(self, results: List[str]) -> Iterable[str]:
        return [
            acc
            for r in results
            for acc in self._unaccented_to_accented[r]
            if r in self._words
        ]

    def convert_stripped_to_accented(self, word: str) -> List[str]:
        return self._unaccented_to_accented[word]


# should be exposed
class CorpusImporter(ABC):
    def build_corpus(self, words) -> ElasticCorpus:
        stripped_to_accented_mapping = defaultdict(list)
        if self.is_accented_language:
            stripped_to_accented_mapping: DefaultDict[str, List[str]] = defaultdict(
                list
            )
            for word in words:
                stripped_to_accented_mapping[word].append(unidecode(word))

        return ElasticCorpus(
            sorted(words), self.is_accented_language, stripped_to_accented_mapping
        )

    @classmethod
    @abstractmethod
    def import_words(cls, *args, **kwargs) -> List[str]:
        ...

    @property
    @abstractmethod
    def is_accented_language(self) -> bool:
        ...


class GarbageTranslator:
    _corpus_a: Optional[ElasticCorpus]
    _corpus_b: Optional[ElasticCorpus]

    def __init__(
        self,
        importer_a_class: Type[CorpusImporter],
        importer_b_class: Type[CorpusImporter],
    ):
        self._corpus_a_importer = importer_a_class()
        self._corpus_b_importer = importer_b_class()

        update_wrapper(self.import_corpus_a, importer_a_class.import_words)
        update_wrapper(self.import_corpus_b, importer_b_class.import_words)
        self._corpus_a = None
        self._corpus_b = None

    def import_corpus_a(self, *args, **kwargs):
        words = self._corpus_a_importer.import_words(*args, **kwargs)
        self._corpus_a = self._corpus_a_importer.build_corpus(words)

    def import_corpus_b(self, *args, **kwargs):
        words = self._corpus_b_importer.import_words(*args, **kwargs)
        self._corpus_b = self._corpus_b_importer.build_corpus(words)

    def translate(self, paragraph: str, garbigility: int) -> str:
        """
        Direction is A to B.
        """
        word_buffer = ""

        garbage_text = ""

        old_c = ""
        for c in paragraph:

            if c in ascii_letters:
                word_buffer += c
            else:
                if old_c in ascii_letters and old_c != "":
                    garbage_word = self._translate_word(word_buffer, garbigility)

                    garbage_text += garbage_word
                    word_buffer = ""
                garbage_text += c
            old_c = c
        return garbage_text

    def _translate_word(self, regular_word: str, garbigility: int) -> str:
        with self._corpus_b.extra_words_inserted({regular_word}) as bloated:
            searcher = FuzzySearcher(bloated)
            dank_words = searcher.search(regular_word, garbigility)
