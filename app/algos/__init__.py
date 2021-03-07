from app.models import Node
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import numpy as np

from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def run(method='kmeans', proximity=[], diversity=[]):
    if not len(proximity) and not len(diversity):
        raise ValueError("Attributes required")

    if len(proximity) + len(diversity) > 3:
        raise ValueError("Attributes must be less than 3")

        