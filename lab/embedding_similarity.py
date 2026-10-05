"""Run: python -m lab.embedding_similarity"""
from lab.common import load_model


def main():
    sentences = [
        "A firewall blocks unauthorized network traffic.",
        "A network security device filters unwanted connections.",
        "A banana is a yellow fruit.",
    ]
    model = load_model()
    vectors = model.encode(sentences, normalize_embeddings=True)
    print(f"Embedding shape: {vectors.shape} (texts, dimensions)")
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            print(f"{i + 1} vs {j + 1}: cosine={vectors[i] @ vectors[j]:.4f}")
    for i, sentence in enumerate(sentences, 1):
        print(f"{i}: {sentence}")
    print("Similarity is not a probability or a guarantee of truth.")


if __name__ == "__main__":
    main()
