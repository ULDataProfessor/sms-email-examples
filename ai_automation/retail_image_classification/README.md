# Retail Image Classification

This package demonstrates how to enrich a folder of product images with labels
from AWS Rekognition and store the results in a SQLite database.

## Directory Layout

```
retail_image_classification/
├── retail_image_classification/  # Python package
│   ├── __init__.py
│   ├── db.py                # Database helpers
│   └── processor.py         # Image processing logic
├── scripts/
│   ├── classify_images.py   # Build or update the database
│   └── query_labels.py      # Query images by label
└── requirements.txt
```

The database `labels.db` (default name) contains a single table `image_labels`
with columns:
- `filename` – image file name
- `label` – detected label
- `confidence` – confidence score returned by Rekognition

## Processing Images

The script `classify_images.py` scans a folder, sends each image to AWS
Rekognition and transforms the response into a DataFrame with columns
`filename`, `label`, `confidence`. Records below the specified confidence
threshold are dropped. The remaining data is appended to the SQLite database.

Adjust the confidence filter using the `--min_confidence` option when running
the script.

Example:

```bash
python scripts/classify_images.py /path/to/images --db labels.db --min_confidence 80
```

## Querying the Database

Use `query_labels.py` to list all images that contain a given label above a
confidence threshold (90% by default).

```bash
python scripts/query_labels.py "Shoe" --min_confidence 90 --db labels.db
```

Example output:

```
product1.jpg (95.2%)
product2.jpg (91.7%)
```

## Notes

- AWS credentials must be configured for `boto3` (environment variables or AWS
  config files).
- The scripts can be run independently; `classify_images.py` must be executed
  before querying so the database is populated.
