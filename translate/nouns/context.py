from dataclasses import dataclass
from enum import Enum

from translate.context.compile import Compileable


class Determiner(Enum):
    DEFINITE = 1
    INDEFINITE = 2

    def __str__(self):
        return f"{self.name}"

    def translate_active_plural(self):
        if self == Determiner.DEFINITE:
            return "na"
        else:
            return "vai"

    def translate_passive_plural(self):
        if self == Determiner.DEFINITE:
            return "ul"
        else:
            return "vu"

    def translate_active_singular(self):
        if self == Determiner.DEFINITE:
            return ""
        else:
            return "ha"

    def translate_passive_singular(self):
        if self == Determiner.DEFINITE:
            return "vn"
        else:
            return "sy"

    def translate_active(self, plural):
        if plural:
            return self.translate_active_plural()
        else:
            return self.translate_active_singular()

    def translate_passive(self, plural):
        if plural:
            return self.translate_passive_plural()
        else:
            return self.translate_passive_singular()

    def translate(self, active: bool, plural: bool):
        if active:
            return self.translate_active(plural)
        else:
            return self.translate_passive(plural)


@dataclass
class DeterminedNoun:
    value: str
    determiner: Determiner = Determiner.DEFINITE
    plural: bool = False
    active: bool = True

    def __str__(self):
        return f"<DN:{self.value} ({self.determiner})>"


@dataclass
class TranslatedNoun(Compileable):
    value: str
    determiner: str
    meaning: str
    base: DeterminedNoun

    def __str__(self):
        return f"<TN:{self.value} ({self.determiner})>"

    def compile(self, punctuation_mark: str) -> str:
        return f"{self.determiner} {self.value}".strip()
