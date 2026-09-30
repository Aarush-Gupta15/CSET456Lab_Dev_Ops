"""TF-IDF weighted token-context profiles; standard library only."""
import csv
import math
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from custom_embedding_1 import (CORPUS_FILE, MAX_VOCAB_SIZE, WINDOW_SIZE,
                                build_vocabulary, cosine_similarity,
                                load_corpus, select_tokens,
                                build_cooccurrence_matrix)

OUT = Path("Lab4/Data")

def main():
    print("===== CUSTOM EMBEDDING APPROACH 2: TF-IDF CONTEXT =====")
    docs = load_corpus()
    vocab = build_vocabulary(docs)
    print(f"Corpus: {CORPUS_FILE}; non-empty tokenized records: {len(docs)}")
    print(f"Vocabulary cap: {MAX_VOCAB_SIZE}; context window: {WINDOW_SIZE}; seed: 42")
    counts = build_cooccurrence_matrix(docs, vocab)
    df = Counter()
    # A context's IDF is based on the number of source files containing it.
    for tokens in docs:
        df.update(set(tokens) & set(vocab))
    n_docs = len(docs)
    idf = {c: math.log((1 + n_docs) / (1 + df[c])) + 1.0 for c in vocab}
    vectors = {t: [counts[t][c] * idf[c] for c in vocab] for t in vocab}
    selected = select_tokens(vocab)
    pairs = []
    for i, a in enumerate(selected):
        for b in selected[i+1:]:
            pairs.append((a, b, cosine_similarity(vectors[a], vectors[b])))
    pairs.sort(key=lambda x: x[2], reverse=True)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "custom_embedding_2.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["token"] + [f"context_{c}" for c in vocab])
        for t in selected: w.writerow([t] + vectors[t])
    with (OUT / "custom_embedding_2_similarity.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["token_1", "token_2", "cosine_similarity"])
        w.writerows((a, b, f"{s:.6f}") for a,b,s in pairs)
    print("Selected tokens:", ", ".join(selected))
    print("Embedding: raw co-occurrence counts multiplied by context IDF; dimension:", len(vocab))
    print("Top 5 pairs:")
    for rank, (a,b,s) in enumerate(pairs[:5], 1): print(f"{rank}. {a} <-> {b} = {s:.6f}")
    print("Saved Lab4/Data/custom_embedding_2.csv and custom_embedding_2_similarity.csv")

if __name__ == "__main__": main()
