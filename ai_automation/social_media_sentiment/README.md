# Social Media Sentiment Analysis

This example demonstrates a small pipeline that collects tweets containing a specific hashtag and classifies each tweet's sentiment using the OpenAI API. The results are exported as CSV files and visualized with a simple line chart.

## Files

- `main.py` – Fetches tweets with Tweepy, transforms them into a DataFrame, calls OpenAI to determine sentiment, aggregates by hour, and exports the results.
- `requirements.txt` – Python dependencies.

## Pipeline Overview

1. **Data Ingestion** – `fetch_tweets()` uses Tweepy and your Twitter API bearer token to pull recent tweets matching a hashtag. Retweets are filtered out.
2. **Transformation** – `tweets_to_dataframe()` creates a pandas DataFrame with columns `timestamp`, `user`, `text`, and `language`.
3. **Sentiment Classification** – `classify_sentiments()` sends each tweet's text to the OpenAI ChatCompletion API, returning `positive`, `neutral`, or `negative`.
4. **Aggregation** – `aggregate_by_hour()` groups the labeled tweets by hour and sentiment, producing a table of counts.
5. **Output** – The script saves `tweets_detailed.csv` (all tweets with sentiment) and `tweets_aggregated.csv` (hourly counts). `plot_sentiment_over_time()` generates `sentiment_over_time.png` showing sentiment trends.

### Pandas Transformations

- Rename columns from Tweepy (`created_at` → `timestamp`, `author_id` → `user`, `lang` → `language`).
- Select only the relevant columns.
- Add a `sentiment` column from the OpenAI response.
- Create an hourly `hour` column for grouping.
- Use `groupby` and `unstack` to compute counts of each sentiment per hour.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `TWITTER_BEARER_TOKEN` – Twitter API bearer token.
   - `OPENAI_API_KEY` – Your OpenAI API key.
   - Optional: `HASHTAG` – Hashtag to search (defaults to `python`).
3. Run the script:
   ```bash
   python main.py
   ```
4. Examine `tweets_detailed.csv`, `tweets_aggregated.csv`, and the generated `sentiment_over_time.png` line chart. The chart's x‑axis represents hourly buckets and the y‑axis shows tweet counts by sentiment.
