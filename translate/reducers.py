from pprint import pprint
from translate.context import UnknownContextWord
from translate.context.compile import Compileable
from translate.verbs import determine_tense_and_affixes
from translate.verbs.context import Verb
from translate.vocabulary.embedding_utils import subject_active


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
                    outs = outs[:-1]
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

    def _try_translate_verbs(self, sentence: str, context: list[UnknownContextWord | Verb], subject_is_active: bool):
        for i, word in enumerate(context):
            if isinstance(word, Verb):
                word.value = word.value.removesuffix("ed")
                word.value = word.value.removesuffix("ing")
                # setting -> sett -> set
                if len(word.value) > 2 and word.value[-1] == word.value[-2]:
                    word.value = word.value[:-1]
                context[i] = word.translate(sentence, subject_is_active)

        return context

    def _compile_sentence(self, full: str, context: list):
        punct = full[-1] if full[-1] in [".", "!", "?"] else "."
        words = []
        for word in context:
            if isinstance(word, Compileable):
                words.append(word.compile(punct))
            else:
                words.append(str(word))

        return " ".join(words) + punct

    def __call__(self, tagged: list[tuple[str, str]], full):
        reducer_ctx = self._begin_reduce(tagged)

        print("=== Context Reducer ===")
        pprint(reducer_ctx)
        subject_is_active = subject_active(full)

        print("=== Verb Linting ===")
        reducer_ctx = self._reduce_and_lint_verbs(reducer_ctx)
        pprint(reducer_ctx)

        print("=== Verb Translation ===")
        reducer_ctx = self._try_translate_verbs(full, reducer_ctx, subject_is_active)
        pprint(reducer_ctx)

        print("=== Sentence Compilation ===")
        compiled = self._compile_sentence(full, reducer_ctx)

        return compiled
