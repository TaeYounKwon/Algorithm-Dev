from cmath import pi
import itertools
import sys
import csv
import timeit

sys.setrecursionlimit(1000000)

#Iterative
def iterativePower(base, exponent):
    retVal = 1.0;
    
    if exponent < 0:
        return 1.0 / iterativePower(base, -exponent)
    else:
        for i in range(0, exponent):
            retVal *= base
            
    return retVal
#Recursive
def recursivePower(base, exponent):
    
    if exponent < 0:
        return 1.0 / recursivePower(base, -exponent)
    elif exponent ==0:
        return 1.0
    else:
        return base * recursivePower(base, exponent -1)
    
dataList = []
 
for i in itertools.count(start=1):
   startIter = timeit.default_timer()
   iterativePower(3.14159265359,i)
   recordData1 = (timeit.default_timer()-startIter)*100000
   
   startRecurs = timeit.default_timer()
   recursivePower(3.14159265359,i)
   recordData2 = (timeit.default_timer()-startRecurs)*100000
   
   recordIter = str(round(recordIter, 2))   
   recordRecurs = str(round(recordRecurs, 2))
    
   dataList.append((i,recordIter,recordRecurs))
   with open('data.csv','w',newline='') as csvFile:
       writeCSV=csv.writer(csvFile)
       for i in dataList:
           writeCSV.writerow(i)