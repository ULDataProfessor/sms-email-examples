"""Restaurant AI pipeline demonstration."""

import re
from typing import List

def ingest_data() -> List[str]:
    """Collect review lines from the user."""
    print("Enter reviews (blank line to finish):")
    reviews = []
    while True:
        line = input()
        if not line:
            break
        reviews.append(line)
    return reviews

def analyze_data(reviews: List[str]) -> float:
    """Simple keyword sentiment score."""
    positive = {"good", "great", "amazing", "excellent", "love"}
    negative = {"bad", "terrible", "awful", "hate", "poor"}
    score = 0
    for review in reviews:
        tokens = re.findall(r"\w+", review.lower())
        for token in tokens:
            if token in positive:
                score += 1
            elif token in negative:
                score -= 1
    return score / len(reviews) if reviews else 0.0

def process_data(score: float) -> str:
    """Turn numeric score into a text summary."""
    if score > 0:
        return "Positive overall sentiment"
    if score < 0:
        return "Negative overall sentiment"
    return "Neutral sentiment"

def output_results(summary: str) -> None:
    print(f"Summary: {summary}")

def main() -> None:
    reviews = ingest_data()
    score = analyze_data(reviews)
    summary = process_data(score)
    output_results(summary)

if __name__ == "__main__":
    main()
