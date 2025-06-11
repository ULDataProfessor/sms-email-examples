# 🗺️ Geospatial Analysis Example

This folder demonstrates basic catchment analysis for retail stores. It loads a
list of store locations and customer addresses, converts the addresses to
coordinates, clusters the customer points and produces an interactive map of the
result.

## Files
- `analyze.py` – command line script that performs the clustering and map
  generation.
- `map_utils.py` – helper functions to build the Folium map.
- `requirements.txt` – required Python packages.

## Clustering Algorithm
DBSCAN is used by default because it groups nearby points without requiring a
predefined number of clusters and works well with irregular shapes. K-Means can
be selected with `--algorithm kmeans` if you prefer a fixed number of clusters.

Adjust the clustering distance for DBSCAN with `--eps` (in kilometres) or set
`--clusters` when using K-Means.

## Viewing the Map
Run the script and open the generated `map.html` file in any web browser. Share
the HTML file directly to allow others to view the interactive map.
