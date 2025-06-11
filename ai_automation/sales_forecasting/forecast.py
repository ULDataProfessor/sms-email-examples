import argparse
from pathlib import Path
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt


def load_data(csv_path: Path, store_id: int | None = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    if store_id is not None:
        df = df[df['store_id'] == store_id]
    df = df.sort_values('date')
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    return df


def train_test_split(df: pd.DataFrame, holdout_days: int = 30):
    train = df.iloc[:-holdout_days]
    holdout = df.iloc[-holdout_days:]
    return train, holdout


def train_prophet(train: pd.DataFrame) -> Prophet:
    model = Prophet()
    model.add_regressor('day_of_week')
    model.add_regressor('month')
    model.fit(train.rename(columns={'date': 'ds', 'sales': 'y'}))
    return model


def forecast(model: Prophet, df: pd.DataFrame, periods: int = 30) -> pd.DataFrame:
    future = model.make_future_dataframe(periods=periods)
    future['day_of_week'] = future['ds'].dt.dayofweek
    future['month'] = future['ds'].dt.month
    forecast = model.predict(future)
    return forecast


def evaluate(holdout: pd.DataFrame, forecast_df: pd.DataFrame) -> tuple[float, float]:
    merged = holdout.merge(forecast_df[['ds', 'yhat']], left_on='date', right_on='ds')
    errors = (merged['sales'] - merged['yhat']).abs()
    mae = errors.mean()
    mape = (errors / merged['sales']).mean() * 100
    return mae, mape


def plot_forecast(df: pd.DataFrame, forecast_df: pd.DataFrame, output: Path | None = None):
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['sales'], label='Historical')
    plt.plot(forecast_df['ds'], forecast_df['yhat'], label='Forecast')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.legend()
    if output:
        plt.savefig(output)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Forecast sales for the next 30 days")
    parser.add_argument('csv', type=Path, help='Path to sales CSV')
    parser.add_argument('--store-id', type=int, help='Store ID to filter')
    parser.add_argument('--plot', type=Path, help='Path to save the plot (PNG)')
    args = parser.parse_args()

    df = load_data(args.csv, args.store_id)
    train, holdout = train_test_split(df)
    model = train_prophet(train)
    forecast_df = forecast(model, df, periods=30)

    mae, mape = evaluate(holdout, forecast_df)
    print(f"MAE: {mae:.2f}")
    print(f"MAPE: {mape:.2f}%")

    plot_forecast(df, forecast_df, args.plot)


if __name__ == '__main__':
    main()
