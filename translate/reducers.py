from pprint import pprint
from translate.context import UnknownContextWord
from translate.verbs import determine_tense_and_affixes
from translate.verbs.context import Verb


class ContextReducer:
    def _begin_reduce(self, tagged: list[tuple[str, str]]):
        return [UnknownContextWord(wrd, clue) for wrd, clue in tagged]

    def _reduce_and_lint_verbs(self, context: list[UnknownContextWord]):
        if len(context) == 0:
            return []

        outs = [context[0]]

        prev = context[0]
        prev_particle = False
        for word in context[1:]:
            out = word
            if prev.is_verb() and word.is_verb():
                verb = word.value
                if prev_particle:
                    tense, affix = determine_tense_and_affixes([prev.value, "to", verb])
                    outs = outs[:-2]
                else:
                    tense, affix = determine_tense_and_affixes([prev.value, verb])
                # outs = outs[:-2]
                out = Verb(verb, tense, affix)
            elif word.is_verb():
                tense, affix = determine_tense_and_affixes([word.value])
                out = Verb(word.value, tense, affix)

            if word.is_particle() and not prev_particle:
                prev_particle = True
            else:
                prev = word
                prev_particle = False

            outs.append(out)

        return outs

    def try_translate_verbs(self, context: list[UnknownContextWord | Verb]):
        for i, word in enumerate(context):
            if isinstance(word, Verb):
                word.value = word.value.removesuffix("ed")
                word.value = word.value.removesuffix("ing")
                context[i] = word.translate()

        return context

    def __call__(self, tagged: list[tuple[str, str]]):
        reducer_ctx = self._begin_reduce(tagged)

        print("=== Context Reducer ===")
        pprint(reducer_ctx)

        print("=== Verb Linting ===")
        reducer_ctx = self._reduce_and_lint_verbs(reducer_ctx)
        pprint(reducer_ctx)

        print("=== Verb Translation ===")
        reducer_ctx = self.try_translate_verbs(reducer_ctx)
        pprint(reducer_ctx)

        return reducer_ctx
