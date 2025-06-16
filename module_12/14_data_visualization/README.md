# Data Visualization

## Project Overview
`create_chart.py` reads a CSV file and generates a bar chart using matplotlib. It demonstrates quickly visualizing tabular data with minimal code.

## Variables
`DATA_FILE` is the path to the CSV. It should contain columns `category` and `value` which will be plotted.

## Instructions
Install `matplotlib` and `pandas` with `pip install matplotlib pandas`. Place your data in `data.csv` or update `DATA_FILE` in the script. Run `python create_chart.py` to produce `chart.png`.

## Explanation
The script loads the CSV into a DataFrame, groups values by category and plots the result as a bar chart. Saving to an image file allows sharing the graphic without displaying a GUI window.
