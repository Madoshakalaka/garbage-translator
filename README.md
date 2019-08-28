# Garbage Translator

## Usage

```python
from garbage_translator import GarbageTranslator as GT

gt = GT.from_list(["hellà", "dankness", "mi", "olt", "frend"])
gt.translate("hello darkness my old friend!", 50)

>>> "hellà dankness mi olt frend!"
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


