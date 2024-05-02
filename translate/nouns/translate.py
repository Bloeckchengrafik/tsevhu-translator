from translate.nouns.context import TranslatedNoun, DeterminedNoun
from translate.vocabulary import vocabulary
import polars as pl
from translate.vocabulary.embedding_utils import most_similar

from translate.vocabulary.translation_utils import meanings_distance, strip_explanation, segment_meaning


def translate_determined_noun(noun: DeterminedNoun) -> TranslatedNoun:
    values_near = vocabulary.filter(
        pl.col("Meaning").str.contains(noun.value) & (pl.col("POS") == "n")
    )

    # Got one? Great! Return it.
    if len(values_near) == 1:
        col = values_near.head(1).to_dicts()[0]
        return TranslatedNoun(
            value=col["Word"],
            determiner=noun.determiner.translate(noun.active, noun.plural),
            base=noun,
            meaning=col["Meaning"]
        )

    # If we have more than one, we need to filter by length and context cues
    if len(values_near) > 1:
        values_near = values_near.sort(
            pl.col("Meaning").map_elements(lambda x: meanings_distance(noun.value, x), return_dtype=pl.Int64)
        )

        col = values_near.head(1).to_dicts()[0]

        return TranslatedNoun(
            value=col["Word"],
            determiner=noun.determiner.translate(noun.active, noun.plural),
            base=noun,
            meaning=col["Meaning"]
        )

    # If we have none, we need to find the closest match using embeddings
    values_near = vocabulary.filter(pl.col("POS") == "n")

    all_noun_cols = values_near.to_dicts()
    all_verb_meanings = ["; ".join([strip_explanation(x) for x in segment_meaning(x["Meaning"])]) for x in
                         all_noun_cols]
    col = most_similar(noun.value, all_verb_meanings, all_noun_cols)

    return TranslatedNoun(
        value=col["Word"],
        determiner=noun.determiner.translate(noun.active, noun.plural),
        base=noun,
        meaning=col["Meaning"]
    )
