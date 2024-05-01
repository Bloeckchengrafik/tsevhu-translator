import enum
from translate.vocabulary.embedding_utils import *


class VerbMoodPartices(enum.Enum):
    HYPOTHETICAL = "hmaei"
    CONSEQUENTIAL = "hmaeci"
    INEVITABLE = "hmo"
    WILLING = "hmoi"
    ABILITY = "hma"
    HABITUAL = "hmai"
    PERMISSIVE = "hvu"
    SUGGESTIVE = "hmai"
    NESSESATIVE = "hde"
    DESIRATIVE = "hdei"
    DEDUCTIVE = "hku"
    DEONTIC = "hkui"
    SPECULATIVE = "hsen"
    POTENTIAL = "hseni"

    def is_in_pair(self, other: "VerbMoodPartices") -> bool:
        return self.value == other.value[:-1] or self.value[:-1] == other.value

    @staticmethod
    def concat(particles: list["VerbMoodPartices"]) -> str:
        # -ci when combining two of the same pair; drop second h- when combining two of different pair
        if len(particles) == 0:
            return ""
        elif len(particles) == 1:
            return particles[0].value

        # try to group particles
        grouped = []
        for particle in particles:
            for group in grouped:
                if group[0].is_in_pair(particle):
                    group.append(particle)
                    break
            else:
                grouped.append([particle])

        string = []
        for group in grouped:
            if len(group) == 1:
                string.append(group[0].value)
            else:
                a, b = group
                if a.value == b.value:
                    string.append(a.value)
                else:
                    string.append(a.value + b.value[1:])

        return "ci".join(string)

    @staticmethod
    def particles_for(sentence: str):
        particles = []
        if hypotheticalness(sentence) > 2:
            particles.append(VerbMoodPartices.HYPOTHETICAL)
        if consequentialness(sentence) > 2:
            particles.append(VerbMoodPartices.CONSEQUENTIAL)

        if willingness(sentence) < -2:
            particles.append(VerbMoodPartices.INEVITABLE)
        if willingness(sentence) > 2:
            particles.append(VerbMoodPartices.WILLING)

        # if habitualness(sentence) > 2: todo this is buggy
        #     particles.append(VerbMoodPartices.HABITUAL)
        # todo ability

        # todo permissive
        # todo suggestive

        if desirability(sentence) < -2:
            particles.append(VerbMoodPartices.NESSESATIVE)
        if desirability(sentence) > 2 and not affection(sentence) > 1:
            particles.append(VerbMoodPartices.DESIRATIVE)

        if deductiveness(sentence) > 2:
            particles.append(VerbMoodPartices.DEDUCTIVE)
        # todo deontic

        if speculativeness(sentence) > 2:
            particles.append(VerbMoodPartices.SPECULATIVE)
        if potentiality(sentence) > 2:
            particles.append(VerbMoodPartices.POTENTIAL)

        return particles
