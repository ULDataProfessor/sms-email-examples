# Actuarial Pricing Example

This package demonstrates a very small actuarial pricing workflow. It loads
policyholder profiles and a mortality table, prices each policy using a simple
present value formula and outputs a PDF summary report.

## Data

Two CSV files are required:

1. **Policyholder profiles** – columns
   `policy_id`, `age`, `gender`, `sum_insured`, `smoker_flag`,
   `coverage_term_years`.
2. **Mortality table** – columns `age`, `q_x` where `q_x` is the mortality rate
   for that age. Any standard table may be used.

The example assumes the interest rate and loading percentages defined in
`config.py`. Adjust these values as needed.

## Usage

Install dependencies and run the pricing workflow:

```bash
pip install -r requirements.txt
```

```python
import pandas as pd
from actuarial_pricing import load_data, pricing, report
from actuarial_pricing.config import interest_rate, expense_loading, profit_loading

policies = load_data.load_policyholders("policyholders.csv")
mort_table = load_data.load_mortality_table("mortality.csv")

priced = pricing.price_policies(policies, mort_table)
priced.to_csv("priced_policies.csv", index=False)

report.generate_pdf(priced.join(policies[["age"]]), "premium_report.pdf")
```

The resulting PDF shows total gross premium by 5‑year age bands.
Modify the values in `config.py` to change the interest rate or loadings.
