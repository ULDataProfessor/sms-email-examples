"""Geospatial clustering for store catchment analysis."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from sklearn.cluster import DBSCAN, KMeans
import numpy as np

from . import map_utils


def load_store_locations(path: Path) -> pd.DataFrame:
    """Load store locations from a CSV file with columns id,latitude,longitude."""
    return pd.read_csv(path)


def load_customer_addresses(path: Path) -> pd.DataFrame:
    """Load customer addresses from a CSV file with columns id,address."""
    return pd.read_csv(path)


def geocode_addresses(df: pd.DataFrame, address_col: str = "address") -> pd.DataFrame:
    """Geocode addresses in the DataFrame using OpenStreetMap Nominatim."""
    geolocator = Nominatim(user_agent="geo_analysis")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    lats: list[float] = []
    lons: list[float] = []
    for addr in df[address_col]:
        location = geocode(addr)
        if location:
            lats.append(location.latitude)
            lons.append(location.longitude)
        else:
            lats.append(np.nan)
            lons.append(np.nan)
    df = df.copy()
    df["latitude"] = lats
    df["longitude"] = lons
    df.dropna(subset=["latitude", "longitude"], inplace=True)
    return df


def cluster_customers(coords: np.ndarray, algorithm: str = "dbscan", eps_km: float = 1.0, n_clusters: int = 5) -> np.ndarray:
    """Cluster coordinates using DBSCAN or KMeans."""
    if algorithm == "dbscan":
        # Convert eps from kilometers to radians for haversine metric
        kms_per_radian = 6371.0088
        db = DBSCAN(eps=eps_km / kms_per_radian, min_samples=3, metric="haversine")
        labels = db.fit_predict(np.radians(coords))
    else:
        km = KMeans(n_clusters=n_clusters, random_state=42)
        labels = km.fit_predict(coords)
    return labels


def assign_to_nearest_store(customer_coords: np.ndarray, store_coords: np.ndarray) -> np.ndarray:
    """Return index of nearest store for each customer."""
    from sklearn.metrics.pairwise import haversine_distances

    cust_rad = np.radians(customer_coords)
    store_rad = np.radians(store_coords)
    dist = haversine_distances(cust_rad, store_rad)
    return np.argmin(dist, axis=1)


def export_statistics(labels: np.ndarray, store_ids: Iterable, assignment: np.ndarray, output: Path) -> None:
    """Export customer count per store."""
    df = pd.DataFrame({"store_id": [store_ids[idx] for idx in assignment]})
    stats = df.value_counts("store_id").rename("customer_count").reset_index()
    stats.to_csv(output, index=False)


def main(argv: Iterable[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Cluster customer locations and create map")
    parser.add_argument("stores", type=Path, help="CSV of store id,latitude,longitude")
    parser.add_argument("customers", type=Path, help="CSV of customer id,address")
    parser.add_argument("--algorithm", choices=["dbscan", "kmeans"], default="dbscan")
    parser.add_argument("--eps", type=float, default=1.0, help="DBSCAN epsilon in km")
    parser.add_argument("--clusters", type=int, default=5, help="Number of clusters for k-means")
    parser.add_argument("--map", type=Path, default=Path("map.html"), help="Output HTML map path")
    parser.add_argument("--stats", type=Path, default=Path("cluster_stats.csv"), help="Output CSV stats path")
    args = parser.parse_args(argv)

    stores = load_store_locations(args.stores)
    customers = load_customer_addresses(args.customers)
    customers = geocode_addresses(customers)

    coords = customers[["latitude", "longitude"]].to_numpy()
    labels = cluster_customers(coords, args.algorithm, args.eps, args.clusters)

    store_coords = stores[["latitude", "longitude"]].to_numpy()
    assignment = assign_to_nearest_store(coords, store_coords)

    export_statistics(labels, stores["id"], assignment, args.stats)

    m = map_utils.create_cluster_map(stores, customers, labels)
    m.save(args.map)
    print(f"Map saved to {args.map}\nStats saved to {args.stats}")


if __name__ == "__main__":
    main()
