"""PDF reporting utilities."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
from jinja2 import Environment, FileSystemLoader, Template
from weasyprint import HTML


def _build_html(df: pd.DataFrame) -> str:
    """Render HTML using a very small inline template."""
    age_bins = (df["age"] // 5) * 5
    summary = df.assign(age_band=age_bins).groupby("age_band")["gross_premium"].sum()
    env = Environment(autoescape=True)
    template = Template(
        """
        <h1>Premium Summary</h1>
        <table border="1" cellspacing="0" cellpadding="4">
            <tr><th>Age Band</th><th>Total Gross Premium</th></tr>
            {% for band, total in summary.items() %}
            <tr><td>{{ band }}-{{ band + 4 }}</td><td>{{ '{:.2f}'.format(total) }}</td></tr>
            {% endfor %}
        </table>
        """
    )
    return template.render(summary=summary)


def generate_pdf(df: pd.DataFrame, output_path: Path | str) -> None:
    """Generate a PDF summary report."""
    html = _build_html(df)
    HTML(string=html).write_pdf(str(output_path))
