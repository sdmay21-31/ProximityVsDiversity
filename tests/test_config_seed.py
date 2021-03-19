from app import seed

# TEST_URL = 'tests/test_datasets/'

import csv

from app.seed import nodeDictionary

class TestConfigSeed:
    
    # TODO
    def dummy_test(self, db):
        database = 'main_table_1.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database)
        
        count = node_type.objects.count()
        assert count == 10355968