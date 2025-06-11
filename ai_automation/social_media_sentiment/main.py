import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import tweepy
import openai


def fetch_tweets(hashtag: str, max_results: int = 50) -> list[dict]:
    """Fetch recent tweets containing the given hashtag."""
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
    if not bearer_token:
        raise EnvironmentError("TWITTER_BEARER_TOKEN environment variable not set")

    client = tweepy.Client(bearer_token=bearer_token)
    # search_recent_tweets returns Tweet objects. request fields: author_id, created_at, lang
    response = client.search_recent_tweets(
        query=f"#{hashtag} -is:retweet",  # exclude retweets
        tweet_fields=["created_at", "lang", "author_id"],
        max_results=max_results,
    )
    tweets = response.data or []
    tweet_dicts = [tweet.data for tweet in tweets]
    return tweet_dicts


def tweets_to_dataframe(tweet_dicts: list[dict]) -> pd.DataFrame:
    """Convert raw tweet dictionaries to a DataFrame."""
    df = pd.DataFrame(tweet_dicts)
    df.rename(
        columns={"created_at": "timestamp", "author_id": "user", "lang": "language"},
        inplace=True,
    )
    df = df[["timestamp", "user", "text", "language"]]
    return df


def classify_sentiments(df: pd.DataFrame) -> pd.DataFrame:
    """Call OpenAI to classify sentiment for each tweet."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable not set")

    sentiments = []
    for text in df["text"]:
        messages = [
            {
                "role": "system",
                "content": "You are a sentiment classifier that responds with just one word: positive, neutral, or negative.",
            },
            {"role": "user", "content": text[:500]},
        ]
        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        sentiment = response.choices[0].message["content"].strip().lower()
        sentiments.append(sentiment)

    df = df.copy()
    df["sentiment"] = sentiments
    return df


def aggregate_by_hour(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment counts per hour."""
    df["hour"] = df["timestamp"].apply(lambda t: t.replace(minute=0, second=0, microsecond=0))
    agg = df.groupby(["hour", "sentiment"]).size().unstack(fill_value=0)
    agg = agg.sort_index()
    return agg


def plot_sentiment_over_time(agg: pd.DataFrame, output_path: str) -> None:
    agg.plot(kind="line")
    plt.xlabel("Hour")
    plt.ylabel("Tweet count")
    plt.title("Tweet Sentiment Over Time")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main():
    hashtag = os.getenv("HASHTAG", "python")
    tweets = fetch_tweets(hashtag)
    df = tweets_to_dataframe(tweets)
    df = classify_sentiments(df)
    agg = aggregate_by_hour(df)

    # export results
    df.to_csv("tweets_detailed.csv", index=False)
    agg.to_csv("tweets_aggregated.csv")
    plot_sentiment_over_time(agg, "sentiment_over_time.png")
    print("Detailed results -> tweets_detailed.csv")
    print("Aggregated results -> tweets_aggregated.csv")
    print("Chart -> sentiment_over_time.png")


if __name__ == "__main__":
    main()
