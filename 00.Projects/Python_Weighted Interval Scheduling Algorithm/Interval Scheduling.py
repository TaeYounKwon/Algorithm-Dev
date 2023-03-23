from functools import cmp_to_key
import csv

#Save the Data with the format: start, finish, value
class Data:
 
    def __init__(self, start, finish, value):
 
        self.start = start
        self.finish = finish
        self.value = value
 
#Read the CSV file and sort the list according to the 'class Data'        
def readFile():
    file = open('data.csv', 'r', encoding='utf-8')
    line = csv.reader(file)

    #Save CSV data line by line
    tmp = []
    for i in line:
        tmp.append(i)
    file.close()
    
    #Save the data in 2D list
    tmp2 = []
    for i in range(len(tmp)):
        tmp2.append([])
        for j in range(len(tmp[i])):
            tmp2[i].append(int(tmp[i][j]))
            
    #Sort the data in tmp2 by finishing time so that f1<=f2<=...<=fn.
    sorted(tmp2,key=lambda l:l[1])
    
    #Put sorted list into dataList
    dataList = []
    for i in range(len(tmp2)):
        dataList.append(Data(tmp2[i][0],tmp2[i][1],tmp2[i][2]))
             
    dataLength = len(dataList)
    
    #Start find MaxVal
    findMaxVal(dataList, dataLength)
 
# Check if there is an exist interval that does not have time conflict
def findInterval(dataList, val):
    
    #checking the inteverals from the largest finish time
    for i in reversed(range(val)):
        if dataList[i].finish <= dataList[val - 1].start:
            return i
    return -1
 
 #Bottom-Up dynamic programming - unwind recursion
def findMaxVal(dataList, dataLength):
    
    #If dataLength less than 0, terminate the program
    if dataLength <0:
        quit()
    
    if dataLength == 0:
        return dataList[0].value
 
    val = [None] * dataLength
    
    #input the first value(weight or profit)
    val[0] = dataList[0].value
    
    #compute p(1), p(2),....p(n)
    for i in range(1, dataLength):
 
        #dynamic program saving the cumulated value
        valCumulate = dataList[i].value
        newInterval = findInterval(dataList, i)        

        if newInterval != -1:
            valCumulate += val[newInterval]
            
        #choose max value in i time
        val[i] = max(valCumulate, val[i - 1])
        
    result = val[dataLength - 1]
 
    print(result)
 
readFile()