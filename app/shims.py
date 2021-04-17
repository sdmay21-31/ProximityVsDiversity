from app.matplot import get_plt
import numpy as np
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

from pyclustering.utils.metric import distance_metric, type_metric
from django.apps import apps


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

    def get_timeframe(self, time_percentage):
        TimeFrame = apps.get_model('app', 'TimeFrame')
        try:
            return TimeFrame.objects.get(dataset=self, time_percentage=time_percentage)
        except TimeFrame.DoesNotExist:
            return TimeFrame.create_timeframe(self, time_percentage)

    def process(self, time_value, number_of_clusters, proximity=None, diversity=None):
        attributes = proximity.get('attributes')
        threshold_attributes = diversity.get('attributes')

        if len(attributes) not in [2, 3]:
            raise ValueError

        is_3d = True if len(attributes) == 3 else False

        attribute_indexes = [
            self.get_attribute_index(attr)
            for attr in attributes]

        threshold_indexes = [
            self.get_attribute_index(attr)
            for attr in threshold_attributes
        ]

        print(threshold_indexes)

        weights = [
            float(weight)
            for weight in proximity.get('weights')
        ]

        time_percentage = float(time_value) / self.max_simulation_nodes
        nodes = self.get_timeframe(time_percentage).relativised_nodes

        def filter_threshold(node):
            """For each node: find all distances between proximity attributes
            find all distances between distance attributes

            for every distance in both:
                if abs(dis1 / dis2 ) < threshold:
                    ignore it
            """
            pass

        def get_specific_nodes(n):
            return [
                n[a] for a in attribute_indexes
            ]

        nodes = list(map(get_specific_nodes, nodes))

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


class TimeFrameShim:
    @classmethod
    def create_timeframe(cls, dataset, time_percentage):
        simulations = dataset.simulation_set.iterator(1000)
        attributes = dataset.attributes
        nodes = []
        for simulation in simulations:
            # Get the linearly interpolated node
            node_time_index = int(simulation.total_nodes * time_percentage)
            maxs = [0 for n in attributes]
            mins = [float('inf') for n in attributes]

            # Find the min and max
            for n in simulation.data:
                node = [float(attr) for attr in n]

                for index in range(len(node)):
                    if node[index] > maxs[index]:
                        maxs[index] = node[index]
                    if node[index] < mins[index]:
                        mins[index] = node[index]

            # Get the nodes for the specific time instance
            node = [
                float(simulation.data[node_time_index][attr_index])
                for attr_index in range(len(attributes))]
            # Relativise
            try:
                nodes.append([
                    relativise(node[index], maxs[index], mins[index])
                    for index in range(len(attributes))
                ])
            except ZeroDivisionError:
                pass
        timeframe = cls(
            dataset=dataset,
            time_percentage=time_percentage,
            relativised_nodes=nodes
        )
        timeframe.save()
        return timeframe
