print("[I] Loading SentenceTransformer model...")
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


if __name__ == '__main__':
    source = "shark"
    targets = ["evil", "nice"]
    print(most_similar(source, targets))  # evil :)
    # this is too cartoony
