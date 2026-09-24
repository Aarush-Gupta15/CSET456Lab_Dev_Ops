
from pathlib import Path
from collections import Counter
import json

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

CORPUS_FILE = BASE_DIR / "Lab3" / "Data" / "source_code_corpus.csv"
OUTPUT_DIR = BASE_DIR / "Lab3" / "Output"

STATS_FILE = OUTPUT_DIR / "character_tokenizer_statistics.json"


def tokenize_characters(source_code):
    """
    Convert source code into a sequence of individual characters.
    """
    return list(source_code)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # keep_default_na=False ensures empty files remain empty strings.
    df = pd.read_csv(
        CORPUS_FILE,
        keep_default_na=False
    )

    vocabulary = Counter()
    sequence_lengths = []

    for source_code in df["source_code"]:
        tokens = tokenize_characters(source_code)

        vocabulary.update(tokens)
        sequence_lengths.append(len(tokens))

    vocab_size = len(vocabulary)

    total_files = len(df)

    total_tokens = sum(sequence_lengths)

    average_sequence_length = (
        total_tokens / total_files
        if total_files > 0
        else 0
    )

    statistics = {
        "tokenizer": "character",
        "total_files": total_files,
        "vocabulary_size": vocab_size,
        "total_tokens": total_tokens,
        "average_sequence_length": average_sequence_length,
        "minimum_sequence_length": min(sequence_lengths)
        if sequence_lengths
        else 0,
        "maximum_sequence_length": max(sequence_lengths)
        if sequence_lengths
        else 0,
        "empty_sequences": sum(
            length == 0 for length in sequence_lengths
        ),
    }

    with open(STATS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            statistics,
            file,
            indent=4
        )

    print("===== CHARACTER TOKENIZER =====")
    print(f"Total files: {total_files}")
    print(f"Vocabulary size: {vocab_size}")
    print(f"Total tokens: {total_tokens}")
    print(
        f"Average sequence length: "
        f"{average_sequence_length:.2f}"
    )
    print(
        f"Minimum sequence length: "
        f"{statistics['minimum_sequence_length']}"
    )
    print(
        f"Maximum sequence length: "
        f"{statistics['maximum_sequence_length']}"
    )
    print(
        f"Empty sequences: "
        f"{statistics['empty_sequences']}"
    )

    print(f"\nStatistics saved to:")
    print(STATS_FILE)


if __name__ == "__main__":
    main()