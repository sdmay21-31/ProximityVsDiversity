# Modified Youtube video example

from django.urls import reverse, resolve

class TestUrls:
	
	def test_database_name_url(self):
		path = reverse('databases')
		assert resolve(path).view_name == 'databases'