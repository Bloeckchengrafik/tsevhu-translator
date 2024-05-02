from translate.log import tx_info

tx_info("Loading SentenceTransformer model...")
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

dimensions = 512

model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=dimensions)


def queryify(source: str):
    return f"Represent this sentence for searching relevant passages: {source}"


def similarities(source: str, targets: list[str]):
    embeddings = model.encode([queryify(source)] + targets)
    return cos_sim(embeddings[0], embeddings[1:])


def most_similar(source: str, targets: list[str], target_data: list = None):
    sims = similarities(source, targets)
    sims = sims.tolist()[0]
    if target_data:
        return target_data[sims.index(max(sims))]
    return targets[sims.index(max(sims))]


def affection(term: str) -> int:
    """
    Affection rating from -3 to 3
    """
    targets = ["truly love", "love", "affectionate", "be", "unaffectionate", "hate", "truly hate"]
    scale = [3, 2, 1, 0, -1, -2, -3]
    return most_similar(term, targets, scale)


def hypotheticalness(term: str) -> int:
    """
    Hypotheticalness rating from 0 to 3
    """
    targets = ["hypothetical", "possible", "probable", "certain"]
    return most_similar(term, targets, [3, 2, 1, 0])


def consequentialness(term: str) -> int:
    """
    Consequentialness rating from 0 to 3
    """
    targets = ["consequential", "important", "significant", "trivial"]
    return most_similar(term, targets, [3, 2, 1, 0])


def willingness(term: str) -> int:
    """
    Willingness rating from -3 to 3
    """
    targets = ["eager", "willing", "neutral", "unwilling", "reluctant"]
    scale = [3, 2, 0, -2, -3]
    return most_similar(term, targets, scale)


def habitualness(term: str) -> int:
    """
    Habitualness rating from 0 to 3
    """
    return most_similar(term, ["habitual", "often", "sometimes", "rarely"], [3, 2, 1, 0])


def deductiveness(term: str) -> int:
    """
    Deductiveness rating from 0 to 3
    """
    return most_similar(term, ["deductive", "logical", "neutral", "illogical"], [3, 2, 1, 0])


def speculativeness(term: str) -> int:
    """
    Speculativeness rating from 0 to 3
    """
    return most_similar(term, ["speculative", "possible", "neutral", "impossible"], [3, 2, 1, 0])


def desirability(term: str) -> int:
    """
    Desirability rating from -3 (necessative) to 3 (desirable)
    """
    return most_similar(term, ["desirable", "good", "neutral", "undesirable", "necessary"], [3, 2, 0, -2, -3])


def potentiality(term: str) -> int:
    """
    Potentiality rating from 0 to 3
    """
    return most_similar(term, ["maybe", "maybe possible", "neutral", "impossible"], [3, 2, 1, 0])


def subject_active(term: str) -> bool:
    """
    Returns True if the subject is active
    """
    return most_similar(term, ["active", "passive"]) == "active"


if __name__ == '__main__':
    source = "shark"
    targets = ["evil", "nice"]
    print(most_similar(source, targets))  # evil :)
    # this is too cartoony
