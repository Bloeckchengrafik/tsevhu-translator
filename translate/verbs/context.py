import enum
from dataclasses import dataclass

from translate.context.compile import Compileable
from translate.letters import VOWELS
from translate.verbs.mood import VerbMoodPartices
from translate.vocabulary import translate_verb
from translate.vocabulary.translate_verb import TranslatedVerbBase


class DiscreteTense(enum.Enum):
    """
    Discrete tenses are used to represent the seven tenses in the language.
    These are used for translating to shorthand and romanized.
    To translate to koiwrit, use fluid tenses instead, since the direction of the fish can have more than 7 values.
    """
    NONFINITE = None
    REMOTE_PAST = -3
    MEDIAL_PAST = -2
    RECENT_PAST = -1
    PRESENT = 0
    NEAR_FUTURE = 1
    MEDIAL_FUTURE = 2
    REMOTE_FUTURE = 3

    def to_romanized_particle(self):
        match self:
            case DiscreteTense.REMOTE_PAST:
                return "bae"
            case DiscreteTense.MEDIAL_PAST:
                return "xir"
            case DiscreteTense.RECENT_PAST:
                return "ci"
            case DiscreteTense.PRESENT:
                return ""
            case DiscreteTense.NEAR_FUTURE:
                return "nui"
            case DiscreteTense.MEDIAL_FUTURE:
                return "asi"
            case DiscreteTense.REMOTE_FUTURE:
                return "vhut"
            case _:
                return "i'li"


@dataclass
class FluidTense:
    value: int | None

    def to_discrete(self) -> DiscreteTense:
        if self.value is None:
            return DiscreteTense.PRESENT

        # Get nearest discrete tense
        nearest_tense = min(list(DiscreteTense),
                            key=lambda x: abs(x.value - self.value) if x.value is not None else 1000000)

        return DiscreteTense(nearest_tense)

    def __repr__(self):
        return f"<FluidTense {self.value} ({self.to_discrete().name})>"

    def to_romanized_particle(self) -> str:
        # TODO implement adjacent verbs particles
        return self.to_discrete().to_romanized_particle()


class VerbAffixes(enum.Enum):
    CONTINUOUS = 1
    INTERROGATIVE = 2
    IMPERATIVE = 3
    PROSPECTIVE = 4
    PERFPECTIVE = 5
    RETROSPECTIVE = 6
    UNDECIDED_IMPERATIVE_INTERROGATIVE = 7

    def apply_particle(self, value: str, mark: str):
        if self == VerbAffixes.CONTINUOUS:
            return value  # Default is continuous
        elif self == VerbAffixes.PROSPECTIVE:
            if value[0] in VOWELS:
                return "th" + value
            else:
                return "vii" + value
        elif self == VerbAffixes.RETROSPECTIVE:
            if value[0] in VOWELS:
                return "otj" + value
            else:
                return "osy" + value
        elif self == VerbAffixes.IMPERATIVE:
            return "a" + value + "t"
        elif self == VerbAffixes.INTERROGATIVE:
            return "y" + value + "n"
        elif self == VerbAffixes.PERFPECTIVE:
            return "sy" + value
        elif self == VerbAffixes.UNDECIDED_IMPERATIVE_INTERROGATIVE:
            if mark == "?":
                return "y" + value + "n"
            elif mark == "!":
                return "a" + value + "t"
            else:
                return value

        return value


@dataclass
class Verb:
    value: str
    tense: FluidTense = lambda: FluidTense(None)
    affix: VerbAffixes = lambda: VerbAffixes.CONTINUOUS

    def translate(self, sentence: str, context: list[str] = None):
        ctx = context or []
        ctx.extend(self.tense.to_discrete().name.lower().split(" "))
        ctx.extend(self.affix.name.lower().split(" "))

        mood = VerbMoodPartices.particles_for(sentence)

        record: TranslatedVerbBase = translate_verb.translate_verb_base(self.value, ctx)
        return TranslatedVerb(
            english=self.value,
            tsevhu=record.verb,
            translated_base=record,
            tense=self.tense,
            affix=self.affix,
            mood=mood
        )

    def __str__(self):
        return f"<V:{self.value}>"


@dataclass
class TranslatedVerb(Compileable):
    english: str
    tsevhu: str
    translated_base: TranslatedVerbBase
    tense: FluidTense = lambda: FluidTense(None)
    affix: VerbAffixes = lambda: VerbAffixes.CONTINUOUS
    mood: list[VerbMoodPartices] = lambda: []

    def compile(self, punctuation_mark: str) -> str:
        tense_part = self.tense.to_romanized_particle()
        affix_part = self.affix.apply_particle(self.tsevhu, punctuation_mark)
        particle = ""  # VerbMoodPartices.concat(self.mood) todo fix
        return f"{particle} {affix_part} {tense_part}".strip().replace("  ", " ")

    def __str__(self):
        return f"<V:{self.tsevhu}>"
