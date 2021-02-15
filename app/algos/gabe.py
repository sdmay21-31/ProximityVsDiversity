

from app.models import Node

import time
import numpy as np
from app.matplot import get_plt, plot_to_uri

plt = get_plt()



def euclid_dist(t1, t2):
         return np.sqrt(((t1-t2)**2).sum())
def k_means(data, num_clust, num_iter):
    centroids = data[np.random.randint(0, data.shape[0], num_clust)]

    for n in range(num_iter): 
        assignments={}
        for ind, i in enumerate(data):
            min_dist = float('inf') 
            closest_clust = None
            for c_ind, j in enumerate(centroids):
                dist = euclid_dist(i, j) 
                if dist < min_dist:
                   min_dist = dist
                   closest_clust = c_ind

            if closest_clust in assignments: 
                assignments[closest_clust].append(ind)
            else:
                assignments[closest_clust]=[] 
                assignments[closest_clust].append(ind)

        for key in assignments:
            clust_sum = 0
            for k in assignments[key]: 
                clust_sum = clust_sum + data[k]
            centroids[key] = [m / len(assignments[key]) for m in clust_sum] 

    return centroids


def run(values):
    n = 100 
    ts_len = 50

    phases = np.array(np.random.randint(0, 50, [n, 2]))
    pure = np.sin([np.linspace(-np.pi * x[0], -np.pi * x[1], ts_len) for x in phases])
    noise = np.array([np.random.normal(0, 1, ts_len) for x in range(n)])

    signals = pure * noise
               
    # Normalize everything between 0 and 1
    signals += np.abs(np.min(signals))
    signals /= np.max(signals)

    plt.plot(signals[0])
    centroids = k_means(signals, 100, 100)
    return (plot_to_uri(plt), centroids)