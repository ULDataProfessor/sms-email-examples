from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from model import RecommendationModel

CSV_PATH = "user_product_interactions.csv"

app = FastAPI()
model = RecommendationModel(CSV_PATH)


class TrainRequest(BaseModel):
    csv_path: str | None = None


@app.post("/train")
def train(data: TrainRequest):
    if data.csv_path:
        model.csv_path = data.csv_path
    try:
        model.train()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"status": "trained"}


@app.get("/recommend/{user_id}")
def recommend(user_id: str):
    try:
        recs = model.recommend(user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"user_id": user_id, "product_ids": recs}
