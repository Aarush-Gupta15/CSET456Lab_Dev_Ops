from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

LAB2_DATASET = BASE_DIR / "Lab2" / "Output" / "source_code_dataset.csv"
WORKING_DIR = BASE_DIR / "Lab2" / "working"

OUTPUT_DIR = BASE_DIR / "Lab3" / "Data"
OUTPUT_FILE = OUTPUT_DIR / "source_code_corpus.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Read the authoritative Lab 2 source-code dataset.
    df = pd.read_csv(LAB2_DATASET)

    corpus_records = []
    missing_files = []

    for _, row in df.iterrows():
        repository = row["repository"]
        file_path = row["file_path"]

        source_path = WORKING_DIR / repository / file_path

        if not source_path.is_file():
            missing_files.append((repository, file_path))
            continue

        try:
            source_code = source_path.read_text(
                encoding="utf-8",
                errors="replace"
            )

        except OSError as error:
            print(f"Could not read {source_path}: {error}")
            continue

        # Keep empty files as an empty string.
        # This allows tokenizers to correctly produce 0 tokens.
        if not source_code:
            source_code = ""

        corpus_records.append(
            {
                "repository": repository,
                "file_path": file_path,
                "language": row["language"],
                "extension": row["extension"],
                "is_test_file": row["is_test_file"],
                "source_code": source_code,
            }
        )

    corpus_df = pd.DataFrame(corpus_records)

    # Save the complete source-code corpus.
    corpus_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("===== CORPUS PREPARATION COMPLETE =====")
    print(f"Lab 2 dataset records: {len(df)}")
    print(f"Corpus records written: {len(corpus_df)}")
    print(f"Missing files: {len(missing_files)}")
    print(f"Output file: {OUTPUT_FILE}")

    if missing_files:
        print("\nFirst 20 missing files:")

        for repository, file_path in missing_files[:20]:
            print(f"{repository}: {file_path}")

    print("\nRecords by repository:")
    print(
        corpus_df["repository"]
        .value_counts()
        .sort_index()
    )

    print("\nRecords by language:")
    print(
        corpus_df["language"]
        .value_counts()
    )

    print("\nEmpty source-code records:")

    empty_count = (
        corpus_df["source_code"]
        .fillna("")
        .eq("")
        .sum()
    )

    print(empty_count)


if __name__ == "__main__":
    main()