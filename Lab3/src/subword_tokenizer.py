from pathlib import Path
from collections import Counter
import json
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

CORPUS_FILE = BASE_DIR / "Lab3" / "Data" / "source_code_corpus.csv"
OUTPUT_DIR = BASE_DIR / "Lab3" / "Output"

STATS_FILE = OUTPUT_DIR / "subword_tokenizer_statistics.json"

TARGET_VOCAB_SIZE = 10000


TOKEN_PATTERN = re.compile(
    r"[A-Za-z_][A-Za-z0-9_]*"
    r"|\d+(?:\.\d+)?"
    r"|==|!=|<=|>=|->|=>|//|\*\*|<<|>>|&&|\|\|"
    r"|[^\sA-Za-z0-9_]"
)


def initial_tokens(source_code):
    """
    Convert source code into basic tokens before BPE merging.
    """
    return TOKEN_PATTERN.findall(source_code)


def build_character_vocabulary(corpus):
    """
    Build the initial character vocabulary.
    """
    vocabulary = Counter()

    for source_code in corpus:
        vocabulary.update(source_code)

    return vocabulary


def get_pair_counts(word_frequencies):
    """
    Count adjacent symbol pairs.
    """
    pair_counts = Counter()

    for symbols, frequency in word_frequencies.items():
        for index in range(len(symbols) - 1):
            pair = (
                symbols[index],
                symbols[index + 1]
            )

            pair_counts[pair] += frequency

    return pair_counts


def merge_pair(word_frequencies, pair):
    """
    Merge one frequent pair throughout the vocabulary.
    """
    merged_frequencies = {}

    first, second = pair
    merged_symbol = first + second

    for symbols, frequency in word_frequencies.items():
        new_symbols = []
        index = 0

        while index < len(symbols):
            if (
                index < len(symbols) - 1
                and symbols[index] == first
                and symbols[index + 1] == second
            ):
                new_symbols.append(merged_symbol)
                index += 2
            else:
                new_symbols.append(symbols[index])
                index += 1

        new_symbols = tuple(new_symbols)

        merged_frequencies[new_symbols] = (
            merged_frequencies.get(new_symbols, 0)
            + frequency
        )

    return merged_frequencies


def train_bpe(corpus, target_vocab_size):
    """
    Train a simple BPE tokenizer.
    """
    word_frequencies = Counter()

    for source_code in corpus:
        tokens = initial_tokens(source_code)

        for token in tokens:
            symbols = tuple(token)
            word_frequencies[symbols] += 1

    vocabulary = set()

    for symbols in word_frequencies:
        vocabulary.update(symbols)

    merges = []

    while len(vocabulary) < target_vocab_size:
        pair_counts = get_pair_counts(word_frequencies)

        if not pair_counts:
            break

        best_pair, best_frequency = pair_counts.most_common(1)[0]

        if best_frequency < 2:
            break

        word_frequencies = merge_pair(
            word_frequencies,
            best_pair
        )

        merged_symbol = best_pair[0] + best_pair[1]

        vocabulary.add(merged_symbol)
        merges.append(best_pair)

    return vocabulary, merges


def apply_bpe(token, merges):
    """
    Apply learned BPE merges to one token.
    """
    symbols = list(token)

    for first, second in merges:
        merged_symbol = first + second

        new_symbols = []
        index = 0

        while index < len(symbols):
            if (
                index < len(symbols) - 1
                and symbols[index] == first
                and symbols[index + 1] == second
            ):
                new_symbols.append(merged_symbol)
                index += 2
            else:
                new_symbols.append(symbols[index])
                index += 1

        symbols = new_symbols

    return symbols


def tokenize_source(source_code, merges):
    """
    Tokenize source code using the trained BPE merges.
    """
    basic_tokens = initial_tokens(source_code)

    subword_tokens = []

    for token in basic_tokens:
        subword_tokens.extend(
            apply_bpe(token, merges)
        )

    return subword_tokens


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(
        CORPUS_FILE,
        keep_default_na=False
    )

    corpus = df["source_code"].tolist()

    print("===== TRAINING SUBWORD TOKENIZER =====")
    print(f"Target vocabulary size: {TARGET_VOCAB_SIZE}")
    print(f"Corpus files: {len(corpus)}")

    vocabulary, merges = train_bpe(
        corpus,
        TARGET_VOCAB_SIZE
    )

    print(f"Actual vocabulary size: {len(vocabulary)}")
    print(f"BPE merges learned: {len(merges)}")

    sequence_lengths = []
    token_frequency = Counter()

    for source_code in corpus:
        tokens = tokenize_source(
            source_code,
            merges
        )

        sequence_lengths.append(len(tokens))
        token_frequency.update(tokens)

    total_files = len(df)
    total_tokens = sum(sequence_lengths)

    average_sequence_length = (
        total_tokens / total_files
        if total_files > 0
        else 0
    )

    statistics = {
        "tokenizer": "subword_bpe",
        "target_vocabulary_size": TARGET_VOCAB_SIZE,
        "vocabulary_size": len(vocabulary),
        "bpe_merges": len(merges),
        "total_files": total_files,
        "total_tokens": total_tokens,
        "average_sequence_length": average_sequence_length,
        "minimum_sequence_length": min(sequence_lengths)
        if sequence_lengths
        else 0,
        "maximum_sequence_length": max(sequence_lengths)
        if sequence_lengths
        else 0,
        "empty_sequences": sum(
            length == 0
            for length in sequence_lengths
        ),
    }

    with open(
        STATS_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            statistics,
            file,
            indent=4
        )

    print("\n===== SUBWORD TOKENIZER RESULTS =====")
    print(f"Vocabulary size: {len(vocabulary)}")
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

    print("\nTop 10 most frequent subword tokens:")

    for token, frequency in token_frequency.most_common(10):
        print(repr(token), "->", frequency)

    print("\nStatistics saved to:")
    print(STATS_FILE)


if __name__ == "__main__":
    main()