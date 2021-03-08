from .algo import Algo
import numpy as np
from app.matplot import get_plt

from app.models import Node
from sklearn.cluster import KMeans

class DummyAlgo(Algo):
    @property
    def name(self):
        return "Dummy Algo"

    @property
    def extra(self):
        return "Dummy algorithm to get things moving."

    def initialize(self):
        self.nodes = np.array([
            n for n in Node.objects.values_list(*self.attributes)[:3000]
        ])

    def process(self):
        kmeans = KMeans(n_clusters=4)
        kmeans.fit(self.nodes)
        self.kmeans = kmeans
        self.y_kmeans = kmeans.predict(self.nodes)
        self.centers = kmeans.cluster_centers_

    def get_plot(self):
        plt = get_plt()

        plt.scatter(self.nodes[:, 0], self.nodes[:, 1], c=self.y_kmeans, s=50, cmap='viridis')
        plt.scatter(self.centers[:, 0], self.centers[:, 1], c='black', s=200, alpha=0.5)

        return plt
    
        