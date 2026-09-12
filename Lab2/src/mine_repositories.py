from pathlib import Path
import subprocess
import json
import re
from collections import Counter

import pandas as pd


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

LAB2_DIR = BASE_DIR / "Lab2"
DATA_DIR = LAB2_DIR / "Data"
OUTPUT_DIR = LAB2_DIR / "Output"
WORKING_DIR = LAB2_DIR / "working"


# ============================================================
# REPOSITORIES
# ============================================================

REPOSITORIES = {
    "flask": {
        "url": "https://github.com/pallets/flask.git",
        "data_dir": DATA_DIR / "flask",
    },
    "requests": {
        "url": "https://github.com/psf/requests.git",
        "data_dir": DATA_DIR / "requests",
    },
    "pytest": {
        "url": "https://github.com/pytest-dev/pytest.git",
        "data_dir": DATA_DIR / "pytest",
    },
    "fastapi": {
        "url": "https://github.com/fastapi/fastapi.git",
        "data_dir": DATA_DIR / "fastapi",
    },
    "scikit-learn": {
        "url": "https://github.com/scikit-learn/scikit-learn.git",
        "data_dir": DATA_DIR / "scikit-learn",
    },
}


# ============================================================
# SOURCE CODE CONFIGURATION
# ============================================================

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".h": "C/C++",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".sh": "Shell",
}


EXCLUDED_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "build",
    "dist",
    "_build",
    "site-packages",
}


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def run_git(command, cwd):
    """
    Run a Git command and return stdout.
    Raises an exception if the command fails.
    """

    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Git command failed:\n"
            f"{' '.join(command)}\n\n"
            f"{result.stderr}"
        )

    return result.stdout


def clone_repository(repository_name, repository_url, repository_path):
    """
    Clone repository if it does not already exist.
    """

    if repository_path.exists() and (repository_path / ".git").exists():
        print(f"[SKIP] {repository_name}: repository already cloned")
        return

    repository_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[CLONE] {repository_name}")
    print(f"        {repository_url}")

    subprocess.run(
        [
            "git",
            "clone",
            repository_url,
            str(repository_path),
        ],
        check=True,
    )

    print(f"[DONE]  {repository_name} cloned")


def get_default_branch(repository_path):
    """
    Determine the repository's default branch from origin/HEAD.
    """

    try:
        output = run_git(
            [
                "git",
                "symbolic-ref",
                "--short",
                "refs/remotes/origin/HEAD",
            ],
            cwd=repository_path,
        ).strip()

        if output.startswith("origin/"):
            return output.replace("origin/", "", 1)

        return output

    except RuntimeError:
        # Fallback to the current branch.
        return run_git(
            [
                "git",
                "rev-parse",
                "--abbrev-ref",
                "HEAD",
            ],
            cwd=repository_path,
        ).strip()


def is_source_file(path):
    """
    Determine whether a file should be included in the
    source-code dataset.
    """

    if path.suffix.lower() not in LANGUAGE_MAP:
        return False

    for part in path.parts:
        if part.lower() in EXCLUDED_DIRS:
            return False

    return True


def is_binary_file(path):
    """
    Detect binary files using a NULL-byte check.
    """

    try:
        with path.open("rb") as file:
            chunk = file.read(8192)

        return b"\x00" in chunk

    except OSError:
        return True


def is_test_file(path):
    """
    Identify likely test files using common naming conventions.
    """

    parts = [part.lower() for part in path.parts]
    filename = path.name.lower()

    if "tests" in parts:
        return True

    if "test" in parts:
        return True

    if filename.startswith("test_"):
        return True

    if filename.endswith("_test.py"):
        return True

    if filename.endswith("_test.js"):
        return True

    if filename.endswith("_test.ts"):
        return True

    return False


def count_loc(path):
    """
    Count non-empty lines of code.
    """

    try:
        with path.open(
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:
            return sum(
                1
                for line in file
                if line.strip()
            )

    except OSError:
        return 0


def normalize_path(path):
    """
    Convert paths to consistent POSIX format.
    """

    return Path(path).as_posix()


# ============================================================
# SOURCE CODE MINING
# ============================================================

def mine_source_code(repository_name, repository_path):
    """
    Mine source-code metadata from the current default branch.
    """

    records = []

    default_branch = get_default_branch(repository_path)

    print(f"[SOURCE] {repository_name}")
    print(f"         Branch: {default_branch}")

    for path in repository_path.rglob("*"):

        if not path.is_file():
            continue

        if not is_source_file(path):
            continue

        if is_binary_file(path):
            continue

        relative_path = path.relative_to(repository_path)

        relative_path_string = normalize_path(relative_path)

        file_name = path.name

        directory = normalize_path(relative_path.parent)

        if directory == ".":
            directory = ""

        extension = path.suffix.lower()

        language = LANGUAGE_MAP[extension]

        try:
            size_bytes = path.stat().st_size
        except OSError:
            size_bytes = 0

        loc = count_loc(path)

        records.append(
            {
                "repository": repository_name,
                "file_path": relative_path_string,
                "file_name": file_name,
                "directory": directory,
                "language": language,
                "extension": extension,
                "loc": loc,
                "size_bytes": size_bytes,
                "is_test_file": is_test_file(relative_path),
            }
        )

    dataframe = pd.DataFrame(records)

    if not dataframe.empty:
        dataframe = dataframe.drop_duplicates(
            subset=[
                "repository",
                "file_path",
            ]
        )

        dataframe = dataframe.sort_values(
            by="file_path"
        ).reset_index(drop=True)

    print(
        f"         Source files found: {len(dataframe)}"
    )

    return dataframe


# ============================================================
# COMMIT HISTORY MINING
# ============================================================

def mine_commit_history(repository_name, repository_path):
    """
    Mine commit history from the repository's default branch.

    Returns:
        commit_records
        file_change_records
    """

    default_branch = get_default_branch(repository_path)

    print(f"[COMMITS] {repository_name}")
    print(f"          Branch: {default_branch}")

    # --------------------------------------------------------
    # Commit header:
    #
    # HASH | DATE | AUTHOR | PARENTS | MESSAGE
    #
    # Unit separator is used to avoid problems with spaces.
    # --------------------------------------------------------

    format_string = (
        "%H%x1f%aI%x1f%an%x1f%P%x1f%s"
    )

    output = run_git(
        [
            "git",
            "log",
            default_branch,
            "--date=iso-strict",
            f"--pretty=format:{format_string}",
            "--numstat",
            "--no-renames",
        ],
        cwd=repository_path,
    )

    commit_records = []
    file_change_records = []

    current_commit = None

    header_pattern = re.compile(
        r"^[0-9a-fA-F]{40}\x1f"
    )

    def save_current_commit():
        if current_commit is None:
            return

        commit_records.append(
            {
                "repository": current_commit["repository"],
                "commit_hash": current_commit["commit_hash"],
                "date": current_commit["date"],
                "author": current_commit["author"],
                "commit_message": current_commit["commit_message"],
                "files_changed": current_commit["files_changed"],
                "additions": current_commit["additions"],
                "deletions": current_commit["deletions"],
                "is_merge_commit": current_commit[
                    "is_merge_commit"
                ],
            }
        )

    for line in output.splitlines():

        if not line.strip():
            continue

        # ----------------------------------------------------
        # New commit header
        # ----------------------------------------------------

        if header_pattern.match(line):

            save_current_commit()

            parts = line.split("\x1f", 4)

            if len(parts) != 5:
                current_commit = None
                continue

            (
                commit_hash,
                date,
                author,
                parents,
                message,
            ) = parts

            parent_list = parents.split()

            current_commit = {
                "repository": repository_name,
                "commit_hash": commit_hash,
                "date": date,
                "author": author.strip(),
                "commit_message": message.strip(),
                "files_changed": 0,
                "additions": 0,
                "deletions": 0,
                "is_merge_commit": len(parent_list) > 1,
            }

            continue

        # ----------------------------------------------------
        # File change line
        #
        # numstat format:
        #
        # additions <TAB> deletions <TAB> file_path
        # ----------------------------------------------------

        if current_commit is None:
            continue

        fields = line.split("\t", 2)

        if len(fields) != 3:
            continue

        added, deleted, file_path = fields

        file_path = file_path.strip()

        if not file_path:
            continue

        current_commit["files_changed"] += 1

        # Binary files have '-' instead of numbers.
        if added == "-":
            added_count = 0
        else:
            try:
                added_count = int(added)
            except ValueError:
                added_count = 0

        if deleted == "-":
            deleted_count = 0
        else:
            try:
                deleted_count = int(deleted)
            except ValueError:
                deleted_count = 0

        current_commit["additions"] += added_count
        current_commit["deletions"] += deleted_count

        # ----------------------------------------------------
        # Keep file-level history for the combined dataset.
        # Only source-code files are relevant here.
        # ----------------------------------------------------

        normalized_file_path = normalize_path(file_path)

        extension = Path(
            normalized_file_path
        ).suffix.lower()

        if extension in LANGUAGE_MAP:

            file_change_records.append(
                {
                    "repository": repository_name,
                    "commit_hash": current_commit[
                        "commit_hash"
                    ],
                    "date": current_commit["date"],
                    "author": current_commit["author"],
                    "file_path": normalized_file_path,
                    "additions": added_count,
                    "deletions": deleted_count,
                }
            )

    save_current_commit()

    # --------------------------------------------------------
    # Remove duplicate commits if any.
    # --------------------------------------------------------

    if commit_records:

        commit_dataframe = pd.DataFrame(
            commit_records
        )

        commit_dataframe = commit_dataframe.drop_duplicates(
            subset=[
                "repository",
                "commit_hash",
            ]
        )

        commit_dataframe = commit_dataframe.sort_values(
            by="date"
        ).reset_index(drop=True)

    else:

        commit_dataframe = pd.DataFrame(
            columns=[
                "repository",
                "commit_hash",
                "date",
                "author",
                "commit_message",
                "files_changed",
                "additions",
                "deletions",
                "is_merge_commit",
            ]
        )

    if file_change_records:

        file_change_dataframe = pd.DataFrame(
            file_change_records
        )

        file_change_dataframe = (
            file_change_dataframe
            .drop_duplicates(
                subset=[
                    "repository",
                    "commit_hash",
                    "file_path",
                ]
            )
            .reset_index(drop=True)
        )

    else:

        file_change_dataframe = pd.DataFrame(
            columns=[
                "repository",
                "commit_hash",
                "date",
                "author",
                "file_path",
                "additions",
                "deletions",
            ]
        )

    print(
        f"          Commits found: {len(commit_dataframe)}"
    )

    print(
        f"          Source file changes: "
        f"{len(file_change_dataframe)}"
    )

    return (
        commit_dataframe,
        file_change_dataframe,
    )


# ============================================================
# COMBINED DATASET
# ============================================================

def build_combined_dataset(
    source_dataframe,
    file_change_dataframe,
):
    """
    Build a logically related dataset.

    Relationship:
        repository + file_path

    Source-code metadata is joined with aggregated
    commit-history information for the same repository
    and same file path.

    This is NOT a Cartesian product.
    """

    if source_dataframe.empty:
        return pd.DataFrame()

    # --------------------------------------------------------
    # No file history available
    # --------------------------------------------------------

    if file_change_dataframe.empty:

        combined = source_dataframe.copy()

        combined["commits_touching_file"] = 0
        combined["total_additions"] = 0
        combined["total_deletions"] = 0
        combined["total_churn"] = 0
        combined["unique_authors"] = 0
        combined["first_modified_date"] = ""
        combined["last_modified_date"] = ""

        return combined

    # --------------------------------------------------------
    # Aggregate commit information by repository + file.
    # --------------------------------------------------------

    history = (
        file_change_dataframe
        .groupby(
            [
                "repository",
                "file_path",
            ],
            as_index=False,
        )
        .agg(
            commits_touching_file=(
                "commit_hash",
                "nunique",
            ),
            total_additions=(
                "additions",
                "sum",
            ),
            total_deletions=(
                "deletions",
                "sum",
            ),
            unique_authors=(
                "author",
                "nunique",
            ),
            first_modified_date=(
                "date",
                "min",
            ),
            last_modified_date=(
                "date",
                "max",
            ),
        )
    )

    # --------------------------------------------------------
    # Churn = additions + deletions
    # --------------------------------------------------------

    history["total_churn"] = (
        history["total_additions"]
        + history["total_deletions"]
    )

    # --------------------------------------------------------
    # Logical merge:
    #
    # repository + file_path
    # --------------------------------------------------------

    combined = source_dataframe.merge(
        history,
        on=[
            "repository",
            "file_path",
        ],
        how="left",
    )

    # --------------------------------------------------------
    # Files with no matching commit history
    # --------------------------------------------------------

    numeric_columns = [
        "commits_touching_file",
        "total_additions",
        "total_deletions",
        "total_churn",
        "unique_authors",
    ]

    for column in numeric_columns:
        combined[column] = (
            combined[column]
            .fillna(0)
            .astype(int)
        )

    date_columns = [
        "first_modified_date",
        "last_modified_date",
    ]

    for column in date_columns:
        combined[column] = (
            combined[column]
            .fillna("")
        )

    combined = combined.sort_values(
        by=[
            "repository",
            "file_path",
        ]
    ).reset_index(drop=True)

    return combined


# ============================================================
# CSV OUTPUT
# ============================================================

def write_csv(dataframe, path):
    """
    Clean and write a dataframe to CSV.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        path,
        index=False,
        encoding="utf-8",
    )

    print(
        f"[WRITE] {path.relative_to(BASE_DIR)}"
    )


# ============================================================
# STATISTICS
# ============================================================

def source_code_statistics(dataframe):
    """
    Generate source-code dataset statistics.
    """

    if dataframe.empty:
        return {
            "total_records": 0,
            "total_repositories": 0,
            "total_loc": 0,
            "total_size_bytes": 0,
            "languages": {},
            "extensions": {},
            "test_files": 0,
            "non_test_files": 0,
        }

    return {
        "total_records": int(len(dataframe)),

        "total_repositories": int(
            dataframe["repository"]
            .nunique()
        ),

        "total_loc": int(
            dataframe["loc"].sum()
        ),

        "total_size_bytes": int(
            dataframe["size_bytes"].sum()
        ),

        "languages": {
            str(key): int(value)
            for key, value in (
                dataframe["language"]
                .value_counts()
                .to_dict()
                .items()
            )
        },

        "extensions": {
            str(key): int(value)
            for key, value in (
                dataframe["extension"]
                .value_counts()
                .to_dict()
                .items()
            )
        },

        "test_files": int(
            dataframe["is_test_file"]
            .sum()
        ),

        "non_test_files": int(
            (~dataframe["is_test_file"])
            .sum()
        ),
    }


def commit_history_statistics(dataframe):
    """
    Generate commit-history dataset statistics.
    """

    if dataframe.empty:
        return {
            "total_records": 0,
            "total_repositories": 0,
            "total_authors": 0,
            "total_files_changed": 0,
            "total_additions": 0,
            "total_deletions": 0,
            "total_churn": 0,
            "merge_commits": 0,
            "non_merge_commits": 0,
        }

    return {
        "total_records": int(len(dataframe)),

        "total_repositories": int(
            dataframe["repository"]
            .nunique()
        ),

        "total_authors": int(
            dataframe["author"]
            .nunique()
        ),

        "total_files_changed": int(
            dataframe["files_changed"].sum()
        ),

        "total_additions": int(
            dataframe["additions"].sum()
        ),

        "total_deletions": int(
            dataframe["deletions"].sum()
        ),

        "total_churn": int(
            (
                dataframe["additions"]
                + dataframe["deletions"]
            ).sum()
        ),

        "merge_commits": int(
            dataframe["is_merge_commit"].sum()
        ),

        "non_merge_commits": int(
            (~dataframe["is_merge_commit"])
            .sum()
        ),
    }


def combined_dataset_statistics(dataframe):
    """
    Generate combined dataset statistics.
    """

    if dataframe.empty:
        return {
            "total_records": 0,
            "total_repositories": 0,
            "total_loc": 0,
            "total_churn": 0,
            "files_with_history": 0,
            "files_without_history": 0,
            "average_loc": 0,
            "average_churn": 0,
        }

    files_with_history = int(
        (
            dataframe[
                "commits_touching_file"
            ]
            > 0
        ).sum()
    )

    files_without_history = int(
        (
            dataframe[
                "commits_touching_file"
            ]
            == 0
        ).sum()
    )

    return {
        "total_records": int(len(dataframe)),

        "total_repositories": int(
            dataframe["repository"]
            .nunique()
        ),

        "total_loc": int(
            dataframe["loc"].sum()
        ),

        "total_churn": int(
            dataframe["total_churn"].sum()
        ),

        "files_with_history": files_with_history,

        "files_without_history": files_without_history,

        "average_loc": round(
            float(dataframe["loc"].mean()),
            2,
        ),

        "average_churn": round(
            float(
                dataframe["total_churn"].mean()
            ),
            2,
        ),
    }


def write_json(data, path):
    """
    Write statistics to JSON.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
        )

    print(
        f"[WRITE] {path.relative_to(BASE_DIR)}"
    )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("=" * 70)
    print("CSET456 DEVOPS LAB 2")
    print("GitHub Repository Mining and Dataset Preparation")
    print("=" * 70)
    print()

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    WORKING_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    all_source_data = []
    all_commit_data = []
    all_file_changes = []

    # ========================================================
    # PROCESS EACH REPOSITORY
    # ========================================================

    for repository_name, config in REPOSITORIES.items():

        print()
        print("-" * 70)
        print(
            f"PROCESSING: {repository_name}"
        )
        print("-" * 70)

        repository_path = (
            WORKING_DIR / repository_name
        )

        # ----------------------------------------------------
        # Clone
        # ----------------------------------------------------

        clone_repository(
            repository_name,
            config["url"],
            repository_path,
        )

        # ----------------------------------------------------
        # Source code
        # ----------------------------------------------------

        source_dataframe = mine_source_code(
            repository_name,
            repository_path,
        )

        all_source_data.append(
            source_dataframe
        )

        # ----------------------------------------------------
        # Commit history
        # ----------------------------------------------------

        (
            commit_dataframe,
            file_change_dataframe,
        ) = mine_commit_history(
            repository_name,
            repository_path,
        )

        all_commit_data.append(
            commit_dataframe
        )

        all_file_changes.append(
            file_change_dataframe
        )

    # ========================================================
    # COMBINE SOURCE DATA
    # ========================================================

    print()
    print("=" * 70)
    print("CREATING SOURCE-CODE DATASET")
    print("=" * 70)

    source_dataset = pd.concat(
        all_source_data,
        ignore_index=True,
    )

    source_dataset = source_dataset.drop_duplicates(
        subset=[
            "repository",
            "file_path",
        ]
    )

    source_dataset = source_dataset.sort_values(
        by=[
            "repository",
            "file_path",
        ]
    ).reset_index(drop=True)

    # ========================================================
    # COMBINE COMMIT DATA
    # ========================================================

    print()
    print("=" * 70)
    print("CREATING COMMIT-HISTORY DATASET")
    print("=" * 70)

    commit_dataset = pd.concat(
        all_commit_data,
        ignore_index=True,
    )

    commit_dataset = commit_dataset.drop_duplicates(
        subset=[
            "repository",
            "commit_hash",
        ]
    )

    commit_dataset = commit_dataset.sort_values(
        by=[
            "repository",
            "date",
        ]
    ).reset_index(drop=True)

    # ========================================================
    # COMBINE FILE HISTORY
    # ========================================================

    file_change_dataset = pd.concat(
        all_file_changes,
        ignore_index=True,
    )

    # ========================================================
    # BUILD LOGICAL COMBINED DATASET
    # ========================================================

    print()
    print("=" * 70)
    print("CREATING COMBINED DATASET")
    print("=" * 70)

    combined_dataset = build_combined_dataset(
        source_dataset,
        file_change_dataset,
    )

    # ========================================================
    # OUTPUT PATHS
    # ========================================================

    source_output = (
        OUTPUT_DIR
        / "source_code_dataset.csv"
    )

    commit_output = (
        OUTPUT_DIR
        / "commit_history_dataset.csv"
    )

    combined_output = (
        OUTPUT_DIR
        / "combined_dataset.csv"
    )

    # ========================================================
    # WRITE DATASETS
    # ========================================================

    print()
    print("=" * 70)
    print("WRITING DATASETS")
    print("=" * 70)

    write_csv(
        source_dataset,
        source_output,
    )

    write_csv(
        commit_dataset,
        commit_output,
    )

    write_csv(
        combined_dataset,
        combined_output,
    )

    # ========================================================
    # STATISTICS
    # ========================================================

    print()
    print("=" * 70)
    print("GENERATING STATISTICS")
    print("=" * 70)

    source_stats = source_code_statistics(
        source_dataset
    )

    commit_stats = commit_history_statistics(
        commit_dataset
    )

    combined_stats = combined_dataset_statistics(
        combined_dataset
    )

    write_json(
        source_stats,
        OUTPUT_DIR
        / "source_code_statistics.json",
    )

    write_json(
        commit_stats,
        OUTPUT_DIR
        / "commit_history_statistics.json",
    )

    write_json(
        combined_stats,
        OUTPUT_DIR
        / "combined_dataset_statistics.json",
    )

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("MINING COMPLETE")
    print("=" * 70)

    print(
        f"Repositories processed : "
        f"{len(REPOSITORIES)}"
    )

    print(
        f"Source-code records    : "
        f"{len(source_dataset)}"
    )

    print(
        f"Commit records         : "
        f"{len(commit_dataset)}"
    )

    print(
        f"Combined records       : "
        f"{len(combined_dataset)}"
    )

    print()
    print("Output directory:")
    print(OUTPUT_DIR)

    print()
    print("Generated files:")
    print("  - source_code_dataset.csv")
    print("  - commit_history_dataset.csv")
    print("  - combined_dataset.csv")
    print("  - source_code_statistics.json")
    print("  - commit_history_statistics.json")
    print("  - combined_dataset_statistics.json")

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()