# Recommendation Engine

This folder contains a minimal example of building a collaborative filtering recommendation engine and exposing it through a FastAPI service.

## Data Wrangling

The service expects a CSV file with `user_id`, `product_id` and `rating` columns. The data is loaded into a pandas `DataFrame` and transformed into the internal format expected by the `surprise` library. Ratings are converted into a user–item matrix using pandas and SciPy's sparse structures under the hood when `surprise` builds the training set.

## Recommendation Algorithm

A matrix factorization model (Surprise's `SVD`) is trained on the full interaction dataset. For a requested user, the model scores every product the user has not rated and returns the top results with the highest predicted rating.

## Running the Server

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare `user_product_interactions.csv` in this folder (or provide a path via the `/train` endpoint).
3. Start the API server:
   ```bash
   uvicorn app:app --reload
   ```
4. Endpoints:
   - `POST /train` – Body `{ "csv_path": "optional/path.csv" }` retrains the model on the given CSV.
   - `GET /recommend/{user_id}` – Returns the top‑10 `product_id` values recommended for that user.
