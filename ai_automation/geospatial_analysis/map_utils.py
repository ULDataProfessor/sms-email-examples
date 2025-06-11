"""Utilities for building Folium maps of store clusters."""

from __future__ import annotations

import numpy as np
import pandas as pd
import folium


COLORS = [
    "red",
    "green",
    "purple",
    "orange",
    "blue",
    "cadetblue",
    "darkred",
    "lightgreen",
    "darkblue",
    "pink",
]


def create_cluster_map(stores: pd.DataFrame, customers: pd.DataFrame, labels: np.ndarray) -> folium.Map:
    """Return a Folium map with store markers and clustered customers."""
    if not customers.empty:
        center = [customers["latitude"].mean(), customers["longitude"].mean()]
    else:
        center = [stores["latitude"].mean(), stores["longitude"].mean()]

    m = folium.Map(location=center, zoom_start=12)

    for _, row in stores.iterrows():
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=str(row.get("id", "store")),
            icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa"),
        ).add_to(m)

    for label in np.unique(labels):
        cluster = customers[labels == label]
        color = COLORS[label % len(COLORS)] if label >= 0 else "lightgray"
        for _, c in cluster.iterrows():
            folium.CircleMarker(
                [c["latitude"], c["longitude"]], radius=3, color=color, fill=True, fill_opacity=0.7
            ).add_to(m)
        if label >= 0 and len(cluster) > 2:
            coords = cluster[["latitude", "longitude"]].values
            min_lat, min_lon = coords.min(axis=0)
            max_lat, max_lon = coords.max(axis=0)
            folium.Rectangle(
                [[min_lat, min_lon], [max_lat, max_lon]], color=color, weight=2, fill=False
            ).add_to(m)
    return m
