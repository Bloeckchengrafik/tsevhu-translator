import nltk
from nltk.tree import TreePrettyPrinter

from translate.context import UnknownContextWord
from translate.reducers import run_reducer


def tx(value: str):
    tokens = nltk.word_tokenize(value)
    tagged = nltk.pos_tag(tokens, tagset="universal")
    ne_chunked = nltk.chunk.ne_chunk(tagged)

    return tokens, tagged, ne_chunked


def pp_tree(tree):
    tpp = TreePrettyPrinter(tree)
    print(tpp.text())

    return input


class MultistageKoiTranslationEngine:
    def __init__(self):
        deps = ["punkt", "averaged_perceptron_tagger", "maxent_ne_chunker", "words"]
        for dep in deps:
            nltk.download(dep, quiet=True)

    def digest(self, value: str) -> str:
        tokens, tagged, ne_chunked = tx(value.replace("'m", ""))
        return run_reducer(tagged, value)
