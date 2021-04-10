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

    def get_attribute_index(self, attr):
        return self.attributes.index(attr)

    def process(self, time_value, number_of_clusters, proximity=None, diversity=None):
        simulations = self.simulation_set.iterator(1000)
        attributes = proximity.get('attributes')

        if len(attributes) not in [2, 3]:
            raise ValueError

        is_3d = True if len(attributes) == 3 else False

        attribute_indexes = [
            self.get_attribute_index(attr)
            for attr in attributes]
        weights = [
            float(weight)
            for weight in proximity.get('weights')
        ]

        time_percentage = float(time_value) / self.max_simulation_nodes
        nodes = []
        for simulation in simulations:
            # Get the linearly interpolated node
            node_time_index = int(simulation.total_nodes * time_percentage)
            maxs = [0 for n in attribute_indexes]
            mins = [float('inf') for n in attribute_indexes]

            # Find the min and max
            for n in simulation.data:
                node = [float(n[attr_index]) for attr_index in attribute_indexes]

                for attr_index in attribute_indexes:
                    if node[attr_index] > maxs[attr_index]:
                        maxs[attr_index] = node[attr_index]
                    if node[attr_index] < mins[attr_index]:
                        mins[attr_index] = node[attr_index]

            # Get the nodes for the specific time instance
            node = [
                float(simulation.data[node_time_index][attr_index])
                for attr_index in attribute_indexes]
            # Relativise
            try:
                nodes.append([
                    relativise(node[attr_index], maxs[attr_index], mins[attr_index])
                    for attr_index in attribute_indexes
                ])
            except ZeroDivisionError:
                pass

        # Prepare initial centers using K-Means++ method.
        metric = distance_metric(type_metric.USER_DEFINED, func=weighted_euclidean_distance(weights))
        initial_centers = kmeans_plusplus_initializer(nodes, number_of_clusters).initialize()
         
        # Create instance of K-Means algorithm with prepared centers.
        kmeans_instance = kmeans(nodes, initial_centers, metric=metric)
         
        # Run cluster analysis and obtain results.
        kmeans_instance.process()
        clusters = kmeans_instance.get_clusters()
        final_centers = np.array(kmeans_instance.get_centers())

        # Add points for graph
        # TODO: make dynamic for attribute_indexes
        plt = get_plt()

        xs = [n[0] for n in nodes]
        ys = [n[1] for n in nodes]
        projection = None
        if is_3d:
            zs = [n[2] for n in nodes]
            projection = '3d'

        fig = plt.figure()
        ax = fig.add_subplot(projection=projection)


        ax.set_xlabel(attributes[0])
        ax.set_ylabel(attributes[1])

        if is_3d:
            ax.scatter(xs, ys, zs, s=1)
            ax.scatter(final_centers[:,0], final_centers[:,1], final_centers[:,2], c='black')
            ax.set_zlabel(attributes[2])
        else: #Is 2D
            ax.scatter(xs, ys, s=1)
            ax.scatter(final_centers[:,0], final_centers[:,1], c='black')

        return plt


