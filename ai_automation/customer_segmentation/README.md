# Customer Segmentation with K-Means

This example groups customers based on their transaction history. Clustering lets you discover natural segments in the data without labels.

## Why clustering?
- Segments reveal patterns in spending, purchase frequency and recency.
- Targeted marketing is easier when customers are grouped by behavior.

## Interpreting clusters
- Each cluster centroid represents the average customer in that group.
- Higher or lower values in the centroid show how that segment differs from the overall population.

## Usage
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the script with your transaction CSV:
   ```bash
   python segment.py transactions.csv
   ```
   This creates `segment_profiles.csv` and `segments_scatter.png` in the current directory.
3. Open `segment_profiles.csv` to view average spend, frequency and recency for each segment. The scatter plot visualizes two dimensions colored by segment.
