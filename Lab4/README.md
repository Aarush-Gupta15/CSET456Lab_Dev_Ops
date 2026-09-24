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

The exact files will be added as each experiment is implemented.

---

# 5. Experiment 1 — Custom Embedding Approach 1

## 5.1 Approach

The first embedding approach will be designed independently.

### Thought Process

The approach will be based on:

- [To be documented after implementation]
- [Why this representation was selected]
- [What information the representation is expected to capture]
- [Expected advantages]
- [Expected limitations]

## 5.2 Token Selection

Twenty tokens will be selected manually and randomly from the source-code vocabulary.

The selected tokens will be recorded here after the experiment is executed.

| No. | Token |
| --: | ----- |
|   1 | TBD   |
|   2 | TBD   |
|   3 | TBD   |
|   4 | TBD   |
|   5 | TBD   |
|   6 | TBD   |
|   7 | TBD   |
|   8 | TBD   |
|   9 | TBD   |
|  10 | TBD   |
|  11 | TBD   |
|  12 | TBD   |
|  13 | TBD   |
|  14 | TBD   |
|  15 | TBD   |
|  16 | TBD   |
|  17 | TBD   |
|  18 | TBD   |
|  19 | TBD   |
|  20 | TBD   |

## 5.3 Embedding Generation

Embeddings will be generated for all 20 selected tokens.

The implementation and generated data will be stored in the `src/` and `Data/` directories.

## 5.4 Cosine Similarity

Pairwise cosine similarity will be calculated between all selected token embeddings.

The resulting similarities will be analyzed to determine which tokens have the most similar representations.

## 5.5 Five Most Similar Pairs

The five most similar token pairs will be reported after the experiment.

| Rank | Token 1 | Token 2 | Cosine Similarity |
| ---: | ------- | ------- | ----------------: |
|    1 | TBD     | TBD     |               TBD |
|    2 | TBD     | TBD     |               TBD |
|    3 | TBD     | TBD     |               TBD |
|    4 | TBD     | TBD     |               TBD |
|    5 | TBD     | TBD     |               TBD |

## 5.6 Analysis

The similarity results will be analyzed based on the expected relationship between the source-code tokens.

Questions considered:

- Do semantically related tokens receive similar representations?
- Do syntactically related tokens receive similar representations?
- Are common programming-language tokens grouped together?
- Are unrelated tokens incorrectly considered similar?

## 5.7 Representation Failures

At least two failure cases will be identified.

| Case | Tokens | Observation |
| ---- | ------ | ----------- |
| 1    | TBD    | TBD         |
| 2    | TBD    | TBD         |

---

# 6. Experiment 2 — Custom Embedding Approach 2

## 6.1 Approach

A second embedding approach will be developed independently from the first approach.

### Thought Process

The approach will be based on:

- [To be documented after implementation]
- [Why this representation was selected]
- [Expected advantages]
- [Expected limitations]
- [Difference from Approach 1]

## 6.2 Token Selection

The experiment will use 20 selected tokens.

The exact tokens and selection process will be documented after implementation.

## 6.3 Embedding Generation

Embeddings will be generated for the selected tokens using the second approach.

## 6.4 Cosine Similarity

Pairwise cosine similarity will be calculated between all token embeddings.

## 6.5 Five Most Similar Pairs

| Rank | Token 1 | Token 2 | Cosine Similarity |
| ---: | ------- | ------- | ----------------: |
|    1 | TBD     | TBD     |               TBD |
|    2 | TBD     | TBD     |               TBD |
|    3 | TBD     | TBD     |               TBD |
|    4 | TBD     | TBD     |               TBD |
|    5 | TBD     | TBD     |               TBD |

## 6.6 Analysis

The similarity results will be analyzed to determine whether the representation captures meaningful relationships between source-code tokens.

## 6.7 Representation Failures

At least two failure cases will be documented.

| Case | Tokens | Observation |
| ---- | ------ | ----------- |
| 1    | TBD    | TBD         |
| 2    | TBD    | TBD         |

---

# 7. Experiment 3 — Word2Vec

Word2Vec will be implemented to learn distributed representations of source-code tokens based on their surrounding context.

The implementation will include:

1. Preparing tokenized source-code sequences.
2. Training the Word2Vec model.
3. Generating embeddings for selected tokens.
4. Calculating similarities between tokens.
5. Identifying related tokens.
6. Analyzing the learned representations.

## 7.1 Word2Vec Configuration

The final configuration will be documented after implementation.

| Parameter       | Value |
| --------------- | ----- |
| Vector size     | TBD   |
| Window          | TBD   |
| Minimum count   | TBD   |
| Training epochs | TBD   |
| Corpus size     | TBD   |

## 7.2 Results

The results will be recorded after training.

## 7.3 Observations

Observations about Word2Vec will be documented after the experiment.

---

# 8. Experiment 4 — Code2Vec

Code2Vec will be implemented to learn representations specifically from source-code structure.

The experiment will investigate how structural information from source code can be used to create meaningful code representations.

The implementation will document:

- Source-code preprocessing
- Representation of code structure
- Context extraction
- Embedding generation
- Similarity analysis
- Observed limitations

## 8.1 Results

Results will be added after implementation.

## 8.2 Observations

Observations about Code2Vec will be documented after the experiment.

---

# 9. Comparison of Embedding Approaches

The custom embeddings will be compared with Word2Vec and Code2Vec.

| Feature              | Custom Approach 1 | Custom Approach 2 | Word2Vec           | Code2Vec    |
| -------------------- | ----------------- | ----------------- | ------------------ | ----------- |
| Input                | TBD               | TBD               | Source-code tokens | Source code |
| Representation       | TBD               | TBD               | TBD                | TBD         |
| Context awareness    | TBD               | TBD               | TBD                | TBD         |
| Structural awareness | TBD               | TBD               | TBD                | TBD         |
| Main advantage       | TBD               | TBD               | TBD                | TBD         |
| Main limitation      | TBD               | TBD               | TBD                | TBD         |

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

The final observations will be added after both experiments have been completed.

---

# 11. Screenshots

Screenshots documenting the experimental process will be stored in:

```text
Lab4/Output/screenshots/
```

The screenshots will include:

- Initial prompts for each experiment
- Token selection
- Embedding generation
- Similarity calculations
- Word2Vec execution
- Code2Vec execution
- Important intermediate results
- Final results

The first few prompts for each experiment will be captured as required by the lab instructions.

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

This section will contain the final findings from the experiments.

Important observations will include:

1. How the two custom embedding approaches represent source-code tokens.
2. Which token relationships were captured successfully.
3. Where the representations failed.
4. How Word2Vec represents source-code tokens.
5. How Code2Vec differs from token-level embeddings.
6. Differences between Word2Vec and the custom embeddings.

---

# 15. Conclusion

This lab explores different techniques for representing source code as numerical embeddings.

The experiments will demonstrate the relationship between tokenization, embeddings, contextual similarity, and source-code structure.

The final conclusion will be updated after completing all experiments and comparing the results.

---

# 16. Submission Checklist

Before submission, verify the following:

- [ ] Two custom embedding approaches implemented
- [ ] 20 tokens selected for experiments
- [ ] Embeddings generated
- [ ] Pairwise cosine similarity calculated
- [ ] Five most similar pairs identified
- [ ] Similarity results analyzed
- [ ] At least two representation failures identified
- [ ] Word2Vec implemented
- [ ] Code2Vec implemented
- [ ] Word2Vec compared with custom embedding
- [ ] Thought process documented
- [ ] Observations documented
- [ ] Screenshots added to `Output/screenshots/`
- [ ] Source code added to `src/`
- [ ] Data added to `Data/`
- [ ] README completed
- [ ] Changes committed to Git
- [ ] Changes pushed to GitHub

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
