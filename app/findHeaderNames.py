import csv
import pandas as pd


def newSeed(file_name='main_table_1.csv'):
    
    node_data = getNames(file_name)
    in_file = isNodeInFile(node_data)
    
    # aaa
    
    # return columns

def getNames(file_name='main_table_1.csv'):
    
    data = pd.read_csv('datasets/' + file_name, nrows=1)
    columns = data.columns.tolist()
    """
    length = len(columns)
    for i in range(0, length):
        print(columns[i])
    """
    # isNodeInFile(columns)
    
    return columns

# Check whether the given list is in the file
def isNodeInFile(node_data):
    
    openFile = open('datasets/nodeList.txt', "r")
    #print(openFile.read())
    #print(openFile.readlines())
    #print(openFile.readline())
    
    currLine = openFile.readline().strip()
    
    while currLine:
        currElementList = currLine.split(", ")
        equalTypes = nodeTypesEqual(node_data, currElementList)
        print(equalTypes)
        currLine = openFile.readline().strip()
    
    return False

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

def createNodeText(file_name='main_table_1.csv'):
    
    df = pd.read_csv('datasets/' + file_name, nrows=0)
    #print(df)
    columns = df.columns.tolist()
    print(columns)
    #print('a')
    
    length = len(columns)
    for i in range(0, length):
        print(columns[i])
    
    return columns