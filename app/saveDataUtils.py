import csv
import os
import pandas as pd
import numpy as np
from app import readDataUtils

# Constants
NODE_FILE_DELIMITER = ", "
DATATYPE_READ_LIMIT = 100
INDENT = "    "


def writeNodeText(node_names):
    
    openFile = open('datasets/nodeList.txt', "a")
    
    # Create a string to write to the node file
    dataString = ""
    listLen = len(node_names)
    
    if listLen > 0:
        dataString = node_names[0]
        #dataString = "\n" + node_names[0]
    
    for i in range(1, listLen):
        dataString += NODE_FILE_DELIMITER + node_names[i]
    
    dataString += "\n"
    
    # Write the new string to the file
    openFile.write(dataString)
    openFile.close()

def generateNodeHeaderString():
    
    INDENT = "    "
    
    classString = "from django.db import models\n";
    classString += "\n";
    classString += "\n";
    classString += "# Put query functions here\n";
    classString += "class NodeQuerySet(models.QuerySet):\n";
    classString += INDENT + "def example_query(self, *args, **kwargs):\n";
    classString += INDENT + INDENT + "\"\"\" Filter time_id is less than or equeal to 200\"\"\"\n";
    classString += INDENT + INDENT + "return self.filter(time_id__lte=200)\n";
    classString += "\n";
    classString += "\n";
    classString += "# Put class based attributes here\n";
    
    return classString

def createNodeClassStr(node_names, data_types, node_num):
    
    classString = "class Node" + str(node_num) + "(models.Model):\n"
    
    listLen = len(node_names)
    for i in range(0, listLen):
        currName = node_names[i]
        dataType = data_types[i]
        #print(dataType)
        #print("Datatype is int?: " + str(isinstance(dataType, dtype('int64'))))
        #print("Datatype is float?: " + str(isinstance(dataType, dtype('float64'))))
        
        if currName == "file_id" or currName == "node_id":
            classString += INDENT + currName + " = " + "models.IntegerField(db_index=True)";
        elif currName == "time_id":
            classString += INDENT + currName + " = " + "models.AutoField(primary_key=True)";
        elif dataType == 'int64': # Fix this to work better???
            classString += INDENT + currName + " = " + "models.IntegerField()";
        elif dataType == 'float64': # Fix this to work better???
            classString += INDENT + currName + " = " + "models.FloatField()";
        else:
            classString += INDENT + currName + " = " + "models.CharField(max_length=20)";
        
        classString += "\n"
    
    return classString

def generateNodeExtrasString():
    
    classString = INDENT + "# Set the manager\n";
    classString += INDENT + "objects = NodeQuerySet.as_manager()\n";
    classString += INDENT + "\n";
    classString += INDENT + "# Properties\n";
    classString += INDENT + "@property\n";
    classString += INDENT + "def __str__(self):\n";
    classString += INDENT + INDENT + "return 'Node: {}'.format(self.time_id)\n";
    classString += INDENT + "\n";
    classString += INDENT + "@property\n";
    classString += INDENT + "def id(self):\n";
    classString += INDENT + INDENT + "\"\"\" Example Property: Return Node primary key \"\"\"\n";
    classString += INDENT + INDENT + "return self.time_id\n";
    classString += INDENT + "\n";
    classString += INDENT + "# Functions\n";
    classString += INDENT + "def get_id(self, *args, **kwargs):\n";
    classString += INDENT + INDENT + "\"\"\" Example method: Return Node primary key \"\"\"\n";
    classString += INDENT + INDENT + "return self.time_id\n";
    classString += INDENT + "\n";
    classString += INDENT + "def __repr__(self):\n";
    classString += INDENT + INDENT + "return str(self.mass_1)\n";
    classString += "\n";
    classString += "\n";
    classString += "\n";
    
    return classString

def appendNodeFile(node_names, data_types):
    
    #openFile = open('datasets/nodeFile.txt', "a")
    openFile = open('datasets/nodeFile.txt', "w")
    
    # Create a string to write to the node file
    dataString = generateNodeHeaderString()
    dataString += createNodeClassStr(node_names, data_types)
    dataString += generateNodeExtrasString()
    
    # Write the new string to the file
    print(dataString)
    openFile.write(dataString)
    openFile.close()
    
    # TODO

def generateEntireNodeFile():
    
    # Open files for reading/writing
    #openFile = open('datasets/nodeFile.txt', "w")
    openFile = open('app/models.py', "w")
    file_names = os.listdir('datasets/')
	
    # Add the header content to the string
    dataString = generateNodeHeaderString()
    node_num = 1
    
    # Create node classes for each of the datasets
    listLen = len(file_names)
    for i in range(0, listLen): # Files are iterated alphabetically
        curr_file_name = file_names[i]
        
        if curr_file_name.endswith(".csv"):
            node_names = readDataUtils.getNames(curr_file_name)
            data_types = readDataUtils.getDataTypes(curr_file_name)
            dataString += createNodeClassStr(node_names, data_types, node_num)
            dataString += generateNodeExtrasString()
            node_num += 1
        
    
    # Write the new string to the file
    #print(dataString)
    openFile.write(dataString)
    openFile.close()

def generateFileNodeMappings():
    
    # Open files for reading
    openFile = open('datasets/nodeFileMappings.txt', "w")
    file_names = os.listdir('datasets/')
    node_num = 1
    
    # Create node classes for each of the datasets
    listLen = len(file_names)
    for i in range(0, listLen): # Files are iterated alphabetically
        curr_file_name = file_names[i]
        
        if curr_file_name.endswith(".csv"):
            mapping_string = curr_file_name + ", " + "Node" + str(node_num) + "\n"
            openFile.write(mapping_string)
            node_num += 1
        
    openFile.close()

def generateNodeDictionaryFile():
    
    # Open files for reading
    #openFile = open('datasets/nodeDictionary.txt', "w")
    openFile = open('app/nodeDictionary.py', "w")
    file_names = os.listdir('datasets/')
    
    # Initialize loop data
    dictionary_string = "from app import seed\n"
    node_num = 1
    
    dictionary_string += "\n"
    dictionary_string += "\n"
    dictionary_string += "node_dictionary = {\n"
    
    # Create node classes for each of the datasets
    listLen = len(file_names)
    for i in range(0, listLen): # Files are iterated alphabetically
        curr_file_name = file_names[i]
        
        if curr_file_name.endswith(".csv"):
            dictionary_string += INDENT + "\"" + curr_file_name + "\": seed.Node" + str(node_num) + ",\n"
            node_num += 1
        
    dictionary_string += "}\n"
    
    openFile.write(dictionary_string)
    openFile.close()
    
# Node dictionary
"""
nodeDictionary = {
    "main_table_1.csv": Node,
    "main_table_2.csv": Node2,
    "hungary_chickenpox.csv": Node3
}
"""
