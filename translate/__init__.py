import nltk
from nltk.tree import TreePrettyPrinter

from translate.context import UnknownContextWord
from translate.reducers import ContextReducer


def tx(input: str):
    tokens = nltk.word_tokenize(input)
    tagged = nltk.pos_tag(tokens, tagset="universal")
    ne_chunked = nltk.chunk.ne_chunk(tagged)

    return tokens, tagged, ne_chunked


def pp_tree(tree):
    tpp = TreePrettyPrinter(tree)
    print(tpp.text())

    return input


class MultistageKoiTranslationEngine:
    def __init__(self):
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")
        nltk.download("universal_tagset")

        self.reducer = ContextReducer()

    def digest(self, value: str) -> str:
        tokens, tagged, ne_chunked = tx(value.replace("'m", ""))
        reduced = self.reducer(tagged)
        return value
