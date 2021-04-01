from app.matplot import get_plt
import numpy as np

"""Kmeans courtesy of: https://github.com/corvasto/Simple-k-Means-Clustering-Python/blob/master/kMeansClustering.py
"""
def compute_euclidean_distance(point, centroid):
    return np.sqrt(np.sum((point - centroid)**2))

def assign_label_cluster(distance, data_point, centroids):
    index_of_minimum = min(distance, key=distance.get)
    return [index_of_minimum, data_point, centroids[index_of_minimum]]

def compute_new_centroids(cluster_label, centroids):
    return np.array(cluster_label + centroids)/2

def iterate_k_means(data_points, centroids, total_iteration):
    label = []
    cluster_label = []
    total_points = len(data_points)
    k = len(centroids)
    
    for iteration in range(0, total_iteration):
        for index_point in range(0, total_points):
            distance = {}
            for index_centroid in range(0, k):
                distance[index_centroid] = compute_euclidean_distance(data_points[index_point], centroids[index_centroid])
            label = assign_label_cluster(distance, data_points[index_point], centroids)
            centroids[label[0]] = compute_new_centroids(label[1], centroids[label[0]])

            if iteration == (total_iteration - 1):
                cluster_label.append(label)

    return [cluster_label, centroids]

def create_centroids():
    centroids = []
    centroids.append([.2, 0.6])
    centroids.append([.1, .0001])
    centroids.append([0, 0])
    return np.array(centroids)


def relativise(value, mmax, mmin):
    return (value - mmin) / (mmax - mmin)

class DatasetShim:
    def process(self):
        simulations = self.simulation_set.filter(total_nodes=1001)
        nodes = []
        for simulation in simulations:
            maxs = [0, 0, 0]
            mins = [float('inf'), float('inf'), float('inf')]

            for n in simulation.data:
                node = [float(n[0]), float(n[1]), float(n[2])]
                if node[0] > maxs[0]:
                    maxs[0] = node[0]
                if node[1] > maxs[1]:
                    maxs[1] = node[1]
                if node[2] > maxs[2]:
                    maxs[2] = node[2]
                if node[0] < mins[0]:
                    mins[0] = node[0]
                if node[1] < mins[1]:
                    mins[1] = node[1]
                if node[2] < mins[2]:
                    mins[2] = node[2]

            node = [float(simulation.data[500][0]), float(simulation.data[500][1]), float(simulation.data[500][2])]
            x = relativise(node[0], maxs[0], mins[0])
            y = relativise(node[1], maxs[1], mins[1])
            z = relativise(node[2], maxs[2], mins[2])
            nodes.append([x, y, z])


        xs = [n[0] for n in nodes]
        ys = [n[1] for n in nodes]
        zs = [n[2] for n in nodes]

        plt = get_plt()
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.scatter(xs, ys, zs)
        # plt.scatter(new_centroids[:,0], new_centroids[:,1], c='black')
        return plt


