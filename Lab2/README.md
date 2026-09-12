# CSET456 DevOps Lab 2

## GitHub Repository Mining and Dataset Preparation

## 1. Objective

The objective of this laboratory exercise is to mine software repositories from GitHub and prepare structured datasets from their source-code information and Git commit history.

The experiment focuses on:

- Mining source-code files from multiple GitHub repositories.
- Extracting source-code attributes such as programming language, file size and lines of code.
- Extracting Git commit-history information.
- Cleaning and structuring the extracted data.
- Identifying relevant and irrelevant attributes.
- Creating separate source-code and commit-history datasets.
- Creating a logically related combined dataset.
- Generating statistical summaries in JSON format.
- Understanding software evolution through source-code and repository-history data.

---

## 2. Repositories Used

Five open-source GitHub repositories were selected for this experiment.

| No. | Repository   | GitHub URL                                   |
| --- | ------------ | -------------------------------------------- |
| 1   | Flask        | https://github.com/pallets/flask             |
| 2   | Requests     | https://github.com/psf/requests              |
| 3   | Pytest       | https://github.com/pytest-dev/pytest         |
| 4   | FastAPI      | https://github.com/fastapi/fastapi           |
| 5   | Scikit-learn | https://github.com/scikit-learn/scikit-learn |

These repositories were selected because they are established open-source Python projects with substantial source code and Git histories.

---

## 3. Methodology

The repository mining process was performed separately for each repository.

### Step 1: Repository Cloning

Each repository was cloned into the local `Lab2/working/` directory using Git.

The repositories were processed independently to preserve repository identity and avoid mixing source files or commit records between projects.

### Step 2: Source-Code Mining

The current source tree of the default branch of each repository was examined.

Source files were identified using supported programming-language extensions.

The mining process collected:

- Repository name
- File path
- File name
- Directory
- Programming language
- File extension
- Lines of code
- File size
- Test-file indicator

### Step 3: Commit-History Mining

Git commit history was extracted from the default branch of each repository.

The commit dataset contains:

- Repository
- Commit hash
- Commit date
- Author
- Commit message
- Number of files changed
- Lines added
- Lines deleted
- Merge-commit indicator

### Step 4: Data Cleaning

The extracted data was cleaned before generating the final datasets.

The following cleaning operations were performed:

- `.git` metadata was excluded from source-code mining.
- Build and cache directories were excluded.
- Virtual-environment and dependency directories were excluded.
- Only supported source-code extensions were included.
- Binary files were excluded from source-code analysis.
- Empty or invalid file paths were ignored.
- Duplicate source-file records were removed using repository and file path.
- Duplicate commit records were removed using repository and commit hash.
- File paths were normalized to a consistent POSIX format.
- Missing numeric history values were represented as zero where appropriate.
- Commit additions and deletions were converted to numeric values.
- Binary Git changes represented by `-` were handled without treating them as numeric line changes.

---

## 4. Source-Code Dataset

The source-code dataset is stored at:

`Output/source_code_dataset.csv`

### Schema

| Attribute      | Description                                             | Relevance |
| -------------- | ------------------------------------------------------- | --------- |
| `repository`   | Name of the GitHub repository                           | Relevant  |
| `file_path`    | Relative path of the source file                        | Relevant  |
| `file_name`    | Name of the source file                                 | Relevant  |
| `directory`    | Directory containing the file                           | Relevant  |
| `language`     | Programming language                                    | Relevant  |
| `extension`    | File extension                                          | Relevant  |
| `loc`          | Number of non-empty lines of code                       | Relevant  |
| `size_bytes`   | File size in bytes                                      | Relevant  |
| `is_test_file` | Indicates whether the file is identified as a test file | Relevant  |

### Source-Code Statistics

- Total source-code records: **2,623**
- Total repositories: **5**
- Total lines of code: **604,468**
- Total source-code size: **25,004,678 bytes**
- Python files: **2,568**
- Shell files: **29**
- JavaScript files: **11**
- C/C++ header files: **7**
- C++ files: **5**
- C files: **3**
- Test files: **1,125**
- Non-test files: **1,498**

---

## 5. Commit-History Dataset

The commit-history dataset is stored at:

`Output/commit_history_dataset.csv`

### Schema

| Attribute         | Description                                       | Relevance |
| ----------------- | ------------------------------------------------- | --------- |
| `repository`      | Repository associated with the commit             | Relevant  |
| `commit_hash`     | Unique Git commit identifier                      | Relevant  |
| `date`            | Commit date and time                              | Relevant  |
| `author`          | Git author name                                   | Relevant  |
| `commit_message`  | Commit description                                | Relevant  |
| `files_changed`   | Number of files changed by the commit             | Relevant  |
| `additions`       | Number of added lines                             | Relevant  |
| `deletions`       | Number of deleted lines                           | Relevant  |
| `is_merge_commit` | Indicates whether the commit has multiple parents | Relevant  |

### Commit-History Statistics

- Total commits: **71,487**
- Total repositories: **5**
- Unique author names: **6,947**
- Total files changed: **187,535**
- Total additions: **6,999,081**
- Total deletions: **5,796,290**
- Total churn: **12,795,371**
- Merge commits: **10,897**
- Non-merge commits: **60,590**

Where:

`Total Churn = Additions + Deletions`

---

## 6. Combined Dataset

The combined dataset is stored at:

`Output/combined_dataset.csv`

The combined dataset connects the current source-code snapshot with its historical Git activity.

### Relationship Used

The relationship used for combining the datasets is:

`repository + file_path`

This means that source-code information is connected only with commit-history information belonging to the **same repository and the same source file path**.

The commit history was first aggregated at the repository-file level using:

- Number of commits touching the file
- Total additions
- Total deletions
- Total churn
- Number of unique authors
- First modification date
- Last modification date

This approach provides a meaningful relationship between source-code characteristics and software evolution.

A Cartesian product was deliberately avoided because pairing every source file with every commit would produce unrelated records and misleading analysis.

### Combined Dataset Schema

| Attribute               | Description                                 |
| ----------------------- | ------------------------------------------- |
| `repository`            | Repository name                             |
| `file_path`             | Relative source-file path                   |
| `file_name`             | Source-file name                            |
| `directory`             | Directory containing the file               |
| `language`              | Programming language                        |
| `extension`             | File extension                              |
| `loc`                   | Current lines of code                       |
| `size_bytes`            | Current file size                           |
| `is_test_file`          | Test-file indicator                         |
| `commits_touching_file` | Number of commits affecting the file        |
| `total_additions`       | Total historical additions                  |
| `total_deletions`       | Total historical deletions                  |
| `unique_authors`        | Number of unique authors affecting the file |
| `first_modified_date`   | Earliest recorded modification              |
| `last_modified_date`    | Most recent recorded modification           |
| `total_churn`           | Historical additions plus deletions         |

### Combined Dataset Statistics

- Total records: **2,623**
- Total repositories: **5**
- Total current LOC: **604,468**
- Total historical churn associated with current source files: **1,786,430**
- Files with history: **2,622**
- Files without matching history: **1**
- Average LOC per file: **230.45**
- Average historical churn per file: **681.06**

Approximately **99.96%** of the current source files have corresponding historical Git activity.

---

## 7. Relevant and Irrelevant Attributes

### Relevant Attributes

The following attributes were considered relevant because they directly support source-code analysis, repository evolution analysis, or the relationship between source code and Git history:

- Repository identity
- File path
- File name
- Programming language
- File extension
- Lines of code
- File size
- Test-file status
- Commit hash
- Commit date
- Author
- Commit message
- Files changed
- Additions
- Deletions
- Merge status
- File-level commit count
- Historical churn
- First and last modification dates

### Irrelevant or Excluded Attributes

The following information was not included in the analytical datasets:

- `.git` internal metadata
- Git object files
- Git hooks
- Local repository configuration
- Build artifacts
- Dependency directories
- Python cache files
- Virtual-environment files
- Binary source files
- Temporary files
- Local machine-specific information

These attributes do not provide meaningful information for the intended source-code and software-evolution analysis.

---

## 8. Data Cleaning and Preparation

Data cleaning was performed before combining the datasets.

### Source-Code Cleaning

Only recognized source-code extensions were considered.

Common generated, temporary, cache, build, and dependency directories were excluded.

Binary files were detected using a binary-content check and excluded from source-code analysis.

File paths were normalized so that equivalent paths use a consistent format.

### Commit Cleaning

Commit records were identified using the full 40-character Git commit hash.

Duplicate commit records were removed using:

`repository + commit_hash`

Commit additions and deletions were converted into numeric values.

Merge commits were identified from the number of Git parents rather than relying only on file-change counts.

### Identity Preservation

Repository identity is retained in every dataset.

This prevents files with identical names in different repositories from being incorrectly treated as the same file.

Git author names were preserved as provided by Git. Automatic identity merging was not performed because different author names may represent the same person and should not be merged without reliable evidence.

---

## 9. Use Cases and Problems Addressed

The generated datasets can support several software-engineering and DevOps use cases.

### 9.1 Code Maintenance

LOC, file size, and historical churn can help identify large or frequently modified files that may require additional maintenance attention.

### 9.2 Change Hotspot Detection

Files with a high number of commits or high historical churn can be identified as potential change hotspots.

### 9.3 Test-Code Analysis

The `is_test_file` attribute allows comparison between test and non-test source files.

### 9.4 Software Evolution Analysis

Commit dates, additions, deletions, and file-level history can be used to understand how projects evolve over time.

### 9.5 Contributor Analysis

The author information can be used to study contributor participation and the number of contributors affecting individual files.

### 9.6 Technical-Debt Investigation

Frequently modified and high-churn files may indicate areas of complexity, instability, or potential technical debt.

### 9.7 Repository Comparison

The same schema across five repositories allows comparative analysis of project size, programming languages, commit activity, and source-code evolution.

---

## 10. Observations

Several observations can be made from the generated datasets:

1. The five repositories contain **2,623 source files** in total.
2. Python is the dominant programming language, with **2,568 Python files**.
3. The repositories contain more than **604,000 lines of current source code**.
4. The commit-history dataset contains **71,487 commits**.
5. More than **12.7 million lines of total historical churn** were recorded.
6. The combined dataset connects almost all current source files with historical Git activity.
7. The large number of commits and file changes demonstrates significant software evolution across the selected open-source projects.
8. The combined dataset provides a more meaningful analytical view than simply joining unrelated source files and commits.

---

## 11. Generated Output Files

The following files are generated in the `Output/` directory:

```text
Output/
├── source_code_dataset.csv
├── commit_history_dataset.csv
├── combined_dataset.csv
├── source_code_statistics.json
├── commit_history_statistics.json
├── combined_dataset_statistics.json
└── screenshots/
```

12. Source Code

The repository-mining implementation is available at:

Lab2/src/mine_repositories.py

The script automates:

Repository cloning
Source-code mining
Commit-history mining
Data cleaning
Dataset generation
Dataset combination
Statistical analysis
JSON statistics generation 13. Reproducibility
Requirements
Python 3.x
Git
pandas

A Python virtual environment can be used to isolate the project dependencies.

Install Dependencies
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Run the Mining Script

From the project root:

python Lab2/src/mine_repositories.py

The script processes all five repositories and generates the required datasets and statistics in:

Lab2/Output/ 14. Tools and Technologies

The following tools and technologies were used:

Python
Pandas
Git
GitHub
CSV
JSON
Visual Studio Code
macOS Terminal
Python virtual environment 15. Project Structure
CSET456Lab_Dev_Ops/
│
├── Lab1/
│ └── ...
│
└── Lab2/
├── README.md
│
├── Data/
│ ├── flask/
│ ├── requests/
│ ├── pytest/
│ ├── fastapi/
│ └── scikit-learn/
│
├── Output/
│ ├── source_code_dataset.csv
│ ├── commit_history_dataset.csv
│ ├── combined_dataset.csv
│ ├── source_code_statistics.json
│ ├── commit_history_statistics.json
│ ├── combined_dataset_statistics.json
│ └── screenshots/
│
└── src/
└── mine_repositories.py

The local Lab2/working/ directory is used for repository clones during mining and is excluded from version control.

16. Conclusion

This laboratory successfully demonstrates the process of mining multiple open-source GitHub repositories and converting repository information into structured datasets.

Separate source-code and commit-history datasets were generated, cleaned, and analyzed. A third combined dataset was created using the meaningful relationship of repository and file path, allowing source-code characteristics to be associated with historical file-level activity.

The generated statistics demonstrate substantial source-code size, contributor activity, commit activity, and historical code churn across the five selected repositories.

The resulting datasets can be used for further software-engineering, DevOps, repository analytics, maintenance, and software-evolution studies.
