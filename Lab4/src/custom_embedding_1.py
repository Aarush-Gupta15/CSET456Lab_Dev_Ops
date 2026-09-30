import re
import math
import random
import csv
import sys
from collections import Counter, defaultdict


csv.field_size_limit(sys.maxsize)


CORPUS_FILE = "Lab3/Data/source_code_corpus.csv"
OUTPUT_EMBEDDINGS = "Lab4/Data/custom_embedding_1.csv"
OUTPUT_RESULTS = "Lab4/Data/custom_embedding_1_similarity.csv"

WINDOW_SIZE = 2
MAX_VOCAB_SIZE = 500


def tokenize_source_code(source_code):
    """Convert source code into simple tokens."""
    return re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|"
        r"\d+|"
        r"==|!=|<=|>=|->|"
        r"[^\sA-Za-z0-9_]",
        source_code
    )


def load_corpus():
    """Load source code from the Lab 3 corpus."""
    documents = []

    with open(CORPUS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            source_code = row["source_code"]

            if not source_code or not source_code.strip():
                continue

            tokens = tokenize_source_code(source_code)

            if tokens:
                documents.append(tokens)

    return documents


def build_vocabulary(documents):
    """Build vocabulary from token frequencies."""
    frequency = Counter()

    for tokens in documents:
        frequency.update(tokens)

    most_common = frequency.most_common(MAX_VOCAB_SIZE)

    return [token for token, _ in most_common]


def build_cooccurrence_matrix(documents, vocabulary):
    """Create token-context co-occurrence counts."""
    vocabulary_set = set(vocabulary)
    matrix = defaultdict(Counter)

    for tokens in documents:
        for index, token in enumerate(tokens):

            if token not in vocabulary_set:
                continue

            start = max(0, index - WINDOW_SIZE)
            end = min(len(tokens), index + WINDOW_SIZE + 1)

            for context_index in range(start, end):

                if context_index == index:
                    continue

                context_token = tokens[context_index]

                if context_token in vocabulary_set:
                    matrix[token][context_token] += 1

    return matrix


def cosine_similarity(vector_a, vector_b):
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def convert_to_vectors(matrix, vocabulary):
    """Convert sparse co-occurrence counts into dense vectors."""
    vectors = {}

    for token in vocabulary:
        vector = []

        for context_token in vocabulary:
            vector.append(matrix[token][context_token])

        vectors[token] = vector

    return vectors


def select_tokens(vocabulary):
    """Select 20 tokens using a fixed random seed."""
    random.seed(42)

    candidates = [
        token for token in vocabulary
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", token)
    ]

    selected = random.sample(candidates, min(20, len(candidates)))

    return selected


def calculate_pairwise_similarity(tokens, vectors):
    """Calculate pairwise cosine similarity."""
    results = []

    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens)):

            token_a = tokens[i]
            token_b = tokens[j]

            similarity = cosine_similarity(
                vectors[token_a],
                vectors[token_b]
            )

            results.append(
                (token_a, token_b, similarity)
            )

    results.sort(key=lambda x: x[2], reverse=True)

    return results


def save_embeddings(tokens, vectors):
    """Save selected token embeddings."""
    with open(
        OUTPUT_EMBEDDINGS,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["token"] + [
                f"context_{i}"
                for i in range(len(vectors[tokens[0]]))
            ]
        )

        for token in tokens:
            writer.writerow(
                [token] + vectors[token]
            )


def save_similarity_results(results):
    """Save pairwise similarity results."""
    with open(
        OUTPUT_RESULTS,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            ["token_1", "token_2", "cosine_similarity"]
        )

        for token_a, token_b, similarity in results:
            writer.writerow(
                [token_a, token_b, f"{similarity:.6f}"]
            )


def main():

    print("===== CUSTOM EMBEDDING APPROACH 1 =====")

    print("\n[1] Loading Lab 3 corpus...")
    documents = load_corpus()

    print(f"Documents loaded: {len(documents)}")

    print("\n[2] Building vocabulary...")
    vocabulary = build_vocabulary(documents)

    print(f"Vocabulary size: {len(vocabulary)}")

    print("\n[3] Building co-occurrence matrix...")
    matrix = build_cooccurrence_matrix(
        documents,
        vocabulary
    )

    print("Co-occurrence matrix created.")

    print("\n[4] Creating embeddings...")
    vectors = convert_to_vectors(
        matrix,
        vocabulary
    )

    print(
        f"Embedding dimension: {len(vocabulary)}"
    )

    print("\n[5] Selecting 20 tokens...")
    selected_tokens = select_tokens(vocabulary)

    print("\nSelected tokens:")

    for number, token in enumerate(
        selected_tokens,
        start=1
    ):
        print(f"{number:2}. {token}")

    print("\n[6] Calculating pairwise cosine similarity...")

    results = calculate_pairwise_similarity(
        selected_tokens,
        vectors
    )

    print("\n===== TOP 5 MOST SIMILAR PAIRS =====")

    for rank, (
        token_a,
        token_b,
        similarity
    ) in enumerate(results[:5], start=1):

        print(
            f"{rank}. "
            f"{token_a} <-> {token_b} "
            f"= {similarity:.6f}"
        )

    print("\n[7] Saving embeddings...")
    save_embeddings(
        selected_tokens,
        vectors
    )

    print("Saved:", OUTPUT_EMBEDDINGS)

    print("\n[8] Saving similarity results...")
    save_similarity_results(results)

    print("Saved:", OUTPUT_RESULTS)

    print("\n===== EXPERIMENT COMPLETED =====")


if __name__ == "__main__":
    main()