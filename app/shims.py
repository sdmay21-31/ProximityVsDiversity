from app.matplot import get_plt
import numpy as np

class DatasetShim:
    def process(self):
        simulations = self.simulation_set.filter(total_nodes=1001)
        nodes = []
        for simulation in simulations:
            nodes.append(simulation.data[0])
        xs = [float(n[0]) for n in nodes]
        ys = [float(n[1]) for n in nodes]

        plt = get_plt()

        plt.scatter(xs, ys)
        return plt


