import os
from pprint import pprint
from translate.log import tx_info
from translate.nouns.reducers import det_nouns, contextualize_nouns, translate_nouns
from translate.reducer_types import *
from translate.verbs.reducers import reduce_and_lint_verbs, translate_verbs
from translate.vocabulary.reducers import compile_sentence


def run_reducer(tagged: list[tuple[str, str]], full):
    reducer_ctx = [UnknownContextWord(wrd, clue) for wrd, clue in tagged]

    debuggers = os.environ.get("DEBUG", "").split(",")
    if "all" in debuggers:
        debuggers = ["red", "cver", "tver", "dnn", "cnn", "ver", "nn", "tnn"]

    tx_info("Starting Context Reduction")
    if "red" in debuggers:
        pprint(reducer_ctx)

    tx_info("Contextualizing Verbs")
    reducer_ctx = reduce_and_lint_verbs(reducer_ctx)

    if "cver" in debuggers or "ver" in debuggers:
        pprint(reducer_ctx)

    tx_info("Translating Verbs")
    reducer_ctx = translate_verbs(full, reducer_ctx)

    if "tver" in debuggers or "ver" in debuggers:
        pprint(reducer_ctx)

    tx_info("Inferring Noun determiners")
    reducer_ctx = det_nouns(reducer_ctx)
    if "dnn" in debuggers or "nn" in debuggers:
        pprint(reducer_ctx)

    tx_info("Contextualizing Nouns")
    reducer_ctx = contextualize_nouns(reducer_ctx, "cnn" in debuggers or "nn" in debuggers)
    if "cnn" in debuggers or "nn" in debuggers:
        pprint(reducer_ctx)

    tx_info("Translating Nouns")
    reducer_ctx = translate_nouns(reducer_ctx)
    if "nn" in debuggers or "tnn" in debuggers:
        pprint(reducer_ctx)

    tx_info("Building Sentence")
    compiled = compile_sentence(full, reducer_ctx)

    return compiled
