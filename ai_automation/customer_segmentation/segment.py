import sys
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Simple pipeline for customer segmentation using K-Means.

if len(sys.argv) < 2:
    print("Usage: python segment.py <transactions_csv>")
    sys.exit(1)

csv_path = sys.argv[1]

df = pd.read_csv(csv_path)

features = df[["total_spent", "frequency", "recency"]]
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

kmeans = KMeans(n_clusters=4, random_state=0)
labels = kmeans.fit_predict(scaled)

df["segment"] = labels

profiles = df.groupby("segment")[["total_spent", "frequency", "recency"]].mean()
profiles.to_csv("segment_profiles.csv")

plt.figure(figsize=(8, 6))
scatter = plt.scatter(df["total_spent"], df["recency"], c=df["segment"], cmap="viridis")
plt.xlabel("Total Spent")
plt.ylabel("Recency")
plt.title("Customer Segments")
plt.colorbar(scatter, label="Segment")
plt.tight_layout()
plt.savefig("segments_scatter.png")
