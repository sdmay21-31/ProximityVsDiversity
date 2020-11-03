from app.models import Node


def example_algo():
    """ Return the mass_1 of example_query nodes """
    nodes = Node.objects.example_query()
    masses = [node.mass_1 for node in nodes]
    return masses
