# CSET456 DevOps Lab 4 — Source Code Embeddings

## 1. Introduction

This lab focuses on generating and analyzing embeddings for source-code tokens.

The tokenization foundation developed in **Lab 3** is used as the starting point for this lab. The objective is to understand how different embedding approaches represent source-code tokens and how well these representations capture relationships between tokens.

The lab also includes implementation and analysis of **Word2Vec** and **Code2Vec**.

---

## 2. Objectives

The main objectives of Lab 4 are:

1. Develop at least two embedding approaches independently.
2. Select 20 tokens manually and randomly.
3. Generate embeddings for the selected tokens.
4. Calculate pairwise cosine similarity between token embeddings.
5. Identify the five most similar token pairs.
6. Analyze whether the similarities make sense.
7. Identify at least two cases where the embedding representation fails.
8. Implement Word2Vec.
9. Implement Code2Vec.
10. Compare Word2Vec with the custom embedding approaches.
11. Document the thought process and observations for each embedding approach.

---

## 3. Dataset

The source-code dataset prepared during Lab 3 will be used as the foundation for this experiment.

The dataset contains source code mined from the following repositories:

- Flask
- Requests
- Pytest
- FastAPI
- Scikit-learn

The Lab 3 corpus contains **2,623 source-code records**.

The main source-code languages present in the corpus include:

- Python
- Shell
- JavaScript
- C
- C++
- C/C++

The embedding experiments will use tokens extracted from this source-code corpus.

---

## 4. Lab 4 Directory Structure

```text
Lab4/
│
├── README.md
│
├── src/
│   ├── ...
│
├── Data/
│   ├── ...
│
└── Output/
    └── screenshots/
        ├── ...
```

Source, generated CSVs, and experiment logs are stored in the directories above.

---

# 5. Experiment 1 — Custom Embedding Approach 1

## 5.1 Approach

The first embedding approach is a custom token co-occurrence baseline.

### Thought Process

The approach is a raw token co-occurrence matrix. Each token is represented by its counts of neighboring tokens within a two-token window. I chose this transparent baseline so each vector dimension has a direct meaning (one context token); it can reveal usage patterns but does not encode syntax trees or learn compressed latent features.

## 5.2 Token Selection

Twenty identifier-like tokens were sampled reproducibly from the corpus vocabulary with seed 42 and then manually inspected for interpretation.

| No. | Token |
| --: | ----- |
| 1 | `coef` |
| 2 | `on` |
| 3 | `if` |
| 4 | `integer` |
| 5 | `score` |
| 6 | `samples` |
| 7 | `py` |
| 8 | `title` |
| 9 | `id` |
| 10 | `x` |
| 11 | `zeros` |
| 12 | `given` |
| 13 | `are` |
| 14 | `global_random_seed` |
| 15 | `__init__` |
| 16 | `and` |
| 17 | `from` |
| 18 | `random_state` |
| 19 | `should` |
| 20 | `each` |

## 5.3 Embedding Generation

The implementation (`src/custom_embedding_1.py`) produces dense 500-dimensional count vectors for the 20 tokens. It read 2,370 non-empty records from `Lab3/Data/source_code_corpus.csv`; output is `Data/custom_embedding_1.csv`.

## 5.4 Cosine Similarity

Cosine similarity was calculated for all 190 unique pairs and saved to `Data/custom_embedding_1_similarity.csv`.

## 5.5 Five Most Similar Pairs

The five most similar token pairs will be reported after the experiment.

| Rank | Token 1 | Token 2 | Cosine Similarity |
| ---: | ------- | ------- | ----------------: |
| 1 | `integer` | `title` | 0.880550 |
| 2 | `integer` | `id` | 0.879432 |
| 3 | `title` | `id` | 0.861403 |
| 4 | `on` | `given` | 0.842114 |
| 5 | `score` | `x` | 0.817272 |

## 5.6 Analysis

`on`/`given` and `score`/`x` plausibly share some local usage patterns, though the model has no semantic labels. The leading `integer`/`title` and `integer`/`id` pairs are false semantic matches: their names imply different roles, but the count vectors overlap on nearby context tokens. The score is evidence of shared local context only.

## 5.7 Representation Failures

At least two failure cases will be identified.

| Case | Tokens | Observation |
| ---- | ------ | ----------- |
| 1 | `integer` / `title` | Similarity 0.880550 comes from overlapping neighboring-token counts; a numeric value and display label are not interchangeable. |
| 2 | `integer` / `id` | Similarity 0.879432 shows the fixed window cannot distinguish an integer role from an identifier role when nearby token patterns overlap. |

---

# 6. Experiment 2 — Custom Embedding Approach 2

## 6.1 Approach

A second, distinct custom approach is implemented in `src/custom_embedding_2.py`.

### Thought Process

It starts with the same two-token co-occurrence counts, then multiplies each context column by smoothed inverse document frequency: `idf(c) = log((1 + N) / (1 + df(c))) + 1`, where `df(c)` counts corpus records containing context token `c`. This down-weights contexts present in many files. I chose this weighting to test whether rarer, more discriminative contexts improve pairwise separation. Unlike Approach 1, vector dimensions are weighted counts; it remains a hand-built context model and does not learn latent dimensions.

## 6.2 Token Selection

The experiment will use 20 selected tokens.

The same seed-42 sample as Approach 1 is used for a direct comparison: `coef`, `on`, `if`, `integer`, `score`, `samples`, `py`, `title`, `id`, `x`, `zeros`, `given`, `are`, `global_random_seed`, `__init__`, `and`, `from`, `random_state`, `should`, `each`. Vocabulary size is capped at 500; context window is 2; input is the 2,370 non-empty Lab 3 records.

## 6.3 Embedding Generation

Each selected token gets a dense 500-dimensional TF-IDF-weighted context vector in `Data/custom_embedding_2.csv`.

## 6.4 Cosine Similarity

All 190 pairwise cosine similarities are saved to `Data/custom_embedding_2_similarity.csv`.

## 6.5 Five Most Similar Pairs

| Rank | Token 1 | Token 2 | Cosine Similarity |
| ---: | ------- | ------- | ----------------: |
| 1 | `title` | `id` | 0.830668 |
| 2 | `integer` | `id` | 0.818635 |
| 3 | `integer` | `title` | 0.794328 |
| 4 | `on` | `given` | 0.788930 |
| 5 | `if` | `score` | 0.687649 |

## 6.6 Analysis

The leading `title`/`id` and `on`/`given` pairs retain local-context overlap after weighting. Compared with raw counts, `integer`/`title` falls from 0.880550 to 0.794328, while `title`/`id` falls from 0.861403 to 0.830668. This indicates IDF weighting changed the geometry, but it did not remove ambiguous contexts.

## 6.7 Representation Failures

At least two failure cases will be documented.

| Case | Tokens | Observation |
| ---- | ------ | ----------- |
| 1 | `integer` / `title` | Still scores 0.794328 despite distinct identifier roles; rare-context weighting cannot infer semantic types. |
| 2 | `if` / `score` | Similarity 0.687649 is an implausible semantic match; shared nearby syntax and identifier contexts contribute even after common context columns are down-weighted. |

---

# 7. Experiment 3 — Word2Vec

Word2Vec uses a skip-gram objective to learn distributed representations of source-code tokens based on surrounding context.

The implementation will include:

1. Preparing tokenized source-code sequences.
2. Training the Word2Vec model.
3. Generating embeddings for selected tokens.
4. Calculating similarities between tokens.
5. Identifying related tokens.
6. Analyzing the learned representations.

## 7.1 Word2Vec Configuration

The implementation is an educational NumPy skip-gram with negative sampling. Gensim was absent from the existing Python 3.14 virtual environment, so this dependency-free implementation makes the training objective explicit.

| Parameter       | Value |
| --------------- | ----- |
| Vector size | 50 |
| Window | 5 tokens |
| Minimum count | 2 |
| Training epochs | 1 |
| Records | 300 reproducibly sampled from 2,370 non-empty records |
| Tokens per record | first 120; seed 42 |
| Vocabulary | 1,662 after min-count filtering (10,000 cap) |
| Training pairs | 295,190; 3 negative samples; one worker |

## 7.2 Results

`src/word2vec_embedding.py` writes selected 50-dimensional vectors to `Data/word2vec_embeddings.csv`, all 190 pair similarities to `Data/word2vec_similarity.csv`, and the full 1,662-token input/output parameter matrices to `Data/word2vec_model.csv`. Seed 42 selected `has_app_context`, `model_name`, `item_id`, `targets`, `called`, `low`, `abstractmethod`, `reason`, `successful`, `ignore`, `needed`, `tag`, `_LIBSVM_H`, `order`, `confidence`, `plt`, `param`, `that`, `itertools`, `RegressorMixin`.

## 7.3 Observations

Top pairs were `reason`/`order` (0.986384), `model_name`/`item_id` (0.979879), `abstractmethod`/`itertools` (0.965070), `has_app_context`/`abstractmethod` (0.962709), and `low`/`reason` (0.961534). The very high scores, including the questionable `abstractmethod`/`itertools` pair, show that one sampled pass over a small corpus can produce noisy neighborhoods. These are dense learned vectors, unlike the 500 named context dimensions of the custom models. The bounded sample and one epoch limit coverage and training; results are not a quality ranking.

---

# 8. Experiment 4 — Code2Vec

`src/code2vec_embedding.py` is a practical educational implementation inspired by Code2Vec. It uses Python's `ast` module to count identifier occurrences by their last six AST ancestor/node types and compares those path-feature vectors. It does not reproduce Code2Vec's neural attention architecture or learned code vectors.

Only Python records from the Lab 3 corpus are parsed; non-Python and blank records are skipped. Syntax and AST errors are caught per file. Of 2,623 corpus rows, the run parsed 2,315 Python files, skipped 55 non-Python records and 253 blanks, and encountered 0 parse failures. Identifier vectors count path signatures; the selected 20 identifier names are chosen with seed 42. The union of their path dimensions was 60.

## 8.1 Results

Outputs are `Data/code2vec_embeddings.csv` and `Data/code2vec_similarity.csv`. The five leading pairs were `test_reconstruct_patches_perfect`/`test_mds_recovers_true_data` (1.000000), `test_reconstruct_patches_perfect`/`test_should_do_markup_FORCE_COLOR` (1.000000), `test_mds_recovers_true_data`/`test_should_do_markup_FORCE_COLOR` (1.000000), `_validate_multiclass_probabilistic_prediction`/`_get_transformer_list` (0.707107), and `broken_dep`/`test_reconstruct_patches_perfect` (0.707107).

## 8.2 Observations

The identical test-name similarities are a concrete failure: this implementation represents identifier roles with short ancestor-path counts, so unrelated test identifiers with repeated AST shapes can have identical vectors. It also ignores terminal values and relationships between paired leaves, handles Python only, and has no learned parameters. Its structural features differ from token windows, but this simplified representation should not be mistaken for the original Code2Vec model.

---

# 9. Comparison of Embedding Approaches

The custom embeddings are compared with Word2Vec and Code2Vec below.

| Feature              | Custom Approach 1 | Custom Approach 2 | Word2Vec           | Code2Vec    |
| -------------------- | ----------------- | ----------------- | ------------------ | ----------- |
| Input | Lab 3 token streams | Lab 3 token streams | Sampled Lab 3 token streams | Python source parsed as AST |
| Representation | 500 raw count dimensions | 500 IDF-weighted count dimensions | Learned 50-dimensional skip-gram vectors | Counts over AST ancestor-path signatures |
| Context awareness | Symmetric 2-token window | Symmetric 2-token window | 5-token training window | AST node ancestry, up to 6 node types |
| Structural awareness | None | None | None explicitly | Limited AST path shape |
| Dense/Sparse | Dense saved rows from sparse counts | Dense saved rows from sparse counts | Dense | Sparse path counts, emitted as dense CSV columns |
| Interpretability | Named context counts | Named weighted context counts | Latent dimensions | Path signatures are inspectable |
| Main advantage | Simple and auditable | Down-weights corpus-wide contexts | Learns compact distributed vectors | Includes syntax-tree path shape |
| Main limitation | Frequent/noisy contexts and no structure | Still context-count based | Small one-epoch sample yields unstable neighborhoods | Educational path counts, not original Code2Vec |

---

# 10. Word2Vec vs Custom Embedding

The Word2Vec representation will be compared with the custom embedding approach.

The comparison will focus on:

- Similarity between related tokens
- Similarity between unrelated tokens
- Context awareness
- Representation quality
- Failure cases
- Computational requirements
- Interpretability

### Observations

On the shared 20-token sample, the custom raw co-occurrence top pair was `integer`/`title` at 0.880550; IDF context weighting changed it to 0.794328. Word2Vec instead selected its own 20 tokens from the bounded training vocabulary and ranked `reason`/`order` first at 0.986384, with `abstractmethod`/`itertools` at 0.965070. The score scales are not directly comparable because the token sets, dimensions, and learning procedures differ. Custom vectors expose context dimensions, while Word2Vec's 50 dimensions are latent and trained from positive and negative pairs. The observed Word2Vec pairs demonstrate noisy similarity, not superior semantics. Its 300-record, one-epoch run is computationally manageable but has less corpus coverage than the custom methods.

---

# 11. Screenshots

Screenshots documenting the experimental process will be stored in:

```text
Lab4/Output/screenshots/
```

Terminal capture tooling is not available in this environment, so no screenshot images are claimed. Actual command output will be preserved as plain text in `Output/terminal_logs/`. This documents experiment execution/results but does not satisfy the manual's image screenshot requirement; the initial chat prompts also cannot be captured as terminal screenshots.

---

# 12. Source Code

All implementation files will be maintained under:

```text
Lab4/src/
```

The source code will include the implementations for:

- Custom Embedding Approach 1
- Custom Embedding Approach 2
- Cosine similarity calculation
- Word2Vec
- Code2Vec
- Supporting preprocessing/utilities

---

# 13. Data

Generated datasets and experiment outputs will be maintained under:

```text
Lab4/Data/
```

Data generated during the experiments will be documented so that the results can be reproduced.

---

# 14. Key Findings

The co-occurrence and TF-IDF experiments produce interpretable context profiles but preserve semantic ambiguity. In the measured comparison, IDF weighting reduced `integer`/`title` similarity from 0.880550 to 0.794328. The Word2Vec sample learned compact dense vectors, but its high `abstractmethod`/`itertools` similarity illustrates noisy associations. The AST path-count experiment used structural features, yet three different test identifiers had identical feature vectors and cosine 1.0. None of these experiments measures task accuracy.

1. The two custom approaches use raw counts versus IDF-weighted context counts; IDF reduced but did not remove the `integer`/`title` overlap.
2. Word2Vec produced dense 50-dimensional vectors, with noisy high similarities on its limited sample.
3. AST path counts expose tree ancestry but collapsed three distinct test identifiers to identical vectors.
4. The three approaches differ in token coverage, dimensions, interpretability, and structural signal; their cosine scores do not establish a universal ranking.

---

# 15. Conclusion

This lab explores different techniques for representing source code as numerical embeddings.

The experiments show four different representations of the same Lab 3 source corpus: raw local counts, IDF-weighted contexts, learned skip-gram vectors, and simplified AST path counts. Their similarity scores reflect the specific representation and sample used; they should not be interpreted as correctness scores or a universal ranking. The Code2Vec experiment is explicitly educational rather than a reproduction of the original model.

---

# 16. Submission Checklist

Before submission, verify the following:

- [x] Two custom embedding approaches implemented
- [x] 20 tokens selected for each custom experiment
- [x] Embeddings generated
- [x] Pairwise cosine similarity calculated
- [x] Five most similar pairs identified for each experiment
- [x] Similarity results analyzed
- [x] At least two representation failures identified for each custom approach
- [x] Word2Vec implemented
- [x] Code2Vec-inspired AST path experiment implemented
- [x] Word2Vec compared with custom embedding
- [x] Thought process documented
- [x] Observations documented
- [ ] Screenshot images of prompts/results added to `Output/screenshots/` (not capturable in this environment; terminal logs are provided instead)
- [x] Source code added to `src/`
- [x] Data added to `Data/`
- [x] README completed
- [x] Changes committed to Git
- [x] Changes pushed to GitHub

---

## 17. GitHub Repository

Repository:

**CSET456Lab_Dev_Ops**

GitHub organization/account:

**Aarush-Gupta15**

Lab 4 will be maintained inside:

```text
CSET456Lab_Dev_Ops/Lab4/
```

The final Lab 4 work will be committed and pushed to the repository before the submission deadline.

---

## 18. Submission Deadline

**October 1, 2026**

All required source code, data, screenshots, README documentation, and Git commits should be completed before the deadline.
