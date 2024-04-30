from translate import MultistageKoiTranslationEngine
from sys import argv
from pprint import pprint

default_input = "I'm walking"
engine = MultistageKoiTranslationEngine()


def translate_koi(value):
    return engine.digest(value)


def main():
    sys_args = argv[1:]
    value = default_input
    if len(sys_args) > 0:
        value = " ".join(sys_args)
    else:
        print(f"[W] Using default input '{default_input}'")

    pprint(translate_koi(value))


if __name__ == "__main__":
    main()
