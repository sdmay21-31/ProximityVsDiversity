from django.test import TestCase
from app.models import Node, Dataset


class TestQuery(TestCase):
    def new_dataset(self):
        dataset = Dataset(name="test", description="", attributes=[])
        dataset.save()
        return dataset

    def new_node(
        self,
        dataset,
        simulation,
        simulation_index,
        simulation_total_nodes,
        data=[],
        relativised_data=[]
    ):
        node = Node(
            dataset=dataset,
            simulation=simulation,
            simulation_index=simulation_index,
            simulation_total_nodes=simulation_total_nodes,
            data=data,
            relativised_data=relativised_data)
        node.save()

    def test_query_returns_timeframe(self):
        d = self.new_dataset()
        self.new_node(d, 1, 1, 3)
        self.new_node(d, 1, 2, 3)
        self.new_node(d, 1, 3, 3)
        self.new_node(d, 2, 1, 2)
        self.new_node(d, 2, 2, 2)
        self.new_node(d, 3, 1, 1)

        nodes = Node.objects.filter_timeframe(.5)
        assert nodes.count() == 3
