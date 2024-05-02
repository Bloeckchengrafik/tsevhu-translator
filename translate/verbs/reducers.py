from translate.reducer_types import *
from translate.verbs import determine_tense_and_affixes


def reduce_and_lint_verbs(context: list[Unknown]):
    if len(context) == 0:
        return []

    outs = [context[0]]

    prev = context[0]
    prev_particle = False
    for word in context[1:]:
        out = word
        if prev.is_verb() and word.is_verb():
            verb = word.value
            if prev_particle:
                tense, affix = determine_tense_and_affixes([prev.value, "to", verb])
                outs = outs[:-2]
            else:
                tense, affix = determine_tense_and_affixes([prev.value, verb])
                outs = outs[:-1]
            out = Verb(verb, tense, affix)
        elif word.is_verb():
            tense, affix = determine_tense_and_affixes([word.value])
            out = Verb(word.value, tense, affix)

        if word.is_particle() and not prev_particle:
            prev_particle = True
        else:
            prev = word
            prev_particle = False

        outs.append(out)

    return outs


def translate_verbs(sentence: str, context: list[Unknown | Verb]):
    for i, word in enumerate(context):
        if isinstance(word, Verb):
            word.value = word.value.removesuffix("ed")
            word.value = word.value.removesuffix("ing")
            # setting -> sett -> set
            if len(word.value) > 2 and word.value[-1] == word.value[-2]:
                word.value = word.value[:-1]
            context[i] = word.translate(sentence)

    return context
