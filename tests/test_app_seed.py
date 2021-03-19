from app import seed

# TEST_URL = 'tests/test_datasets/'

import csv

from app.seed import nodeDictionary

class TestSeed:
    
    """
    @pytest.fixture
    def delete_existing_nodes(file_name):
        node_to_delete = nodeDictionary[file_name]
        node_to_delete.objects.all().delete()
    """
    
    """
    @pytest.fixture
    def objects_all_tester(file_name):
        node_type = nodeDictionary[file_name]
        
        count = node_type.objects.count()
        exist = node_type.objects.exists()
        allElements = node_type.objects.all()
        print("Count: " + str(count))
        print("Exists: " + str(exist))
        print("All elements: " + str(allElements))
    """
    
    def test_seed_database_1(self, db):
        database = 'main_table_1.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database)

    def test_seed_database_2(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database)

    def test_seed_database_3(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database)



    def test_seed_database_2_full(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True)

    def test_seed_database_3_full(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True)



    def test_seed_database_2_larger_chunk(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True, 20000)

    def test_seed_database_2_smaller_chunk(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True, 100)

    def test_seed_database_2_exact_size_chunk(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True, 30285)

    def test_seed_database_2_print_status(self, db):
        database = 'main_table_2.csv'
        
        # Delete all rows
        node_to_delete = nodeDictionary[database]
        node_to_delete.objects.all().delete()
        
        seed.run(database, True, 10000, False)




    def test_objects_all_1(self, db):
        # Get the node type
        file_name='main_table_1.csv'
        node_type = nodeDictionary[file_name]
        
        count = node_type.objects.count()
        exist = node_type.objects.exists()
        allElements = node_type.objects.all()
        print("Count: " + str(count))
        print("Exists: " + str(exist))
        print("All elements: " + str(allElements))

    def test_objects_all_2(self, db):
        # Get the node type
        file_name='main_table_2.csv'
        node_type = nodeDictionary[file_name]
        
        count = node_type.objects.count()
        exist = node_type.objects.exists()
        allElements = node_type.objects.all()
        print("Count: " + str(count))
        print("Exists: " + str(exist))
        print("All elements: " + str(allElements))

    def test_objects_all_3(self, db):
        # Get the node type
        file_name='hungary_chickenpox.csv'
        node_type = nodeDictionary[file_name]
        
        count = node_type.objects.count()
        exist = node_type.objects.exists()
        allElements = node_type.objects.all()
        print("Count: " + str(count))
        print("Exists: " + str(exist))
        print("All elements: " + str(allElements))



