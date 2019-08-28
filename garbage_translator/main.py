from abc import ABC, abstractmethod
from bisect import bisect_left
from collections import defaultdict
from contextlib import contextmanager
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
        sorted_stripped_words: List[str],
        is_accented_language: bool,
        unaccented_to_accented: Dict[str, List[str]],
        accented_corpus: Set[str],
    ):
        self._is_accented = is_accented_language
        self._words = set(sorted_stripped_words)
        self._sorted_words = sorted_stripped_words
        self._unaccented_to_accented = unaccented_to_accented
        self._extra_words = []
        self._accented_corpus = accented_corpus

    def _in_corpus(self, word: str):
        return word in self._words

    def _insert_extra_words(self, inserted_words: Set[str]):
        self._extra_words = [
            unidecode(extra) for extra in inserted_words if not self._in_corpus(extra)
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
        return (
            [
                acc
                for r in results
                for acc in self._unaccented_to_accented[r]
                if acc in self._accented_corpus
            ]
            if self._is_accented
            else results
        )

    def convert_stripped_to_accented(self, word: str) -> List[str]:
        return self._unaccented_to_accented[word]


# should be exposed
class CorpusImporter(ABC):
    def build_corpus(self, words: List[str]) -> ElasticCorpus:
        stripped_to_accented_mapping: DefaultDict[str, List[str]] = defaultdict(list)
        word_set = set(words)
        stripped_words = []
        if self.is_accented_language:
            for word in word_set:
                stripped = unidecode(word)
                stripped_to_accented_mapping[stripped].append(word)
                stripped_words.append(stripped)
        else:
            stripped_words = list(word_set)

        return ElasticCorpus(
            sorted(stripped_words),
            self.is_accented_language,
            stripped_to_accented_mapping,
            word_set,
        )

    @classmethod
    @abstractmethod
    def import_words(cls, *args, **kwargs) -> List[str]:
        ...

    @property
    @abstractmethod
    def is_accented_language(self) -> bool:
        ...


class ListImporter(CorpusImporter):
    # idiotically true
    is_accented_language = True

    @classmethod
    def import_words(cls, word_list: List[str]) -> List[str]:
        return word_list


class GarbageTranslator:

    _corpus: Optional[ElasticCorpus]

    def __init__(self, importer_class: Type[CorpusImporter]):
        self._corpus_importer = importer_class()

        self._corpus = None

    @classmethod
    def from_list(cls, corpus: List[str]) -> "GarbageTranslator":
        """
        :param corpus: words
        """
        gt = cls(ListImporter)

        gt.import_corpus(corpus)
        return gt

    def import_corpus(self, *args, **kwargs):
        words = self._corpus_importer.import_words(*args, **kwargs)
        self._corpus = self._corpus_importer.build_corpus(words)

    def translate(self, paragraph: str, garbigility: int) -> str:
        """
        :param paragraph: original text
        :param garbigility: from 0 to 100. How garbageous you like your translation to be.
        :return: garbage text
        :raise ValueError: if garbigility is outside interval (0, 100]
        """
        if garbigility <= 0 or garbigility > 100:
            raise ValueError("Garbigility must be in interval (0,100]")

        word_buffer = ""

        garbage_text = ""

        old_c = ""
        for c in paragraph + " ":

            if c in ascii_letters:
                word_buffer += c
            else:
                if old_c in ascii_letters and old_c != "":
                    garbage_word = self._translate_word(word_buffer, garbigility)

                    garbage_text += garbage_word
                    word_buffer = ""
                garbage_text += c
            old_c = c
        return garbage_text[:-1]

    def _translate_word(self, regular_word: str, garbigility: int) -> str:
        upper_limit = len(regular_word) * garbigility // 100
        if upper_limit == 0:
            return regular_word

        with self._corpus.extra_words_inserted({regular_word}) as bloated:
            searcher = FuzzySearcher(bloated)

            distance = upper_limit - 1
            the_garbage: Optional[str] = None
            more_garbageous: Set[str] = set(searcher.search(regular_word, upper_limit))

            while distance >= 0:
                less_garbageous: Set[str] = set(searcher.search(regular_word, distance))
                potential_garbages = more_garbageous - less_garbageous
                if potential_garbages:
                    the_garbage = potential_garbages.pop()
                    break
                distance -= 1

            return the_garbage if the_garbage is not None else regular_word
