from .kmeans import Kmeans
from .dummy import DummyAlgo
from app.matplot import plot_to_uri

def run(method='kmeans', time_frame=1, proximity=[], diversity=[]):
    if not len(proximity) and not len(diversity):
        raise ValueError("Attributes required")

    if len(proximity) + len(diversity) > 3:
        raise ValueError("Attributes must be less than 3")

    if method == 'kmeans':
        algo = Kmeans(time_frame, proximity, diversity)
    else:
        algo = DummyAlgo(time_frame, proximity, diversity)

    algo.initialize()
    algo.process()
    return (
        plot_to_uri(algo.get_plot()),
        {
        'algo': algo.name,
         'extra': algo.extra
         })
