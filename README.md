# Garbage Translator
[![PyPI version fury.io](https://badge.fury.io/py/garbage-translator.svg)](https://pypi.python.org/pypi/garbage-translator/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/garbage-translator.svg)](https://pypi.python.org/pypi/garbage-translator/)
![codecov](https://codecov.io/gh/Madoshakalaka/garbage-translator/branch/master/graph/badge.svg)

## Install

`pip install garbage-translator`

## Usage

```python
from garbage_translator import GarbageTranslator as GT

gt = GT.from_list(["hellà", "dankness", "mi", "olt", "frend"])
>>> gt.translate("hello darkness my old friend!", garbigility=50)
"hellà dankness mi olt frend!"
```

## How to have fun

```python
import nltk
from garbage_translator import GarbageTranslator as GT

nltk.download('cess_esp') # download spanish corpus (or whatever language you like)

gt = GT.from_list(list(nltk.corpus.cess_esp.words()))

text = "The Mexico–United States barrier is a series of vertical barriers along" \
" the Mexico–United States border aimed at preventing illegal crossings " \
"from Mexico into the United States. The barrier is not one contiguous structure" \
", but a discontinuous series of physical obstructions variously classified as 'fences' or 'walls'."

>>> gt.translate(text, garbigility=20)
The méxico–United States barrier is a serias of vertical barriers along the méxico–United States borde aimed at 
preventing ilegal crossings from méxico into the United States. The barrier is not one contiguous structure, but 
a discontinuous serias of physical obstructions variously classified as 'fences' or 'walls'.

>>> gt.translate(text, garbigility=30)
The méxico–United States barriles is a serias of vertical barriles along the méxico–United States borde aimed at 
prevenir legal crossings from méxico pintó the United States. The barriles is not one continuas estructura, but a 
discontinuous serias of physical obstructions variously clasificó as 'fences' or 'walls'.

>>> gt.translate(text, garbigility=40)
Te ético–Usted Staples barriles is a Serías of ética Zarrías lona Ché ético–Usted Staples aborde Jaime at preceptivo 
legal crossings from ético pintó Ché Usted Staples. Te barriles is nota One consigue estructural, buk a continuas
 Serías of musical instrucción varios clarifica as 'fuentes' or 'falló'.

>>> gt.translate(text, garbigility=50)
Te cómico–mitad bares bares es a bares ó alérgicas aéreas lona Ché cómico–mitad bares bares Jaime ay prudencial 
relegar cortinas frío cómico rito Ché mitad bares. Te bares es nota One conejos sucre, buk a continúa bares ó 
física brutos Varios clásica es 'mientes' Cr 'falló'.
```




## API

```python
class GarbageTranslator:

    @classmethod
    def from_list(cls, corpus: List[str]) -> "GarbageTranslator":
        """
        :param corpus: words of target language
        """
        ...

    def translate(self, paragraph: str, garbigility: int) -> str:
        """
        :param paragraph: original text
        :param garbigility: from 0 to 100. How garbageous you like your translation to be.
        :return: garbage text
        :raise ValueError: if garbigility is outside interval (0, 100]
        """
        ...
```


