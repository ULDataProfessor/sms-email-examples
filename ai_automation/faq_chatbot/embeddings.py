"""FAQ indexing utilities using sentence-transformers."""

from pathlib import Path
from typing import List, Dict

import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

MODEL_NAME = "all-MiniLM-L6-v2"
SIM_THRESHOLD = 0.5

class FAQIndexer:
    """Load FAQs and perform similarity search."""

    def __init__(self, csv_path: str = "faq.csv", model_name: str = MODEL_NAME):
        csv_file = Path(__file__).resolve().parent / csv_path
        self.df = pd.read_csv(csv_file)
        self.questions = self.df["question"].fillna("").tolist()
        self.answers = self.df["answer"].fillna("").tolist()
        self.model = SentenceTransformer(model_name)
        self.embeddings = self.model.encode(self.questions, convert_to_tensor=True)

    def query(self, text: str, top_k: int = 3) -> List[Dict[str, str]]:
        """Return the most similar FAQs above the similarity threshold."""
        query_emb = self.model.encode(text, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, self.embeddings)[0]
        k = min(top_k, len(self.questions))
        best_scores, best_idx = torch.topk(scores, k=k)
        results = []
        for score, idx in zip(best_scores, best_idx):
            if score.item() >= SIM_THRESHOLD:
                results.append(
                    {
                        "question": self.questions[idx],
                        "answer": self.answers[idx],
                        "score": float(score.item()),
                    }
                )
        return results
