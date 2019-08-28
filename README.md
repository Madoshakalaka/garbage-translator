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
"""
The méxico–United States barrier is a seres of vertical barriers along the méxico–United States bordes aimed at 
preventing ilegal crossings from méxico into the United States. The barrier is not one contiguous structure, but a
 discontinuous seres of physical obstructions variously classified as 'fences' or 'walls'.
"""

>>> gt.translate(text, garbigility=30)
"""
The méxico–United States barrio is a seres of vertical barrios along the méxico–United States bordes aimed at presentan 
llegan crossings from méxico instó the United States. The barrio is not one continuo estructura, but a discontinuous 
seres of physical obstructions variously clasificó as 'fences' or 'walls'.
"""

>>> gt.translate(text, garbigility=40)
"""
Te Mérito–Usted Staples barrio is a seis of vecinal barrio abono te Mérito–Usted Staples borrar anime at pretendido
 llegan crossings from Mérito instó te Usted Staples. Te barrio is notó once consigo estructuras, buk a discóticas seis 
of musical instrucción varios clarifica as 'fauces' or 'allí'.
"""

>>> gt.translate(text, garbigility=50)
"""
Te Maxis–Unión Santos barriendo ir a sordos os vestir batir abono te Maxis–Unión Santos bondad anime a prevemos irreal
 consigo farol Maxis invitó te Unión Santos. Te barriendo ir notó once conteo sepultura, buk a disponibles sordos os
 publica obligaciones valioso calificó así 'francos' o 'allí'.
"""
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


