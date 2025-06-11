import pandas as pd
from surprise import Dataset, Reader, SVD


class RecommendationModel:
    """Simple wrapper around Surprise's SVD algorithm."""

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df: pd.DataFrame | None = None
        self.model: SVD | None = None

    def load_data(self) -> pd.DataFrame:
        self.df = pd.read_csv(self.csv_path)
        return self.df

    def train(self) -> None:
        self.load_data()
        if self.df is None:
            raise ValueError("No data loaded")
        rating_scale = (self.df.rating.min(), self.df.rating.max())
        reader = Reader(rating_scale=rating_scale)
        data = Dataset.load_from_df(
            self.df[["user_id", "product_id", "rating"]], reader
        )
        trainset = data.build_full_trainset()
        self.model = SVD()
        self.model.fit(trainset)

    def recommend(self, user_id: str, n: int = 10) -> list[str]:
        if self.model is None or self.df is None:
            raise ValueError("Model has not been trained")
        all_items = self.df["product_id"].unique()
        rated = self.df[self.df["user_id"] == user_id]["product_id"].unique()
        candidates = [iid for iid in all_items if iid not in rated]
        scored = [
            (iid, self.model.predict(str(user_id), str(iid)).est) for iid in candidates
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return [iid for iid, _ in scored[:n]]
