from translate.log import tx_info, tx_debug
from translate.nouns.context import Determiner, TranslatedNoun
from translate.nouns.translate import translate_determined_noun
from translate.reducer_types import *


def create_determined_noun(word: UnknownContextWord, determiner: UnknownContextWord | None) -> DeterminedNoun:
    if determiner is None:
        return DeterminedNoun(word.value)

    if determiner.value == "a" or determiner.value == "an":
        return DeterminedNoun(word.value, Determiner.INDEFINITE)
    elif determiner.value == "the":
        return DeterminedNoun(word.value, Determiner.DEFINITE)
    else:
        return DeterminedNoun(word.value)


def det_nouns(context: list[Unknown | TVerb]) -> list[Unknown | TVerb | DNoun]:
    out = []
    last_was_determiner = False
    for word in context:
        if isinstance(word, UnknownContextWord):
            if word.nlp_tag == "NOUN":
                out.append(create_determined_noun(word, out.pop() if last_was_determiner else None))
                last_was_determiner = False
            elif word.nlp_tag == "DET":
                last_was_determiner = True
                out.append(word)
        else:
            out.append(word)

    return out


def find_nearest_verb(context: list[Unknown | TVerb | DNoun], index: int) -> TVerb | None:
    left = index - 1
    right = index + 1

    while left >= 0 or right < len(context):
        if left >= 0:
            if isinstance(context[left], TranslatedVerb):
                return context[left]
            left -= 1
        if right < len(context):
            if isinstance(context[right], TranslatedVerb):
                return context[right]
            right += 1

    return None


def contextualize_noun(noun: DNoun, verb: TVerb, dbg: bool):
    noun.active = verb.translated_base.active
    if dbg:
        tx_debug(f"Contextualized {noun.value} to active={noun.active}")


def contextualize_nouns(context: list[Unknown | TVerb | DNoun], dbg: bool) -> list[Unknown | TVerb | DNoun]:
    # find noun -> find nearest verb -> run function to get context
    for i, word in enumerate(context):
        if isinstance(word, DeterminedNoun):
            verb = find_nearest_verb(context, i)
            if verb is not None:
                contextualize_noun(word, verb, dbg)

    return context


def translate_if_noun(noun: DNoun | Unknown) -> TranslatedNoun | Unknown:
    if isinstance(noun, DeterminedNoun):
        return translate_determined_noun(noun)
    else:
        return noun


def translate_nouns(context: list[Unknown | TVerb | DNoun]) -> list[Unknown | TVerb | TranslatedNoun]:
    return [translate_if_noun(word) for word in context]
