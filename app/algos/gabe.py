

from app.models import Node

import time
import numpy as np
from app.matplot import get_plt, plot_to_uri
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

"""Major help from

https://blog.newrelic.com/product-news/optimizing-k-means-clustering/
"""


def euclid_dist(t1, t2):
         return np.sqrt(((t1-t2)**2).sum())
         
def k_means(data, num_clust, num_iter):
    centroids = data[np.random.randint(0, data.shape[0], num_clust)]
    # How many times we want to run kmeans
    for n in range(num_iter):
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

    node_keys = ['node_id', 'mass0_1', 'lumin_1']
    nodes = Node.objects.values_list(*node_keys)

    good_nodes = []
    node_ids = set()
    for n in nodes:
        if not n[0] in node_ids:
            good_nodes.append([n[1], n[2]])
            node_ids.add(n[0])

    print(np.array(good_nodes))


    X, y_true = make_blobs(n_samples=300, centers=4,
                       cluster_std=0.60, random_state=0)
    X = np.array(good_nodes)
    plt.scatter(X[:, 0], X[:, 1], s=50);

    kmeans = KMeans(n_clusters=4)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)

    return (plot_to_uri(plt), [])
    
    # Normalize each eattribute to 1
     
    
    # plt.style.use('seaborn-bright')
    # plt.plot(signals)
    centroids = k_means(signals, 50, 10)
    print(centroids)
    x = []
    y = []
    for index, c in enumerate(centroids):
        x.append(index * 200)
        y.append(c[0])
    plt.plot(x, y)
    # plt.plot(t)
    # print(centroids)
    # for i in 
    # print(len(centroids[0]))
    # print(len(centroids[1]))
    # plt.plot(centroids[0])
    # plt.plot(centroids[1])
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