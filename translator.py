from translate import MultistageKoiTranslationEngine
from sys import argv
from pprint import pprint


default_input = "The sun is setting"
engine = MultistageKoiTranslationEngine()

def translate_koi(input):
    return engine.digest(input)

def main():
    sysargs = argv[1:]
    input = default_input
    if len(sysargs) > 0:
        input = " ".join(sysargs)
    else:
        print(f"[W] Using default input '{default_input}'")

    pprint(translate_koi(input))

if __name__ == "__main__":
    main()
