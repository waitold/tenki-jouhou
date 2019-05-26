from pykakasi import kakasi


def to_english(kanji):
    kakashi = kakasi()
    kakashi.setMode('J', 'a')
    conv = kakashi.getConverter()
    text = conv.do(kanji)
    return text

