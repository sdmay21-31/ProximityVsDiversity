from app.matplot import get_plt
import numpy as np

def relativise(value, mmax, mmin):
    return (value - mmin) / (mmax / mmin)

class DatasetShim:
    def process(self):
        simulations = self.simulation_set.filter(total_nodes=1001)
        nodes = []
        for simulation in simulations:
            maxs = [0, 0]
            mins = [float('inf'), float('inf')]

            for n in simulation.data:
                node = [float(n[0]), float(n[1])]
                if node[0] > maxs[0]:
                    maxs[0] = node[0]
                if node[1] > maxs[1]:
                    maxs[1] = node[1]
                if node[0] < mins[0]:
                    mins[0] = node[0]
                if node[1] < mins[1]:
                    mins[1] = node[1]

            node = [float(simulation.data[100][0]), float(simulation.data[100][1])]
            nodes.append([
                relativise(node[0], maxs[0], mins[0]),
                relativise(node[1], maxs[1], mins[1]),
            ])
            
        xs = [n[0] for n in nodes]
        ys = [n[1] for n in nodes]

        plt = get_plt()

        plt.scatter(xs, ys)
        return plt


