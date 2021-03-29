import csv
import os
import pandas as pd
import numpy as np
from app import saveDataUtils
from app import readDataUtils

# Constants
NODE_FILE_DELIMITER = ", "
DATATYPE_READ_LIMIT = 100


def newSeed(file_name='main_table_1.csv'):
    
    # Create info lists
    node_names = readDataUtils.getNames(file_name)
    data_types = readDataUtils.getDataTypes(file_name)
    
    is_in_file = readDataUtils.isNodeInFile(node_names)
    print(is_in_file)
    
    if not is_in_file:
        saveDataUtils.writeNodeText(node_names)
    
    saveDataUtils.createNodeClassStr(node_names, data_types, 1)
    #generateNodeFile(node_names, data_types)
    saveDataUtils.generateEntireNodeFile()
    
    saveDataUtils.generateFileNodeMappings()
    saveDataUtils.generateNodeDictionaryFile()
    
    # aaa
    
    # return columns