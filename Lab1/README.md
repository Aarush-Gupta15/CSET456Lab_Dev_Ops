# CSET456 – DevOps Lab 1

## Mining and Profiling a Software Repository

### 1. Objective

The objective of this lab is to mine and profile a software repository using Git and Python.

The analysis focuses on:

- Repository inventory
- Number of files and directories
- Programming languages
- Lines of Code (LOC)
- File-type distribution
- Largest source-code files
- File-level metrics
- Git commit history
- Contributor activity
- Frequently modified files
- Monthly commit activity
- File additions and deletions

The repository analyzed in this lab is **Requests**, a popular Python HTTP library.

---

## 2. Repository Used

**Repository:** `psf/requests`

**GitHub:** https://github.com/psf/requests

The repository was cloned locally and analyzed using a custom Python mining script.

---

## 3. Lab Directory Structure

The Lab 1 files are organized as follows:

```text
Lab1/
├── README.md
├── Data/
│   └── Requests repository
│       ├── .github/
│       ├── docs/
│       ├── src/
│       ├── tests/
│       ├── setup.py
│       ├── pyproject.toml
│       ├── README.md
│       └── ...
│
├── Output/
│   ├── file_metrics.csv
│   ├── git_history.csv
│   └── repository_stats.json
│
└── src/
    └── mine_repository.py
```

### Folder Description

| Folder/File | Description                                        |
| ----------- | -------------------------------------------------- |
| `Data/`     | Contains the Requests repository used for analysis |
| `Output/`   | Contains generated CSV and JSON analysis results   |
| `src/`      | Contains the Python mining script                  |
| `README.md` | Documentation and findings of the lab              |

---

# 4. Repository Inventory

The mining script analyzed the current contents of the Requests repository.

### Inventory Results

| Metric                 |         Result |
| ---------------------- | -------------: |
| Repository             | `psf/requests` |
| Total Files            |        **128** |
| Source-Code Files      |         **39** |
| Directories            |         **25** |
| Total LOC              |      **9,875** |
| Total Commits          |      **6,494** |
| Contributor Identities |        **841** |

### LOC Definition

For this lab, **LOC (Lines of Code)** is calculated as the number of **non-empty lines** in a file.

Blank lines are not counted.

---

# 5. Programming Languages

The repository contains the following detected programming/source languages:

| Language  | Number of Files |
| --------- | --------------: |
| Python    |              37 |
| HTML      |               1 |
| CSS       |               1 |
| **Total** |          **39** |

Python is the dominant programming language in the repository.

---

# 6. File-Type Distribution

The repository contains multiple types of source, documentation, configuration, certificate, and other files.

| Extension    | Number of Files |
| ------------ | --------------: |
| `.py`        |              37 |
| `.rst`       |              16 |
| `.md`        |              13 |
| `.yml`       |              10 |
| `.png`       |               5 |
| `.key`       |               4 |
| `.cnf`       |               4 |
| `.pem`       |               3 |
| `.csr`       |               3 |
| `.yaml`      |               2 |
| `.txt`       |               2 |
| `.html`      |               1 |
| `.css`       |               1 |
| `.toml`      |               1 |
| `.in`        |               1 |
| `.ini`       |               1 |
| `.ai`        |               1 |
| `.svg`       |               1 |
| `.crt`       |               1 |
| `.srl`       |               1 |
| `.bat`       |               1 |
| `.typed`     |               1 |
| No extension |              18 |

The `.py` extension is the most common source-code file type.

---

# 7. Largest Source-Code Files

The following are the largest source files based on non-empty LOC:

| Rank | File                       | Language |   LOC |
| ---: | -------------------------- | -------- | ----: |
|    1 | `tests/test_requests.py`   | Python   | 2,597 |
|    2 | `src/requests/models.py`   | Python   |   988 |
|    3 | `src/requests/utils.py`    | Python   |   915 |
|    4 | `tests/test_utils.py`      | Python   |   875 |
|    5 | `src/requests/sessions.py` | Python   |   758 |
|    6 | `src/requests/adapters.py` | Python   |   634 |
|    7 | `src/requests/cookies.py`  | Python   |   503 |
|    8 | `tests/test_lowlevel.py`   | Python   |   329 |
|    9 | `docs/conf.py`             | Python   |   291 |
|   10 | `src/requests/auth.py`     | Python   |   283 |

### Observation

`tests/test_requests.py` is the largest source file with **2,597 LOC**. This indicates that the project has a substantial automated test suite for validating the behavior of the Requests library.

---

# 8. File-Level Metrics

A detailed file-level dataset was generated and stored in:

```text
Output/file_metrics.csv
```

The CSV contains the following fields:

```text
file_path
language
extension
loc
size_bytes
```

### Example

```text
file_path,language,extension,loc,size_bytes
docs/_static/custom.css,CSS,.css,8,287
docs/_templates/sidebar.html,HTML,.html,26,1361
docs/_themes/flask_theme_support.py,Python,.py,74,4875
docs/conf.py,Python,.py,291,12148
setup.py,Python,.py,6,179
src/requests/__init__.py,Python,.py,184,5637
```

This dataset can be used for further analysis of source-code size and file complexity.

---

# 9. Git History Mining

Git history was analyzed to understand the development activity of the repository.

The analysis includes:

- Total number of commits
- Contributor activity
- Frequently changed files
- Commits per month
- Files changed per month
- Lines added
- Lines deleted

---

## 9.1 Total Commits

The repository contains:

**6,494 commits**

This indicates a long development history with substantial ongoing maintenance and contributions.

---

## 9.2 Contributors

The analysis identified:

**841 Git author identities**

> Note: Contributor count represents Git author identities based on author name and email. Different identities may belong to the same person.

### Most Active Contributor

**Kenneth Reitz [me@kennethreitz.com](mailto:me@kennethreitz.com)**

Number of commits:

**2,142**

Kenneth Reitz is therefore the most active contributor according to the mined Git history.

---

# 10. Most Frequently Changed Files

The following files have been changed most frequently according to the Git history analysis:

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

### Observation

`requests/models.py` has the highest number of recorded changes with **761 changes**.

This suggests that the file has been an important part of the project's evolution and has undergone frequent modification throughout its development history.

> Historical Git paths may differ from the repository's current paths because files can be moved or renamed over time.

---

# 11. Commits Per Month

Monthly Git history was extracted into:

```text
Output/git_history.csv
```

The dataset contains:

```text
month
commits
files_changed
additions
deletions
```

### Example

```text
month,commits,files_changed,additions,deletions
2011-02,194,212,3905,1659
2011-03,14,15,78,32
2011-04,24,19,526,77
2011-05,121,165,2924,1403
2011-06,58,69,2798,278
2011-07,24,24,179,38
2011-08,221,240,2499,1177
2011-09,105,175,2923,2432
2011-10,237,287,4554,2623
```

The complete monthly history is available in the CSV file.

---

# 12. Git Activity Statistics

The following averages were calculated from the Git history:

| Metric                  |   Average |
| ----------------------- | --------: |
| Files Changed per Month | **46.74** |
| Additions per Commit    | **25.66** |
| Deletions per Commit    | **21.06** |

These metrics provide an overview of the repository's development activity.

---

# 13. Generated Output Files

The mining process generates three main output files.

### 1. `file_metrics.csv`

Location:

```text
Output/file_metrics.csv
```

Contains file-level information including:

- File path
- Programming language
- Extension
- LOC
- File size in bytes

---

### 2. `git_history.csv`

Location:

```text
Output/git_history.csv
```

Contains monthly Git statistics including:

- Month
- Number of commits
- Files changed
- Lines added
- Lines deleted

---

### 3. `repository_stats.json`

Location:

```text
Output/repository_stats.json
```

Contains the complete repository inventory and Git history summary in JSON format.

---

# 14. Mining Script

The repository was analyzed using the Python script:

```text
src/mine_repository.py
```

The script performs the following operations:

1. Walks through the repository.
2. Counts files and directories.
3. Identifies programming languages based on file extensions.
4. Calculates non-empty LOC.
5. Calculates file sizes.
6. Identifies the largest source files.
7. Calculates file-type distribution.
8. Analyzes Git commit history.
9. Counts contributors.
10. Identifies the most active contributor.
11. Identifies frequently changed files.
12. Calculates monthly commit statistics.
13. Calculates additions and deletions.
14. Generates CSV and JSON output files.

---

# 15. Tools Used

The following tools and technologies were used:

- **Git**
- **GitHub**
- **Python**
- **CSV**
- **JSON**
- **Terminal / Command Line**
- **Git log**
- **Git numstat**

---

# 16. Key Findings

The main findings from the repository mining exercise are:

1. The Requests repository contains **128 files** and **25 directories**.
2. There are **39 source-code files**.
3. **Python** is the primary programming language.
4. The repository contains **9,875 non-empty lines of code**.
5. `tests/test_requests.py` is the largest source file with **2,597 LOC**.
6. The repository has **6,494 commits**.
7. The Git history contains **841 author identities**.
8. **Kenneth Reitz** is the most active contributor with **2,142 commits**.
9. `requests/models.py` has the highest number of historical changes with **761 changes**.
10. The average number of files changed per month is **46.74**.
11. The average number of additions per commit is **25.66**.
12. The average number of deletions per commit is **21.06**.

---

# 17. Conclusion

This lab demonstrates how software repositories can be systematically mined and profiled using Git and Python.

The analysis provides both **static repository information** and **historical development information**. Static analysis helps understand the size, structure, languages, and source-code distribution of the project, while Git history analysis provides insights into contributors, development activity, frequently modified files, and code changes over time.

The generated CSV and JSON datasets can also be used for further software analytics and visualization.

---

## Lab 1 Summary

**Repository:** `psf/requests`

**Total Files:** 128

**Source Files:** 39

**Directories:** 25

**Total LOC:** 9,875

**Total Commits:** 6,494

**Contributors:** 841

**Most Active Contributor:** Kenneth Reitz

**Largest Source File:** `tests/test_requests.py` — 2,597 LOC

**Most Changed File:** `requests/models.py` — 761 changes

**Average Files Changed/Month:** 46.74

**Average Additions/Commit:** 25.66

**Average Deletions/Commit:** 21.06
