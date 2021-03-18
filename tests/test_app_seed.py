from app import seed

# TEST_URL = 'tests/test_datasets/'

class TestSeed:
	
	def test_seed_database(self):
		path = reverse('databases')
		assert resolve(path).view_name == 'databases'