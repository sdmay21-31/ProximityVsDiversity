from app.models import Node
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

from django.core.cache import cache

def example_algo():
    """ Return the mass_1 of example_query nodes """
    nodes = Node.objects.example_query()
    masses = [node.mass_1 for node in nodes]
    return masses


def get_elbow_cache_key(node_keys: list):
    """Given a list of string return a unique cache key"""
    return "elb_{}".format(hash(''.join(node_keys)))

# Help from: https://realpython.com/k-means-clustering-python/
def get_number_of_clusters(node_keys=['mass0_1', 'lumin_1']):
    """ Uses the elbow method to determine the best number of clusters for given data"""
    # Check if elbow for node_keys exists
    key = get_elbow_cache_key(node_keys)
    elbow = cache.get(key)
    if elbow:
        return elbow
    # Find the new elbow
    features = Node.objects.values_list(*node_keys)
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

    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)
    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
    # Add this elbow to cache
    cache.set(key, kl.elbow, None)
    return kl.elbow
