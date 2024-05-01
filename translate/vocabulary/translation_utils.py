import Levenshtein as lev


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
