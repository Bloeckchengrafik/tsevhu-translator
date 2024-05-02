from translate.context.compile import Compileable


def compile_sentence(full: str, context: list):
    punct = full[-1] if full[-1] in [".", "!", "?"] else "."
    words = []
    for word in context:
        if isinstance(word, Compileable):
            words.append(word.compile(punct))
        else:
            words.append(str(word))

    return " ".join(words) + punct
