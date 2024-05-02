from dataclasses import dataclass
import polars as pl

from translate.vocabulary import vocabulary
from translate.vocabulary.translation_utils import meaning_context_score, segment_meaning, strip_explanation


@dataclass
class TranslatedVerbBase:
    verb: str
    meaning: str
    verb_class: str
    pronunciation: str
    active: bool


def is_active(verb: str) -> bool:
    stative_endings = [
        "'en",
        "cet",
        "vh",
        "vhi",
        "non",
        "ak",
        "ge"
    ]

    for ending in stative_endings:
        if verb.endswith(ending):
            return False
    return True


def transform_first_row(values_near: pl.DataFrame) -> TranslatedVerbBase:
    vl = values_near.row(0)
    return TranslatedVerbBase(
        verb=vl[0],
        meaning=vl[3],
        verb_class=vl[4],
        pronunciation=vl[1],
        active=is_active(vl[0])
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
        values_near = values_near.sort(
            pl.col("Meaning").map_elements(lambda x: meaning_context_score(english, x, context_cues),
                                           return_dtype=pl.Int64)
        )

        return transform_first_row(values_near)

    # If we have none, we need to find the closest match using embeddings
    values_near = vocabulary.filter(pl.col("POS") == "v")
    from translate.vocabulary.embedding_utils import most_similar

    all_verb_cols = values_near.to_dicts()
    all_verb_meanings = ["; ".join([strip_explanation(x) for x in segment_meaning(x["Meaning"])]) for x in
                         all_verb_cols]
    col = most_similar(english, all_verb_meanings, all_verb_cols)

    return TranslatedVerbBase(
        verb=col["Word"],
        meaning=col["Meaning"],
        verb_class=col["POS"],
        pronunciation=col["Pronunciation"],
        active=is_active(col["Word"])
    )


if __name__ == '__main__':
    verb = "run"
    print(translate_verb_base(verb))
