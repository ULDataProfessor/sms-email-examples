"""CSV ingestion helpers."""

from pathlib import Path
import pandas as pd

from .utils import DataLoadError


POLICY_COLS = [
    "policy_id",
    "age",
    "gender",
    "sum_insured",
    "smoker_flag",
    "coverage_term_years",
]

MORTALITY_COLS = ["age", "q_x"]


def load_policyholders(csv_path: Path | str) -> pd.DataFrame:
    """Load policyholder profiles from a CSV file."""
    try:
        df = pd.read_csv(csv_path, usecols=POLICY_COLS)
    except Exception as exc:  # broad catch to wrap errors
        raise DataLoadError(f"Could not load policyholder data: {exc}") from exc
    return df


def load_mortality_table(csv_path: Path | str) -> pd.DataFrame:
    """Load mortality table CSV."""
    try:
        df = pd.read_csv(csv_path, usecols=MORTALITY_COLS)
    except Exception as exc:
        raise DataLoadError(f"Could not load mortality table: {exc}") from exc
    return df.set_index("age")
