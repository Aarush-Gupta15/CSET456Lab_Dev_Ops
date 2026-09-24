# Lab 3 – Source Code Tokenization and Vocabulary Analysis

## Objective

The objective of Lab 3 is to prepare the source-code dataset generated in Lab 2 for AI/ML processing by applying different tokenization techniques.

The lab covers:

1. Source-code corpus preparation
2. Character-level tokenization
3. Word-level tokenization
4. Subword tokenization using a simple Byte Pair Encoding (BPE) approach
5. Vocabulary-size analysis
6. Token-frequency analysis
7. Comparison of tokenization strategies

---

## Repositories Used

The source-code corpus was prepared from the five repositories used in Lab 2:

* Flask
* Requests
* Pytest
* FastAPI
* Scikit-learn

The Lab 3 corpus is generated directly from the verified Lab 2 source-code dataset.

---

## Dataset Preparation

The Lab 2 source-code dataset contains **2,623 source files**.

The dataset was verified against the working repositories before creating the Lab 3 corpus.

### Verification Results

```text
Dataset records: 2623
Missing files: 0

SUCCESS: All dataset files exist in the working repositories.
```

The Lab 3 corpus was then generated at:

```text
Lab3/Data/source_code_corpus.csv
```

### Corpus Statistics

| Repository   |    Files |
| ------------ | -------: |
| FastAPI      |     1147 |
| Flask        |       84 |
| Pytest       |      274 |
| Requests     |       37 |
| Scikit-learn |     1081 |
| **Total**    | **2623** |

### Languages

| Language   |    Files |
| ---------- | -------: |
| Python     |     2568 |
| Shell      |       29 |
| JavaScript |       11 |
| C/C++      |        7 |
| C++        |        5 |
| C          |        3 |
| **Total**  | **2623** |

There are **253 empty source-code records**. These are primarily empty `__init__.py` files and are retained because the corpus preserves the complete Lab 2 dataset.

---

# 1. Corpus Preparation

### Script

```text
Lab3/src/prepare_corpus.py
```

### Input

```text
Lab2/Output/source_code_dataset.csv
```

### Output

```text
Lab3/Data/source_code_corpus.csv
```

The corpus contains the following columns:

```text
repository
file_path
language
extension
is_test_file
source_code
```

### Verification

```text
Lab 2 records: 2623
Corpus records written: 2623
Missing files: 0
```

The repository counts between Lab 2 and Lab 3 were also verified to match.

---

# 2. Character-Level Tokenization

Character-level tokenization treats every character in the source code as a token.

For example:

```python
print("Hello")
```

can be represented as a sequence of individual characters.

### Script

```text
Lab3/src/character_tokenizer.py
```

### Output

```text
Lab3/Output/character_tokenizer_statistics.json
```

### Verified Results

```text
Total files: 2623
Vocabulary size: 296
Total tokens: 25000932
Average sequence length: 9531.43
Minimum sequence length: 0
Maximum sequence length: 394863
Empty sequences: 253
```

### Observation

Character-level tokenization produces a relatively small vocabulary but very long sequences.

This can make character-level representations useful for capturing fine-grained source-code patterns, but processing long sequences can require more computational resources.

---

# 3. Word-Level Tokenization

Word-level tokenization separates source code into larger lexical units such as identifiers, keywords, numbers, and symbols.

For example:

```python
total_count = 10
```

can be separated into tokens such as:

```text
total_count
=
10
```

### Script

```text
Lab3/src/word_tokenizer.py
```

### Output

```text
Lab3/Output/word_tokenizer_statistics.json
```

### Verified Results

```text
Total files: 2623
Vocabulary size: 72246
Total tokens: 5171379
Average sequence length: 1971.55
Minimum sequence length: 0
Maximum sequence length: 41770
Empty sequences: 253
```

### Observation

Word-level tokenization significantly reduces the total number of tokens compared with character-level tokenization.

However, the vocabulary is much larger because source code contains many unique identifiers, names, paths, and other lexical elements.

---

# 4. Subword Tokenization

The Lab 3 subword tokenizer implements a simplified Byte Pair Encoding (BPE) approach.

### Script

```text
Lab3/src/subword_tokenizer.py
```

The implementation:

1. Performs initial lexical tokenization.
2. Represents tokens as character sequences.
3. Counts frequently occurring adjacent symbol pairs.
4. Merges the most frequent pair.
5. Repeats the process until the target vocabulary size is reached or no useful merge remains.
6. Applies the learned merges to the source-code corpus.

### Target Vocabulary

```text
10000
```

The resulting statistics are saved to:

```text
Lab3/Output/subword_tokenizer_statistics.json
```

---

# 5. Token Frequency Analysis

The lab also includes token-frequency analysis.

The top token results are stored in:

```text
Lab3/Data/top_50_tokens.csv
```

This file contains the most frequently occurring tokens identified during the tokenization analysis.

Token-frequency analysis helps identify commonly occurring programming-language constructs and source-code patterns.

---

# 6. Tokenization Comparison

| Property                    | Character                   | Word                          | Subword                                        |
| --------------------------- | --------------------------- | ----------------------------- | ---------------------------------------------- |
| Basic unit                  | Character                   | Lexical token                 | Subword                                        |
| Vocabulary                  | Small                       | Large                         | Controlled                                     |
| Sequence length             | Very high                   | Lower                         | Intermediate                                   |
| Handles unknown identifiers | Naturally                   | Can create many unique tokens | Can split identifiers                          |
| Main advantage              | Fine-grained representation | Simple and interpretable      | Balance between vocabulary and sequence length |

The actual numerical results for character-level and word-level tokenization are stored in the corresponding JSON files.

---

# 7. Directory Structure

```text
Lab3/
│
├── Data/
│   ├── source_code_corpus.csv
│   └── top_50_tokens.csv
│
├── Output/
│   ├── character_tokenizer_statistics.json
│   ├── word_tokenizer_statistics.json
│   └── subword_tokenizer_statistics.json
│
├── Output/
│   └── screenshots/
│
└── src/
    ├── prepare_corpus.py
    ├── character_tokenizer.py
    ├── word_tokenizer.py
    └── subword_tokenizer.py
```

---

# 8. Execution

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run corpus preparation:

```bash
python Lab3/src/prepare_corpus.py
```

Run character tokenizer:

```bash
python Lab3/src/character_tokenizer.py
```

Run word tokenizer:

```bash
python Lab3/src/word_tokenizer.py
```

Run subword tokenizer:

```bash
python Lab3/src/subword_tokenizer.py
```

---

# 9. Final Verified Lab 3 Results

The Lab 3 corpus contains:

```text
2623 source files
5 repositories
2568 Python files
29 Shell files
11 JavaScript files
7 C/C++ files
5 C++ files
3 C files
```

Character tokenizer:

```text
Vocabulary: 296
Tokens: 25,000,932
Average sequence length: 9,531.43
```

Word tokenizer:

```text
Vocabulary: 72,246
Tokens: 5,171,379
Average sequence length: 1,971.55
```

Empty source-code records:

```text
253
```

All **2,623 corpus file paths were verified against the Lab 2 working repositories**, with:

```text
Missing files: 0
```

---

## Conclusion

Lab 3 transforms the source-code dataset produced in Lab 2 into a corpus suitable for tokenization and later AI/ML processing.

The experiments demonstrate the trade-off between vocabulary size and sequence length:

* Character tokenization produces a small vocabulary but very long sequences.
* Word tokenization produces a much larger vocabulary but shorter sequences.
* Subword tokenization attempts to balance these two properties by learning frequently occurring symbol combinations.

These representations can be used as a foundation for later source-code embeddings, similarity analysis, and machine-learning experiments.

