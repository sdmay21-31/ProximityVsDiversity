import csv
import os
import pandas as pd
import numpy as np
from app import saveDataUtils

# Constants
NODE_FILE_DELIMITER = ", "
DATATYPE_READ_LIMIT = 100


def newSeed(file_name='main_table_1.csv'):
    
    # Create info lists
    node_names = getNames(file_name)
    data_types = getDataTypes(file_name)
    
    is_in_file = isNodeInFile(node_names)
    print(is_in_file)
    
    if not is_in_file:
        writeNodeText(node_names)
    
    createNodeClassStr(node_names, data_types, 1)
    #generateNodeFile(node_names, data_types)
    generateEntireNodeFile()
    
    # aaa
    
    # return columns

def getNames(file_name='main_table_1.csv'):
    
    data = pd.read_csv('datasets/' + file_name, nrows=1)
    columns = data.columns.tolist()
    
    return columns

# Check whether the given list is in the file
def isNodeInFile(node_names):
    
    openFile = open('datasets/nodeList.txt', "r")
    
    # Read each line of the file, and check if node_names is in the list
    is_in_file = False
    currLine = openFile.readline().strip()
    while currLine:
        currElementList = currLine.split(NODE_FILE_DELIMITER)
        equalTypes = nodeTypesEqual(node_names, currElementList)
        
        if equalTypes:
            is_in_file = True
        
        currLine = openFile.readline().strip()
    
    return is_in_file

# Check whether two lists of data contain the same elements
def nodeTypesEqual(givenDataList, prevDataList):
    
    givenDataLen = len(givenDataList)
    prevDataLen = len(prevDataList)
    
    if givenDataLen != prevDataLen:
        return False
    
    for i in range(0, givenDataLen):
        givenData = givenDataList[i]
        prevData = prevDataList[i]
        
        if givenData != prevData:
            return False
    
    return True

def getDataTypes(file_name='main_table_1.csv'):
    
    data = pd.read_csv('datasets/' + file_name, nrows=DATATYPE_READ_LIMIT)
    datatypeList = data.dtypes.tolist()
    
    return datatypeList
