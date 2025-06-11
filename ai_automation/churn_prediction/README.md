# Churn Prediction Pipeline

This example demonstrates a simple machine learning pipeline to predict whether a customer will churn.

## Files

- `train.py` – trains a `RandomForestClassifier` on historical customer data.
- `predict.py` – loads a saved model and scores new customers.
- `requirements.txt` – Python dependencies.

## Data Wrangling & Feature Engineering

The training CSV should contain columns like `user_id`, `tenure`, `usage_metrics`, `support_calls`, and `churn_flag`.
The script drops the `user_id` column, one‑hot encodes any categorical features, and standardizes numerical values. The processed features are fed into the classifier.

## Model Selection

A RandomForest classifier was chosen because it handles mixed data types well and requires little tuning to achieve good baseline performance.

## Training & Evaluation

```bash
pip install -r requirements.txt
python train.py path/to/customers.csv model.joblib
```

The script splits the data into train and test sets, fits the model, and prints accuracy, ROC‑AUC, and a classification report. The trained pipeline is saved with `joblib`.

## Scoring New Data

```bash
python predict.py model.joblib new_customers.csv predictions.csv
```

`predict.py` outputs a CSV with the predicted label and probability for each new customer.
