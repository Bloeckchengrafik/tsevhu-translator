from dataclasses import dataclass


@dataclass
class UnknownContextWord:
    value: str
    nlp_tag: str

    def is_verb(self):
        return self.nlp_tag == "VERB"

    def is_particle(self):
        return self.nlp_tag == "PRT"

    def __str__(self):
        return f"<?:{self.value}>"
