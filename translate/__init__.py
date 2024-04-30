from typing import Callable
import nltk
from nltk.tree import TreePrettyPrinter

def tx(input: str):
    tokens = nltk.word_tokenize(input)
    tagged = nltk.pos_tag(tokens)
    ne_chunked = nltk.chunk.ne_chunk(tagged)

    return tokens, tagged, ne_chunked

def pp_tree(input):
    tree = input[2]
    tpp = TreePrettyPrinter(tree)
    print(tpp.text())

    return input

class MultistageKoiTranslationEngine:
    def __init__(self):
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")
        nltk.download("maxent_ne_chunker")
        nltk.download("words")

        self.passes: list[Callable] = [
            tx,
            pp_tree
        ]

    def digest(self, input: str) -> str:
        for t_pass in self.passes:
            input = t_pass(input)
        return input
