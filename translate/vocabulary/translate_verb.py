from dataclasses import dataclass
import polars as pl
import Levenshtein as lev

from translate.vocabulary import vocabulary


@dataclass
class TranslatedVerbBase:
    verb: str
    meaning: str
    verb_class: str
    pronunciation: str


def segment_meaning(meaning: str) -> list[str]:
    return meaning.split(";")


def strip_explanation(string: str) -> str:
    # remove anything in parentheses
    return string.split("(")[0].strip()


def get_explanation(string: str) -> str:
    try:
        return string.split("(")[1].split(")")[0].strip()
    except IndexError:
        return ""


def meanings_distance(meaning: str, target: str) -> int:
    meanings = [strip_explanation(x) for x in segment_meaning(meaning)]
    return min([lev.distance(target, x) for x in meanings])


def context_cues_distance(target: str, context_cues: list[str] = None) -> int:
    if context_cues is None:
        return 0

    explanations = [x for x in [get_explanation(x) for x in segment_meaning(target)] if x]
    # max amount of context clues found in any explanation
    return max([len([x for x in context_cues if x in explanation]) for explanation in explanations])


def meaning_context_score(target: str, meaning: str, context_cues: list[str] = None):
    try:
        return meanings_distance(meaning, target) + context_cues_distance(meaning, context_cues)
    except ValueError:
        return 1000000


def transform_first_row(values_near: pl.DataFrame) -> TranslatedVerbBase:
    vl = values_near.row(0)
    return TranslatedVerbBase(
        verb=vl[0],
        meaning=vl[3],
        verb_class=vl[4],
        pronunciation=vl[1]
    )


def translate_verb_base(english: str, context_cues: list[str] = None):
    values_near = vocabulary.filter(
        pl.col("Meaning").str.contains(english) & (pl.col("POS") == "v")
    )

    # Got one? Great! Return it.
    if len(values_near) == 1:
        return transform_first_row(values_near)

    # If we have more than one, we need to filter by length and context cues
    if len(values_near) > 1:
        print(values_near.head(5))
        values_near = values_near.sort(
            pl.col("Meaning").map_elements(lambda x: meaning_context_score(english, x, context_cues),
                                           return_dtype=pl.Int64)
        )

        return transform_first_row(values_near)

    # If we have none, we need to find the closest match using embeddings
    values_near = vocabulary.filter(pl.col("POS") == "v")
    from translate.vocabulary.embedding_utils import most_similar

    all_verb_cols = values_near.to_dicts()
    all_verb_meanings = ["; ".join([strip_explanation(x) for x in segment_meaning(x["Meaning"])]) for x in all_verb_cols]
    col = most_similar(english, all_verb_meanings, all_verb_cols)

    return TranslatedVerbBase(
        verb=col["Word"],
        meaning=col["Meaning"],
        verb_class=col["POS"],
        pronunciation=col["Pronunciation"]
    )


if __name__ == '__main__':
    verb = "corndog"
    print(translate_verb_base(verb))
