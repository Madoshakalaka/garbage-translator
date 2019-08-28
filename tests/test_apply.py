from garbage_translator import GarbageTranslator as GT


def test_apply():
    gt = GT.from_list(["hellà", "dankness", "mi", "olt", "frend"])
    garbage = gt.translate("hello darkness my old friend!", 50)
    assert garbage == "hellà dankness mi olt frend!"
