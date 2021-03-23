from app import seed
from subprocess import call
import os
import django

# TEST_URL = 'tests/test_datasets/'

import csv

from app.seed import nodeDictionary

class TestConfigSeed:
    
    def test_without_database_arg(self, db):
        database = "main_table_1.csv"
        
        # Django is definitely installed...What is the problem???
        print(django.VERSION)
        
        print(os.getcwd())
        
        # This may not be a valid function call...
        call(["source", ".venv/Scripts/activate"])
        #call(["source", "../.venv/Scripts/activate"])
        
        # The path for manage.py depends on the current working directory
        argList = ["python", "manage.py", "seed"]
        
        # This program appears to run correctly...
        #argList = ["ls", "-l"]
        
        # Setting python path does not appear to work, unless wrong directory was used
        # DJANGO_SETTINGS_MODULE = config.settings -> settings.py
        
        # manage.py cannot find "django" for some reason on line 11
        # Some item failed to be imported at the very least...
        call(argList, shell=True)
        print(argList)
        
        node_type = nodeDictionary[database]
        count = node_type.objects.count()
        assert count == 10000
    
    def test_database_arg_1(self, db):
        database = "main_table_1.csv"
        
        argList = ["python", "manage.py", "seed", "-d", database]
        call(argList)
        
        node_type = nodeDictionary[database]
        count = node_type.objects.count()
        assert count == 10000
    
    def test_database_arg_2(self, db):
        database = "main_table_2.csv"
        
        argList = ["python", "manage.py", "seed", "-d", database]
        call(argList)
        
        node_type = nodeDictionary[database]
        count = node_type.objects.count()
        assert count == 10000
    
    def test_database_arg_3(self, db):
        database = "hungary_chickenpox.csv"
        
        argList = ["python", "manage.py", "seed", "-d", database]
        call(argList)
        
        node_type = nodeDictionary[database]
        count = node_type.objects.count()
        assert count == 10000
    