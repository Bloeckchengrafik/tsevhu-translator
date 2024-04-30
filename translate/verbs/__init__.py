from enum import Enum

from translate.verbs.context import FluidTense, VerbAffixes, DiscreteTense
from translate.verbs.english_tense_bs import is_irregular_participle


class EnglishTense(Enum):
    NONFINITE = -1
    PRESENT_SIMPLE = 0
    PRESENT_CONTINUOUS = 1
    PRESENT_PERFECT = 2
    PRESENT_PERFECT_CONTINUOUS = 3
    PAST_SIMPLE = 4
    PAST_CONTINUOUS = 5
    PAST_PERFECT = 6
    PAST_PERFECT_CONTINUOUS = 7
    FUTURE_SIMPLE = 8
    FUTURE_CONTINUOUS = 9
    FUTURE_PERFECT = 10
    FUTURE_PERFECT_CONTINUOUS = 11

    def is_continuous(self):
        return self in [EnglishTense.PRESENT_CONTINUOUS, EnglishTense.PAST_CONTINUOUS, EnglishTense.FUTURE_CONTINUOUS,
                        EnglishTense.PRESENT_PERFECT_CONTINUOUS, EnglishTense.PAST_PERFECT_CONTINUOUS,
                        EnglishTense.FUTURE_PERFECT_CONTINUOUS]

    def to_discrete(self) -> DiscreteTense:
        match self:
            case EnglishTense.PRESENT_SIMPLE:
                return DiscreteTense.PRESENT
            case EnglishTense.PRESENT_CONTINUOUS:
                return DiscreteTense.PRESENT
            case EnglishTense.PRESENT_PERFECT:
                return DiscreteTense.PRESENT
            case EnglishTense.PRESENT_PERFECT_CONTINUOUS:
                return DiscreteTense.PRESENT
            case EnglishTense.PAST_SIMPLE:
                return DiscreteTense.RECENT_PAST
            case EnglishTense.PAST_CONTINUOUS:
                return DiscreteTense.RECENT_PAST
            case EnglishTense.PAST_PERFECT:
                return DiscreteTense.RECENT_PAST
            case EnglishTense.PAST_PERFECT_CONTINUOUS:
                return DiscreteTense.RECENT_PAST
            case EnglishTense.FUTURE_SIMPLE:
                return DiscreteTense.NEAR_FUTURE
            case EnglishTense.FUTURE_CONTINUOUS:
                return DiscreteTense.NEAR_FUTURE
            case EnglishTense.FUTURE_PERFECT:
                return DiscreteTense.NEAR_FUTURE
            case EnglishTense.FUTURE_PERFECT_CONTINUOUS:
                return DiscreteTense.NEAR_FUTURE
            case _:
                return DiscreteTense.NONFINITE


POSSIBLE_TO_BE = ["am", "is", "are", "was", "were", "being", "been"]
POSSIBLE_TO_HAVE = ["have", "has", "had", "having"]
POSSIBLE_TO_DO = ["do", "does", "did", "doing"]
AUXILIARY_VERBS = POSSIBLE_TO_BE + POSSIBLE_TO_HAVE + POSSIBLE_TO_DO

TO_BE_SIMPLE_TENSES = {
    "am": EnglishTense.PRESENT_SIMPLE,
    "is": EnglishTense.PRESENT_SIMPLE,
    "are": EnglishTense.PRESENT_SIMPLE,
    "was": EnglishTense.PAST_SIMPLE,
    "were": EnglishTense.PAST_SIMPLE,
    "being": EnglishTense.PRESENT_CONTINUOUS,
}

TO_HAVE_SIMPLE_TENSES = {
    "have": EnglishTense.PRESENT_SIMPLE,
    "has": EnglishTense.PRESENT_SIMPLE,
    "had": EnglishTense.PAST_SIMPLE,
    "having": EnglishTense.PRESENT_CONTINUOUS,
}

TO_DO_SIMPLE_TENSES = {
    "do": EnglishTense.PRESENT_SIMPLE,
    "does": EnglishTense.PRESENT_SIMPLE,
    "did": EnglishTense.PAST_SIMPLE,
    "doing": EnglishTense.PRESENT_CONTINUOUS,
}

TIMENESS_AUXILIARY_VERBS = TO_DO_SIMPLE_TENSES | TO_HAVE_SIMPLE_TENSES | TO_BE_SIMPLE_TENSES

FUTURE_AUX = ["will", "shall", "gonna", "going"]


def determine_tense_and_affixes(verbs: list[str]) -> (FluidTense, VerbAffixes):
    """
    Determines the tense of the English verb and returns the appropriate FluidTense and Affixes object.
    """

    # Auxiliary verbs alone
    if (len(verbs) == 1) and (verbs[0] in AUXILIARY_VERBS):
        if verbs[0] in POSSIBLE_TO_BE:
            return (
                FluidTense(TO_BE_SIMPLE_TENSES[verbs[0]].to_discrete().value),
                VerbAffixes.CONTINUOUS if TO_BE_SIMPLE_TENSES[
                    verbs[0]].is_continuous() else VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
            )

        if verbs[0] in POSSIBLE_TO_HAVE:
            return (
                FluidTense(TO_HAVE_SIMPLE_TENSES[verbs[0]].to_discrete().value),
                VerbAffixes.CONTINUOUS if TO_HAVE_SIMPLE_TENSES[
                    verbs[0]].is_continuous() else VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
            )

        if verbs[0] in POSSIBLE_TO_DO:
            return (
                FluidTense(TO_DO_SIMPLE_TENSES[verbs[0]].to_discrete().value),
                VerbAffixes.CONTINUOUS if TO_DO_SIMPLE_TENSES[
                    verbs[0]].is_continuous() else VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
            )

    # Auxiliary verbs with main verb
    if (len(verbs) == 2) and (verbs[0] in AUXILIARY_VERBS):
        """
        either:
        - present continuous
        - present perfect
        - past continuous
        - past perfect
        - future continuous
        - future perfect
        """
        aux_time: EnglishTense = TIMENESS_AUXILIARY_VERBS[verbs[0]]
        main_continuous = verbs[1].endswith("ing")

        if aux_time == EnglishTense.PRESENT_SIMPLE:
            if main_continuous:
                return (
                    FluidTense(EnglishTense.PRESENT_CONTINUOUS.to_discrete().value),
                    VerbAffixes.CONTINUOUS
                )
            else:
                return (
                    FluidTense(EnglishTense.PRESENT_PERFECT.to_discrete().value),
                    VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
                )

        if aux_time == EnglishTense.PAST_SIMPLE:
            if main_continuous:
                return (
                    FluidTense(EnglishTense.PAST_CONTINUOUS.to_discrete().value),
                    VerbAffixes.CONTINUOUS
                )
            else:
                return (
                    FluidTense(EnglishTense.PAST_PERFECT.to_discrete().value),
                    VerbAffixes.RETROSPECTIVE
                )

        if aux_time == EnglishTense.FUTURE_SIMPLE:
            if main_continuous:
                return (
                    FluidTense(EnglishTense.FUTURE_CONTINUOUS.to_discrete().value),
                    VerbAffixes.CONTINUOUS
                )
            else:
                return (
                    FluidTense(EnglishTense.FUTURE_PERFECT.to_discrete().value),
                    VerbAffixes.PROSPECTIVE
                )

    # Tri-verb constructions
    if (len(verbs) == 3) and (verbs[0] in AUXILIARY_VERBS) or (verbs[0] in FUTURE_AUX):
        """
        either:
        - present perfect continuous
        - past perfect continuous
        - future perfect continuous
        """
        aux_time: EnglishTense = TIMENESS_AUXILIARY_VERBS.get(verbs[0])
        is_future = verbs[0] in FUTURE_AUX
        main_continuous = verbs[2].endswith("ing")

        if aux_time == EnglishTense.PRESENT_SIMPLE and main_continuous:
            # Present perfect continuous
            return (
                FluidTense(EnglishTense.PRESENT_PERFECT_CONTINUOUS.to_discrete().value),
                VerbAffixes.CONTINUOUS
            )

        if aux_time == EnglishTense.PAST_SIMPLE and main_continuous:
            # Past perfect continuous
            return (
                FluidTense(EnglishTense.PAST_PERFECT_CONTINUOUS.to_discrete().value),
                VerbAffixes.CONTINUOUS
            )

        if is_future and main_continuous:
            # Future perfect continuous
            return (
                FluidTense(EnglishTense.FUTURE_PERFECT_CONTINUOUS.to_discrete().value),
                VerbAffixes.CONTINUOUS
            )
        elif is_future:
            # "Going to" future
            return (
                FluidTense(EnglishTense.FUTURE_SIMPLE.to_discrete().value),
                VerbAffixes.PROSPECTIVE
            )

    # Main verb alone
    if len(verbs) == 1:
        if verbs[0].endswith("ing"):
            return (
                FluidTense(EnglishTense.PRESENT_CONTINUOUS.to_discrete().value),
                VerbAffixes.CONTINUOUS
            )
        elif is_irregular_participle(verbs[0]) or verbs[0].endswith("ed"):
            return (
                FluidTense(EnglishTense.PAST_PERFECT.to_discrete().value),
                VerbAffixes.RETROSPECTIVE
            )
        else:
            return (
                FluidTense(EnglishTense.PRESENT_SIMPLE.to_discrete().value),
                VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
            )

    return (
        FluidTense(EnglishTense.NONFINITE.to_discrete().value),
        VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE
    )


def verb_is_active(tsevhu: str) -> bool:
    passive_endings = ["'en", "cet", "vh", "vhi", "non", "ak", "ge"]
    return not any([tsevhu.endswith(ending) for ending in passive_endings])


if __name__ == '__main__':
    print(determine_tense_and_affixes(input("Enter a verb: ").split()))
