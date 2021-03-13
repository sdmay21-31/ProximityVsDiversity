from django.test import TestCase
from app.algos import example_algo
from app.seed import run as seed_nodes
from app.models import Node


# Create your tests here.
class ExampleQueryUnitTestCase(TestCase):
    def setUp(self):
        """ Run before every test """
        seed_nodes(full_seed=False, chunk_size=200, print_status=False)

    def test_ids_less_than_or_equal_to_50(self):
        """ Make sure there is no id that is greater than 200"""
        ids = [node.id for node in Node.objects.example_query()]
        self.assertTrue(max(ids) <= 200)




