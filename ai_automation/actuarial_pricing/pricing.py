"""Premium calculation utilities."""

from __future__ import annotations

import pandas as pd
import numpy as np

from .config import interest_rate, expense_loading, profit_loading
from .utils import PricingError


def lookup_q(age: int, mortality_table: pd.DataFrame) -> float:
    """Return mortality rate q_x for given age."""
    try:
        return float(mortality_table.loc[age, "q_x"])
    except KeyError as exc:
        raise PricingError(f"No mortality rate for age {age}") from exc


def net_premium(age: int, sum_insured: float, term: int, mortality_table: pd.DataFrame) -> float:
    """Calculate net premium using simple actuarial present value formula."""
    v = 1 / (1 + interest_rate)
    premiums = []
    for t in range(1, term + 1):
        q = lookup_q(age + t - 1, mortality_table)
        premiums.append(q * v**t)
    return sum_insured * float(np.sum(premiums))


def gross_premium(net: float) -> float:
    """Apply expense and profit loadings to net premium."""
    loading_factor = 1 + expense_loading + profit_loading
    return net * loading_factor


def price_policies(
    policies: pd.DataFrame,
    mortality_table: pd.DataFrame,
) -> pd.DataFrame:
    """Return premiums for each policy."""
    results = []
    for _, row in policies.iterrows():
        net = net_premium(
            age=int(row["age"]),
            sum_insured=float(row["sum_insured"]),
            term=int(row["coverage_term_years"]),
            mortality_table=mortality_table,
        )
        gross = gross_premium(net)
        results.append(
            {
                "policy_id": row["policy_id"],
                "net_premium": net,
                "gross_premium": gross,
            }
        )
    return pd.DataFrame(results)
