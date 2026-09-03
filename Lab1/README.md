# LAB-1: Mining and Profiling a Software Repository

**Course:** CSET456 – DevOps  
**Lab:** 1  
**Repository Analyzed:** [psf/requests](https://github.com/psf/requests)

---

## 1. Objective

The objective of this lab is to mine and profile a software repository using Python and Git.

The analysis covers:

- Repository inventory
- Source-code identification
- Lines of Code (LOC)
- Programming languages
- File-type distribution
- Largest source files
- File-level metrics
- Git commit history
- Contributors
- Frequently changed files
- Monthly commit activity
- Code additions and deletions

---

## 2. Repository Used

The repository analyzed in this lab is the Python Requests library:

**Repository:** `psf/requests`

The repository was cloned locally and analyzed using a Python mining script and Git commands.

---

## 3. Repository Structure

The Lab 1 directory is organized as follows:

```text
Lab1/
├── README.md
└── requests/
    ├── mining/
    │   ├── file_metrics.csv
    │   ├── git_history.csv
    │   └── repository_stats.json
    └── mine_repository.py
```

## 4. Repository Inventory

| Metric            |       Result |
| ----------------- | -----------: |
| Repository        | psf/requests |
| Total Files       |          128 |
| Source-Code Files |           39 |
| Directories       |           25 |
| Total LOC         |        9,875 |

## 5. Programming Languages

| Language  | Number of Files |
| --------- | --------------: |
| Python    |              37 |
| HTML      |               1 |
| CSS       |               1 |
| **Total** |          **39** |

## 6. File-Type Distribution

| File Type    | Count |
| ------------ | ----: |
| No extension |    18 |
| `.rst`       |    16 |
| `.md`        |    13 |
| `.yml`       |    10 |
| `.png`       |     5 |
| `.key`       |     4 |
| `.cnf`       |     4 |
| `.pem`       |     3 |
| `.csr`       |     3 |
| `.yaml`      |     2 |
| `.txt`       |     2 |
| `.toml`      |     1 |
| `.in`        |     1 |
| `.ini`       |     1 |
| `.ai`        |     1 |
| `.svg`       |     1 |
| `.crt`       |     1 |
| `.srl`       |     1 |
| `.bat`       |     1 |
| `.html`      |     1 |
| `.css`       |     1 |
| `.typed`     |     1 |
| `.py`        |    37 |

## 7.Largest Source Files

| Rank | File                       |   LOC | Size (Bytes) |
| ---: | -------------------------- | ----: | -----------: |
|    1 | `tests/test_requests.py`   | 2,597 |      108,534 |
|    2 | `src/requests/models.py`   |   988 |       41,462 |
|    3 | `src/requests/utils.py`    |   915 |       36,061 |
|    4 | `tests/test_utils.py`      |   875 |       31,454 |
|    5 | `src/requests/sessions.py` |   758 |       34,072 |
|    6 | `src/requests/adapters.py` |   634 |       27,992 |
|    7 | `src/requests/cookies.py`  |   503 |       21,504 |
|    8 | `tests/test_lowlevel.py`   |   329 |       15,343 |
|    9 | `docs/conf.py`             |   291 |       12,148 |
|   10 | `src/requests/auth.py`     |   283 |       12,107 |

## 8. File-Level Metrics

A CSV dataset was generated containing metrics for every identified source-code file.

CSV Columns
file_path,language,extension,loc,size_bytes

The dataset is available at:

requests/mining/file_metrics.csv

Example:

docs/conf.py,Python,.py,291,12148
src/requests/**init**.py,Python,.py,184,5637
src/requests/models.py,Python,.py,988,41462

## 9. Git History Analysis

| Metric                          |        Result |
| ------------------------------- | ------------: |
| Total Commits                   |         6,494 |
| Contributor Identities          |           841 |
| Most Active Contributor         | Kenneth Reitz |
| Most Active Contributor Commits |         2,142 |
| Average Files Changed / Month   |         46.74 |
| Average Additions / Commit      |         25.66 |
| Average Deletions / Commit      |         21.06 |

## 10. Most Frequently Changed Files

| Rank | File                     | Changes |
| ---: | ------------------------ | ------: |
|    1 | `requests/models.py`     |     761 |
|    2 | `test_requests.py`       |     379 |
|    3 | `requests/sessions.py`   |     365 |
|    4 | `HISTORY.rst`            |     324 |
|    5 | `tests/test_requests.py` |     297 |
|    6 | `requests/utils.py`      |     295 |
|    7 | `docs/user/advanced.rst` |     225 |
|    8 | `requests/__init__.py`   |     189 |
|    9 | `docs/index.rst`         |     188 |
|   10 | `setup.py`               |     184 |

## 11.Commits Per Month

| Month   | Commits |
| ------- | ------: |
| 2011-02 |     194 |
| 2011-03 |      14 |
| 2011-04 |      24 |
| 2011-05 |     121 |
| 2011-06 |      58 |
| 2011-07 |      24 |
| 2011-08 |     221 |
| 2011-09 |     105 |
| 2011-10 |     237 |

## 12. Generated Files

The mining process generated three datasets:

file_metrics.csv

Contains file-level source-code metrics:

File path
Programming language
Extension
LOC
File size
git_history.csv

Contains monthly Git history metrics:

Month
Number of commits
Files changed
Additions
Deletions
repository_stats.json

Contains the complete repository inventory and Git-history statistics in JSON format.

## 13. Mining Script

The repository was analyzed using:

requests/mine_repository.py

The Python script performs:

1 Repository traversal
2 File counting
3 Directory counting
4 Source-code identification
5 LOC calculation
6 File-size calculation
7 Language identification
8 File-type distribution
9 Largest-file analysis
10 Git commit analysis
11 Contributor analysis
12 Frequently changed file analysis
13 Monthly Git activity analysis
14 CSV generation
15 JSON generation

## 14. Key Findings

The analysis shows that:

The repository contains 128 files and 25 directories.
There are 39 identified source-code files.
Python is the dominant programming language.
The repository contains approximately 9,875 non-empty source-code lines.
tests/test_requests.py is the largest identified source file.
The repository has 6,494 commits, showing extensive development history.
Git records 841 contributor identities.
Kenneth Reitz is the most active recorded contributor by commit count.
requests/models.py is the most frequently changed historical file.
Git activity varies significantly across different periods of the project's development.

## 15. Conclusion

This lab demonstrated how software repository mining can be used to understand both the current structure and historical evolution of a software project.

The analysis combined Python-based static file profiling with Git history mining to extract measurable information about source code, files, contributors, commits, and development activity.

The resulting CSV and JSON datasets provide structured data that can be used for further software engineering and DevOps analysis.

## 16. Tools Used

Python 3
Git
GitHub
CSV
JSON
macOS Terminal
