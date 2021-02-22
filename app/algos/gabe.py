from app.models import Node
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

# mass0_1
# lumin_1
def run(*args):
    features, true_labels = make_blobs(
        n_samples=200,
        centers=3,
        cluster_std=2.75,
        random_state=42
    )
    features = Node.objects.values_list('mass0_1', 'lumin_1')
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(
        init="random",
        n_clusters=3,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)
        plt.style.use("fivethirtyeight")
    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
    print(kl.elbow)
