"""CLI for transaction anomaly detection pipeline."""

from pathlib import Path
from typing import Optional

import click
import pandas as pd

from . import utils


@click.command()
@click.option("--mode", type=click.Choice(["batch", "stream"]), default="batch", help="Processing mode")
@click.option("--input", "input_csv", required=True, help="CSV of transactions to process")
@click.option("--history", type=click.Path(), help="Historical CSV for stream mode")
@click.option("--output", default="anomaly_report.csv", help="Path for flagged transaction report")
@click.option("--contamination", default=0.01, show_default=True, help="IsolationForest contamination")
def main(mode: str, input_csv: str, history: Optional[str], output: str, contamination: float) -> None:
    """Run the detection pipeline."""
    new_df = utils.load_transactions(input_csv)

    if mode == "stream" and history:
        hist_df = utils.load_transactions(history)
        combined = pd.concat([hist_df, new_df], ignore_index=True)
        combined = utils.feature_engineering(combined)
        combined, _ = utils.detect_anomalies(combined, contamination=contamination)
        new_processed = combined.iloc[len(hist_df) :].copy()
        flagged = new_processed[new_processed["anomaly"]]
    else:
        df = utils.feature_engineering(new_df)
        df, _ = utils.detect_anomalies(df, contamination=contamination)
        flagged = df[df["anomaly"]]

    flagged.to_csv(output, index=False)

    summary = flagged["amount"].describe()
    summary_path = str(Path(output).with_name(Path(output).stem + "_summary.csv"))
    summary.to_csv(summary_path)

    click.echo(f"Flagged {len(flagged)} transactions. Summary saved to {summary_path}.")


if __name__ == "__main__":
    main()
