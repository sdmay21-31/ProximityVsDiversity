from app.matplot import get_plt
import numpy as np
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from pyclustering.utils.metric import distance_metric, type_metric

def relativise(value, mmax, mmin):
    return (value - mmin) / (mmax - mmin)

def weighted_euclidean_distance(weights):
    def euclidean_distance_square(point1, point2):
        distance = 0.0
        for i in range(len(point1)):
            distance += ((point1[i] - point2[i]) ** 2.0) * weights[i]

        return distance

    def euclidean_distance(point1, point2):
        distance = euclidean_distance_square(point1, point2)
        return distance ** 0.5

    return euclidean_distance

class DatasetShim:

    def process(self, time_value, number_of_clusters, proximity=None, diversity=None):
        simulations = self.simulation_set.filter(total_nodes__gt=5).iterator(1000)
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

            node = [float(simulation.data[time_value][0]), float(simulation.data[time_value][1]), float(simulation.data[time_value][2])]
            try:
                x = relativise(node[0], maxs[0], mins[0])
                y = relativise(node[1], maxs[1], mins[1])
                z = relativise(node[2], maxs[2], mins[2])
                nodes.append([x, y, z])
            except ZeroDivisionError:
                pass

        # Prepare initial centers using K-Means++ method.
        metric = distance_metric(type_metric.USER_DEFINED, func=weighted_euclidean_distance([1, 1, 1]))
        initial_centers = kmeans_plusplus_initializer(nodes, number_of_clusters).initialize()
         
        # Create instance of K-Means algorithm with prepared centers.
        kmeans_instance = kmeans(nodes, initial_centers, metric=metric)
         
        # Run cluster analysis and obtain results.
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        final_centers = np.array(kmeans_instance.get_centers())

        xs = [n[0] for n in nodes]
        ys = [n[1] for n in nodes]
        zs = [n[2] for n in nodes]


        plt = get_plt()
        # fig = plt.figure()
        # ax = fig.add_subplot(projection='3d')
        plt.scatter(xs, ys, s=1)
        plt.scatter(final_centers[:,0], final_centers[:,1], c='black')
        return plt


