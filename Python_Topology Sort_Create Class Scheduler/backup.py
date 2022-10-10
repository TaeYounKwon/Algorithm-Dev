import re
import schemdraw
from fileinput import filename
from collections import deque
from schemdraw import flow
d = schemdraw.Drawing()
s = schemdraw.Drawing()

dataList = []        # The file that has all the input value

classWOpre = []      # Classes without prerequisites
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Taken(True or False)
                     # 2.Quarter('1,2')
                     # 3.Credit
classWOfinal = []                     
                     
classWpreInfo = []   # Classes with prerequisites
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Taken(True or False)
                     # 2.Quarter('1,2')
                     # 3.Credit      
                     # 4.Prerequisite Fullfilled(True or False)

flowChartInfo = []   # Classes with prerequisites
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Taken(True or False)
                     # 2.Quarter('1,2')      
                     # 3.Prerequisite Fullfilled(True or False)                     
                         
classWpre = []       # Prerequisites classes and classes with prerequisites                     
classWpreSorted = [] # Classes sorted by topology sort
classCode = []       # Store class code (csc1230)
degreeCheck = []     # Store the number of Prerequisites remained
degreeFlow = []
finalPlan =[]        # 2D list, store final schedule to take the classes 
creditPerqurter = []
chartPlan=[]

#If input value has missing information, stop the while loop in creating plan
catchError = []
 
#Read File from user input file, 
def readFile(fileName):
    #Reading the file
    try:
        file = ''
        file = fileName
        data = open(file, 'r')
    #If cannot find file, terminate python
    except OSError:
        print("could not open/read the file: ", fileName)    
        quit()
        
    with data:    
        line = data.readline()

        line_Numb = 0
        index=[]
        tmp=''
        inBracket = False   
        
        while(line):
            dataList.append([])
            
            #save the data wihtout '[', ']', '\n', and ','(except ',' inside of [])
            for i in line:
                if i=='[':
                    inBracket=True 
                if i==',' and inBracket==False:
                    if tmp != '':
                        index.append(tmp)
                        tmp=''                  
                if i==']':
                    index.append(tmp)
                    inBracket=False 
                    tmp=''        
                if i!=',' and inBracket==False:
                    if i!='\n' and i!=']':
                        tmp=tmp+i                
                if inBracket==True:
                    if i!='[' and i!=']':
                        tmp=tmp+i          
            #Save each combined token into dataList
            for i in range(len(index)):
                dataList[line_Numb].append(index[i])
            index.clear()
            line = data.readline()
            line_Numb += 1

#Separate DataList into classWpreInfo and classWOpre
def seperateClass():
    
    # Save the name of the class and name of prerequisit classes from the dataList to tmp
    tmp= [] 
    tmpExtra= []
    valCount = 0
    
    #If prerequisit exsits, save the class code, prerequisit class codes into the tmp list
    for i in range (len(dataList)):
        if dataList[i][3]!=" ":
            tmp.append([])
            tmp[valCount].append(dataList[i][0])
            tmp[valCount].append(dataList[i][3])
            valCount+=1
        
        #If does not exist, then save the class code to the tmpExtra
        elif dataList[i][3]==" ":
            tmpString = dataList[i][0].replace(' ','')
            tmpExtra.append(tmpString)
            
    #Save the prerequisit information seperated by comma, and deliver those elements to classWpre list          
    tmp2 = []       
    for i in range(len(tmp)):
        tmp2 = tmp[i][1].split(',')
        del tmp[i][1]
        for j in range(len(tmp2)):
            tmp[i].append(tmp2[j])
        tmp2.clear    
    
    #After seperated by comma, remove all whitespace betweeen class code      
    for i in range(len(tmp)):
        classWpre.append([])
        for j in range(len(tmp[i])):
            tmpString = ''
            tmpString = tmp[i][j].replace(' ','')
            classWpre[i].append(tmpString)  
    
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            print(classWpre[i][j],end='--')
        print('')    
            
                
    #have all the classCode -- ex)csc1230
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):           
            if classWpre[i][j] not in classCode:
                classCode.append(classWpre[i][j])
    
    for i in range(len(classCode)):
        degreeFlow.append(0)
        degreeCheck.append(0)
    
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j>0:
                 #if j has prerequisit, add one to degreeCheck
                degreeCheck[classCode.index(classWpre[i][0])] +=1
                degreeFlow[classCode.index(classWpre[i][0])] +=1
    
    #Create classWpreInfo list
    count = 0
    for i in range(len(dataList)):
            checkClass = ''
            checkClass = dataList[i][0].replace(' ','')
            if checkClass in classCode:
                classWpreInfo.append([])
                flowChartInfo.append([])
                classWpreInfo[count].append(checkClass) #0. CSC 1230
                classWpreInfo[count].append(False) #1. TAKEN? => TRUE OR FALSE
                classWpreInfo[count].append(dataList[i][4]) #2. Quarter => 1,2,3
                classWpreInfo[count].append(dataList[i][2]) #3. Credit => 5
                
                flowChartInfo[count].append(checkClass) #0. CSC 1230
                flowChartInfo[count].append(False) #1. TAKEN? => TRUE OR FALSE
                flowChartInfo[count].append(dataList[i][4]) #2. Quarter => 1,2,3
                
                checkPrerequisite = dataList[i][3].replace(' ','')
                
                if checkPrerequisite != '': 
                    flowChartInfo[count].append(False) #3. Prerequisite Taken?
                    classWpreInfo[count].append(False) #4. Prerequisite Taken?
                elif checkPrerequisite== '':
                    flowChartInfo[count].append(True)  #3. Prerequisite Taken?
                    classWpreInfo[count].append(True)  #4. Prerequisite Taken?
                      
                count += 1 
    
            
    #Find the common value between classWpre and tmpExtra, save those element into tmp4
    tmp4 = [] 
    for i in range(len(classCode)):
        for j in range(len(tmpExtra)):
            if classCode[i] == tmpExtra[j]:
                tmp4.append(classCode[i])
                
    #Remove the element from tmpExtra that is already in classWpre        
    for i in range(len (tmp4)):
        tmpExtra.remove(tmp4[i]) 
    
    #Create classWOpre List
    count = 0
    for i in range(len(dataList)):
            checkClass = ''
            checkClass = dataList[i][0].replace(' ','')
            if checkClass in tmpExtra:
                classWOpre.append([])
                classWOpre[count].append(checkClass) #UCOR 3000
                classWOpre[count].append(False) #TAKEN? => TRUE OR FALSE
                classWOpre[count].append(dataList[i][4]) # Quarter => 1,2,3
                classWOpre[count].append(dataList[i][2]) # Credit => 5
                count += 1

#Check each requirements, and add the classes into finalPlan  
def createPlan(quarter,credit):
    
    currentQuarter = quarter
    maxCredit=int(credit)
    numbClass= len(classWOpre) + len(classCode)

    count = 0
    classTaken = 0

    #While loop until number of class = classTaken
    while classTaken<numbClass:    
        currentCredit = 0  
        classTakenBefore = classTaken    
        tmpClass = []
        finalPlan.append([])
        classWOfinal.append([])
        
        #classWpreInfo comes first        
        for i in range(len(classWpreInfo)):       
            if classWpreInfo[i][1] == False: #class not taken
                 if currentCredit + int(classWpreInfo[i][3]) < maxCredit: #enough credit to take
                    if classWpreInfo[i][4] == True: #Prerequisite fullfilled    
                        for tmpString in classWpreInfo[i][2]: #quarter match
                            if currentQuarter in tmpString: 
                                finalPlan[count].append(classWpreInfo[i][0])
                                currentCredit+=(int(classWpreInfo[i][3]))
                                classWpreInfo[i][1] = True 
                                classTaken+=1
                                tmpClass.append(classWpreInfo[i][0])
        
        #Update the degreeCheck
        if len(tmpClass) != 0:                               
             for i in tmpClass:
                updatePrerequisite(i)
        del tmpClass    

        #left over credit space, fill it with class without prerequisite
        for i in range(len(classWOpre)):       
            if classWOpre[i][1] == False:
               for tmpString in classWpreInfo[i][2]: #quarter match
                    if currentQuarter in tmpString: 
                        if currentCredit + int(classWOpre[i][3]) < maxCredit: #enough credit to take                            
                            finalPlan[count].append(classWOpre[i][0])
                            currentCredit+=(int(classWOpre[i][3]))
                            classWOpre[i][1]=True
                            classTaken+=1
                            
                            #Used for drawing graph
                            classWOfinal[count].append(classWOpre[i][0])
                            
        
       
        creditPerqurter.append(currentCredit)
        # if there is a quarter that no classes are available
        if currentCredit == 0:
            finalPlan[count].append('NoClass') # add NoClass
            classWOfinal[count].append('NoClass')
            catchError.append(currentQuarter)
        
        # Change to next quarter
        if currentQuarter == '1':
            currentQuarter = '2'
        elif currentQuarter == '2':
            currentQuarter ='3'
        elif currentQuarter == '3':
            currentQuarter = '0'
        elif currentQuarter == '0':
            currentQuarter = '1'        
        count += 1 
        
        if len(catchError) > 20:
            print('Unknown Error occurs, Please check your input file again!')
            break
        
        if numbClass==classTakenBefore:
            break                 
     
#It will take the classCode(CSC1230) and update the degreeCheck of each class that has the classCode 
def updatePrerequisite(className):
    current = className
    targetClass = [] # store all the classes that have prerequised of current class
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j >0:
                if classWpre[i][j] == current:
                    targetClass.append(classWpre[i][0])     

    targetClassIndex = [] #store index of targetClass in classCode
    #chagne class code to index number to calcualte the degreeCheck
    for classname in targetClass:
        targetClassIndex.append(classCode.index(classname))
    
    #deduct 1 from degreeCheck related to classCode
    for i in targetClassIndex:
        degreeCheck[i] -= 1
        
    #Check if new degree makes classWpreInfo[?][4] <- prerequisit check , False -> True    
    classFullfilled = []    
    for i in range(len(degreeCheck)):
            if degreeCheck[i] == 0:
                classFullfilled.append(classCode[i])                 
    for i in range(len(classWpreInfo)):
            for j in range(len(classFullfilled)):
                if classWpreInfo[i][0]==classFullfilled[j]:
                   classWpreInfo[i][4] = True                         
     
#Print out the finalPlan       
def printPlan(quarter):
    
    currentQuarter = int(quarter)
    
    print('Schedule with Credit and Starting Quarter')
    print(' ')
    count = 0
    for i in range(len(finalPlan)):
        if currentQuarter%4 == 1:
            print('Fall Quarter: ',creditPerqurter[i],'Credit')
            currentQuarter += 1
        elif currentQuarter%4 == 2:
            print('Winter Quarter',creditPerqurter[i],'Credit')
            currentQuarter += 1
        elif currentQuarter%4 == 3:
            print('Spring Quarter',creditPerqurter[i],'Credit')        
            currentQuarter += 1
        else:
            print('Summer Quarter',creditPerqurter[i],'Credit')
            currentQuarter += 1
            
        for j in range(len(finalPlan[i])):
            print(finalPlan[i][j],end=' ')
            if finalPlan[i][j]!= 'NoClass':
                count+=1
        print(' ')    
        print(' ')  
    print('TotalClass: ',count)
    print('')    
    print('---------------------------------')

def printPlanWO():
    currentQuarter = 1
    
    print('Schedule without Constraint')
    print(' ')
    count = 0
    for i in range(len(chartPlan)):
        if currentQuarter%4 == 1:
            print('Fall Quarter: ',creditPerqurter[i],'Credit')
            currentQuarter += 1
        elif currentQuarter%4 == 2:
            print('Winter Quarter',creditPerqurter[i],'Credit')
            currentQuarter += 1
        elif currentQuarter%4 == 3:
            print('Spring Quarter',creditPerqurter[i],'Credit')        
            currentQuarter += 1
        else:
            print('Summer Quarter',creditPerqurter[i],'Credit')
            currentQuarter += 1
        for j in range(len(chartPlan[i])):
            print(chartPlan[i][j],end=' ')
            if chartPlan[i][j]!= 'NoClass':
                count+=1
        print(' ')    
        print(' ')  
    print('key class(class With Prerequisits): ',count)
    print('')    
    print('---------------------------------')


#Draw actual diagram of user's class schedule(With credit & starting quarters)
def drawClassPlan(quarter,credit):
    
    qName = []
    boxName = [] 
    rmbboxName = []
    for i in range(len(finalPlan)):
        boxName.append([])
        rmbboxName.append([])
        for j in range(len(finalPlan[i])):
            boxName[i].append('box'+str(i))
    
    for i in range(len(finalPlan)):
        qName.append('q'+str(i))
        
        
    currentCredit = int(credit)
        
    if currentCredit > 17:
        d.config(fontsize=11)
    elif currentCredit <=17 and currentCredit > 10:
        d.config(fontsize=10)
    else:
        d.config(fontsize=9)                  
    
    quarterNumb = int(quarter)    
    start = 0
    count = 0
    for i in range(len(finalPlan)):
        
        if quarterNumb % 4 == 1:
            quarter = 'Fall'
            quarterNumb +=1
        elif quarterNumb % 4 == 2:
            quarter = 'Winter'
            quarterNumb +=1
        elif quarterNumb % 4 == 3:
            quarter = 'Spring'
            quarterNumb = 0
        else:
            quarter = 'Summer'
            quarterNumb +=1
        
        if start == 0:     
            begin=d.add(flow.Start(w=7, h=7, color='red',label= 'Start'))
            d.add(flow.Arrow('right',xy=begin.E,l=5))
            qName[i] = d.add(flow.Box(w=9, h=4, E='',W='',S='',label=quarter))
            start += 1        
            
        else:
            d.add(flow.Arrow('right',xy=qName[i-1].E,l=5))
            qName[i] = d.add(flow.Box(w=9, h=4, E='',W='',S='',label=quarter))
        
        downCount  = 0
        downLocation = 0
        
        for j in range (len(finalPlan[i])):
            name = finalPlan[i][j]
            if downCount == 0:
                d.add(flow.Arrow('down',xy=qName[i].S,l=5))
                boxName[i][j]=d.add(flow.Box(w=9, h=4).label(name))
                downCount += 1
                downLocation = j
                
            else:
                d.add(flow.Arrow('down',xy=boxName[i][downLocation].S,l=2))
                boxName[i][j]=d.add(flow.Box(w=9, h=4).label(name))
                downCount += 1
                downLocation = j
              
                   
  
                        
    
    d.draw(show=False) 
    del boxName
    del qName
    del rmbboxName 
 
#Change the classcode into integer form by using it's index, then create topology sort
def TopologySort():


    tmp = [] #have all the classCode, csc1230
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):           
            if classWpre[i][j] not in tmp:
                tmp.append(classWpre[i][j])
                
    nodeNumb = len(tmp)
    createGraph = [[]for i in range(nodeNumb)] # classCode to numbers -- ex) csc1230 ->0, csc2430 ->1 ...
    degreeCheck = [0] * (nodeNumb) # check how many vertex they have -- ex) 1(csc2430) -> 1
    
    #adding inputs into createGraph -- ex) 1->4, [1][4]
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j>0:
                createGraph[tmp.index(classWpre[i][j])].append(tmp.index(classWpre[i][0])) #[i][j]=prerequisite, [i][0]=currentClass -- prerequisite -> currentClass
                degreeCheck[tmp.index(classWpre[i][0])] +=1 #[i][0]=currentClass, add numbers of prerequisites -- ex) 1<--(csc2430) will have value 1 for having 1 prerequisit
    
    sortedList = [] # store index number of topology sorted classWpre list            
    q = deque()
    
    #Find the classes that does have any prerequisit
    for i in range(0, nodeNumb):
        if degreeCheck[i] == 0:
            q.append(i)
            
    while q:
        current = q.popleft()
        sortedList.append(current)
        
        for i in createGraph[current]:
            degreeCheck[i] -= 1
            if degreeCheck[i] == 0:
                q.append(i)

                                           
    for i in range(len(sortedList)):
       classWpreSorted.append(tmp[sortedList[i]])
 
#Printout Topology Sort           
def printTopology():
    #Print out Topology Sort 
    print('Topology Sorted List:')
    for i in range (len(classWpreSorted)):
        if i%5 != 4:
            print (classWpreSorted[i], end='-> ')
        else:
            print (classWpreSorted[i])  

def createPlanWO():

    currentQuarter = '1'
    numbClass= len(classCode)

    count = 0
    classTaken = 0
    

    #While loop until number of class = classTaken
    while classTaken<numbClass:    
        currentCredit = 0  
        tmpClass = []
        chartPlan.append([])
        
        #flowChartInfo        
        for i in range(len(flowChartInfo)):       
            if flowChartInfo[i][1] == False: #class not taken
                    if flowChartInfo[i][3] == True: #Prerequisite fullfilled    
                        for tmpString in flowChartInfo[i][2]: #quarter match
                            if currentQuarter in tmpString: 
                                chartPlan[count].append(flowChartInfo[i][0])
                                flowChartInfo[i][1] = True 
                                classTaken+=1
                                tmpClass.append(flowChartInfo[i][0])
        
        #Update the degreeCheck
        if len(tmpClass) != 0:                               
             for i in tmpClass:
                updateChart(i)
        del tmpClass    
           
        # Change to next quarter
        if currentQuarter == '1':
            currentQuarter = '2'
        elif currentQuarter == '2':
            currentQuarter ='3'
        elif currentQuarter == '3':
            currentQuarter = '0'
        elif currentQuarter == '0':
            currentQuarter = '1'        
        count += 1 
        
        if len(catchError) > 20:
            print('Unknown Error occurs, Please check your input file again!')
            break
        
        if numbClass==classTaken:
            break               
#Printout  
def drawFlowChart():
      
    quarterName = []
    boxName = [] 
    rmbboxName = []
    
    for i in range(len(chartPlan)):
        boxName.append([])
        rmbboxName.append([])
        for j in range(len(chartPlan[i])):
            boxName[i].append('box'+str(i))
    
    for i in range(len(chartPlan)):
        quarterName.append('cond'+str(i))
        
    s.config(fontsize=11)          
    quarterNumb = 1    
    start = 0
    boxLocation = []
    boxFinder = []
    for i in range(len(classCode)):
        boxFinder.append('')
    
    for i in range(len(chartPlan)):
        boxLocation.append([])       
        if quarterNumb % 4 == 1:
            quarter = 'Fall'
            quarterNumb +=1
        elif quarterNumb % 4 == 2:
            quarter = 'Winter'
            quarterNumb +=1
        elif quarterNumb % 4 == 3:
            quarter = 'Spring'
            quarterNumb = 0
        else:
            quarter = 'Summer'
            quarterNumb +=1
        
        if start == 0:     
            begin=s.add(flow.Start(w=7, h=7, color='red',label= 'Start'))
            s.add(flow.Arrow('right',xy=begin.E,l=5))
            quarterName[i] = s.add(flow.Box(w=9, h=4, E='',W='',S='',label=quarter))
            start += 1        
            
        else:
            s.add(flow.Arrow('right',xy=quarterName[i-1].E,l=5))
            quarterName[i] = s.add(flow.Box(w=9, h=4, E='',W='',S='',label=quarter))
        

        downCount = 0
        downLocation = 0
        for j in range (len(chartPlan[i])):
            name = chartPlan[i][j]
            nameIndex = classCode.index(name)
            
            if downCount == 0:
                s.add(flow.Arrow('down',xy=quarterName[i].S,l=5))
                boxName[i][j]=s.add(flow.Box(w=9, h=4).label(name))
                boxLocation[i].append(name)
                boxFinder[nameIndex]=boxName[i][j]
                downCount += 1
                downLocation = j                
            else:
                s.add(flow.Arrow('down',xy=boxName[i][downLocation].S,l=2))
                boxName[i][j]=s.add(flow.Box(w=9, h=4).label(name))
                boxFinder[nameIndex]=boxName[i][j]
                downCount += 1
                downLocation = j
                            
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j>0:
                classAt = boxFinder[classCode.index(classWpre[i][j])]
                classTo = boxFinder[classCode.index(classWpre[i][0])]
                s.add(flow.Arrow(color='blue').at(classAt.E).to(classTo.W))                   
        
        
    s.draw(show=True) 

  
def updateChart(className):  
    current = className
    targetClass = [] # store all the classes that have prerequised of current class
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j >0:
                if classWpre[i][j] == current:
                    targetClass.append(classWpre[i][0])     

    targetClassIndex = [] #store index of targetClass in classCode
    #chagne class code to index number to calcualte the degreeCheck
    for classname in targetClass:
        targetClassIndex.append(classCode.index(classname))
    
    #deduct 1 from degreeCheck related to classCode
    for i in targetClassIndex:
        degreeFlow[i] -= 1
        
    #Check if new degree makes classWpreInfo[?][4] <- prerequisit check , False -> True    
    classFullfilled = []    
    for i in range(len(degreeCheck)):
            if degreeFlow[i] == 0:
                classFullfilled.append(classCode[i])                 
    for i in range(len(flowChartInfo)):
            for j in range(len(classFullfilled)):
                if flowChartInfo[i][0]==classFullfilled[j]:
                   flowChartInfo[i][3] = True         
  

#fName=input("Please type the file name: ")
fName = 'data2.txt'
readFile(fName)
seperateClass()
#quarter = input("Please type the starting quarter(ex: 1, 2, 3): ")
#credit = input("Please type the maximum credit per quarter: ")
quarter = '1'
credit = '18'

createPlan(quarter,credit)
createPlanWO()
printPlan(quarter)
printPlanWO()
#TopologySort()
#drawClassPlan(quarter,credit)
#drawFlowChart()

#printTopology()
