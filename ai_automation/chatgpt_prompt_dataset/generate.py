"""Generate a prompt/response dataset from business scenarios."""

import os
import sys
import pandas as pd
import openai

from utils import build_payload, chat_completion_with_retry


def main(input_csv: str, output_csv: str) -> None:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")

    scenarios = pd.read_csv(input_csv)
    records = []

    for _, row in scenarios.iterrows():
        description = row.get("description", "")
        scenario_id = row.get("scenario_id")
        payload = build_payload(description)
        response = chat_completion_with_retry(payload)
        message = response.choices[0].message["content"].strip()
        tokens = response.usage.total_tokens if getattr(response, "usage", None) else None
        records.append({
            "scenario_id": scenario_id,
            "prompt": description,
            "response": message,
            "tokens_used": tokens,
        })

    pd.DataFrame(records).to_csv(output_csv, index=False)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python generate.py <input_csv> <output_csv>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
