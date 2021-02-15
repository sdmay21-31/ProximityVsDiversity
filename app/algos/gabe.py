

from app.models import Node

import time
import numpy as np
from app.matplot import get_plt, plot_to_uri


"""Major help from

https://blog.newrelic.com/product-news/optimizing-k-means-clustering/
"""


def euclid_dist(t1, t2):
         return np.sqrt(((t1-t2)**2).sum())
def k_means(data, num_clust, num_iter):
    centroids = data[np.random.randint(0, data.shape[0], num_clust)]
    # How many times we want to run kmeans
    for n in range(num_iter): 
        print('Iteration ' + str(n))
        assignments={}
        for index, i_node in enumerate(data):
            min_dist = float('inf') 
            closest_clust = None
            for c_index, j_node in enumerate(centroids):
                dist = euclid_dist(i_node, j_node) 
                if dist < min_dist:
                   min_dist = dist
                   closest_clust = c_index

            if closest_clust in assignments: 
                assignments[closest_clust].append(index)
            else:
                assignments[closest_clust]=[] 
                assignments[closest_clust].append(index)

        for key in assignments:
            clust_sum = 0
            for k in assignments[key]: 
                clust_sum = clust_sum + data[k]
            centroids[key] = [m / len(assignments[key]) for m in clust_sum] 

    return centroids


def run(values):
    plt = get_plt()
    n = 2 # Number of entities observed
    ts_len = 1000 # The number of times each entity is observed

    phases = np.array(np.random.randint(0, 50, [n, 2])) # Create our attributes
    pure = np.sin([np.linspace(-np.pi * x[0], -np.pi * x[1], ts_len) for x in phases]) # Make our attributes a sin wave
    noise = np.array([np.random.normal(0, 1, ts_len) for x in range(n)]) # Create an array of random noise
    # print(pure)
    signals = pure * noise # Add some noise so it isn't exactly a sin wave
    # print(signals)
    # print(signals[0])
    # print(signals[0][0])
    node_keys=['mass0_1', 'mass0_2']
    nodes = Node.objects.values_list(*node_keys)[:1000]
    signals = []
    signals.append([n[0] for n in nodes])
    signals.append([n[1] for n in nodes])

    signals = np.array(signals)

    print(signals)



    # Normalize everything between 0 and 1
    signals += np.abs(np.min(signals))
    signals /= np.max(signals)
    plt.style.use('seaborn-bright')
    # plt.plot(signals)
    centroids = k_means(signals, 50, 100)
    print(centroids)
    print(len(centroids[0]))
    print(len(centroids[1]))
    plt.plot(centroids)
    # plt.scatter(centroids)
    # plt.scatter([i for i in range(ts_len)], centroids[0])
    # plt.scatter([i for i in range(ts_len)], centroids[1])
    # for i in range(ts_len):
        # plt.plot(centroids[0][i], centroids[1][i])
    # plt.plot(centroids)

    # print(centroids[0])
    # # plt.plot(centroids[0])
    # for index, p in enumerate(centroids[0]):
    #     print(p)
    #     print(index)
    #     print(p[0], p[1])
    #     plt.plot(p[0], p[1])
    # for p in centroids:
    #     plt.plot(p)
    # plt.plot(centroids[0])
    # plt.plot(centroids)
    # print('f')
    # print(centroids[0])
    # print(len(centroids))
    return (plot_to_uri(plt), [])