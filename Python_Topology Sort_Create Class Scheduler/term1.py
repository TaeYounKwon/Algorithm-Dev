import schemdraw
from fileinput import filename
from schemdraw import flow

dataList = []        # The file that has all the input value
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Name(Data Structure)
                     # 2.Credit ('5')
                     # 3.Pre Requisit (CSC1230)
                     # 4.Quarter ('1,2')                        

classWOpre = []      # Classes without prerequisites
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Taken(True or False)
                     # 2.Quarter('1,2')
                     # 3.Credit                   
                     
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
classCode = []       # Store class code (csc1230)
degreeCheck = []     # Store the number of Prerequisites remained
degreeFlow = []
finalPlan =[]        # 2D list, store final schedule to take the classes 
creditPerqurter = []
chartPlan=[]
#If input value has missing information, stop the while loop in creating plan
catchError = []
     
 
#Read File from user input file, 
def readFile():
    dataList.clear()
    threeChance = 0
    fileNotOpen = True
    
    while(fileNotOpen):
        fileName=input("Please type the file name: ")
        try:
            open(fileName, 'r', encoding='UTF8') or open(fileName, 'rt', encoding='UTF8')
        except FileNotFoundError:
            print('')
            print('----------------------------')
            print("could not open/read the file: ", fileName)
            print('----------------------------')
            print('')
        except OSError:      
            print('')
            print('----------------------------')
            print("could not open/read the file: ", fileName)
            print('----------------------------')
            print('')
        else: 
            fileNotOpen = False
        
        if threeChance == 3:
            print('')
            print('----------------------------------------------------')
            print('Could not find the file, Please check your directory.')
            print('----------------------------------------------------')
            print('')
            quit()             
        
        threeChance += 1    
         

    data = open(fileName, 'r', encoding = 'UTF8') or open(fileName, 'rt', encoding = 'UTF8')    
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

    
       # The file that has all the input value
                     # 0.ClassCode(UCOR1000)
                     # 1.Class Name(Data Structure)
                     # 2.Credit ('5')
                     # 3.Pre Requisit (CSC1230)
                     # 4.Quarter ('1,2')
                
            
    for i in range(len(dataList)):    
        try:
            int(dataList[i][2])
            dataList[i][4]
        except ValueError:
            print('Data has extra comma or invalid input.')
            print('Please check your text file and try again.')
            quit()
        except IndexError:
            print('Data has missing input.')
            print('Please check your text file and try again.')
            quit()
                   
    for i in range(len(dataList)):  
        if len(dataList[i])>5:
            print('Data has extra comma or invalid input.')
            print('Please check your text file and try again.')
            quit()
        elif dataList[i][4].replace(' ','') == '':
            print('Data has missing quarter value.')
            print('Please check your text file and try again.')
            quit()
    
    print('')        
    print('----------------------------')             
    print('File is successfully readed!')   
    print('----------------------------')    
    print('')     
       
        
def findMinCredit():
    maxVal = 0
    for i in range(len(dataList)):
        if int(dataList[i][2])>maxVal:
            maxVal = int(dataList[i][2])
    
    return maxVal                          
            
#Separate DataList into classWpreInfo and classWOpre
def seperateClass():
    
    classWpre.clear()
    classWOpre.clear()
    classCode.clear()
    degreeFlow.clear()
    degreeCheck.clear()
    classWpreInfo.clear()
    flowChartInfo.clear()
    
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
    
    finalPlan.clear()  
    creditPerqurter.clear()
    
    currentQuarter = quarter
    maxCredit=int(credit)
    numbClass= len(classWOpre) + len(classCode)
    count = 0
    classTaken = 0

    #While loop until number of class = classTaken
    while classTaken<numbClass:   
         
        currentCredit = 0   
        tmpClass = []
        finalPlan.append([])
      
        
        #classWpreInfo comes first        
        for i in range(len(classWpreInfo)):       
            if classWpreInfo[i][1] == False: #class not taken
                 if currentCredit + int(classWpreInfo[i][3]) <= maxCredit: #enough credit to take
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
                        if currentCredit + int(classWOpre[i][3]) <= maxCredit: #enough credit to take                            
                            finalPlan[count].append(classWOpre[i][0])
                            currentCredit+=(int(classWOpre[i][3]))
                            classWOpre[i][1]=True
                            classTaken+=1
                            

                            
        
       
        creditPerqurter.append(currentCredit)
        # if there is a quarter that no classes are available
        if currentCredit == 0:
            finalPlan[count].append('NoClass') # add NoClass
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
        
        if len(catchError) > 100:
            print('Unknown Error occurs, Please check your input file again!')
            break
        
        if numbClass==classTaken:
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
   
    outFile = open("output1.txt","w")
    
    currentQuarter = int(quarter)
    print('Schedule with Credit and Starting Quarter')
    print(' ')
    outFile.writelines('Schedule with Credit and Starting Quarter\n\n')
    count = 0
    for i in range(len(finalPlan)):
        if currentQuarter%4 == 1:
            print('Fall Quarter: ',creditPerqurter[i],'Credit')
            outFile.write('Fall Quarter: ')
            outFile.write(str(creditPerqurter[i]))
            outFile.write('Credit\n')
            currentQuarter += 1
        elif currentQuarter%4 == 2:
            print('Winter Quarter',creditPerqurter[i],'Credit')
            outFile.write('Winter Quarter: ')
            outFile.write(str(creditPerqurter[i]))
            outFile.write('Credit\n')
            currentQuarter += 1
        elif currentQuarter%4 == 3:
            print('Spring Quarter',creditPerqurter[i],'Credit')        
            outFile.write('Spring Quarter: ')
            outFile.write(str(creditPerqurter[i]))
            outFile.write('Credit\n')
            currentQuarter += 1
        else:
            print('Summer Quarter',creditPerqurter[i],'Credit')
            outFile.write('Summer Quarter: ')
            outFile.write(str(creditPerqurter[i]))
            outFile.write('Credit\n')
            currentQuarter += 1
        for j in range(len(finalPlan[i])):
            print(finalPlan[i][j],end=' ')
            outFile.write(finalPlan[i][j])
            if finalPlan[i][j]!= 'NoClass':
                count+=1
        print(' ')  
        outFile.writelines('\n\n')      
        print(' ')  
    print('TotalClass: ',count)
    outFile.write('TotalClass: ')
    outFile.write(str(count))
    print('')
    print('-----------------------------------------------------------')
    print('The class plan is successfully save to your file directory!')
    print('Please check output1.txt file in your folder.')
    print('-----------------------------------------------------------')
    print('')
    outFile.close()

def printPlanWO():
   
    outFile = open("output2.txt","w")
    
    currentQuarter = 1
    
    print('Schedule without Constraint')
    outFile.writelines('Schedule without Constraint\n\n')
    print(' ')
    count = 0
    for i in range(len(chartPlan)):
        if currentQuarter%4 == 1:
            print('Fall Quarter: ')
            outFile.writelines('Fall Quarter: \n')
            currentQuarter += 1
        elif currentQuarter%4 == 2:
            print('Winter Quarter: ')
            outFile.writelines('Winter Quarter: \n')
            currentQuarter += 1
        elif currentQuarter%4 == 3:
            print('Spring Quarter: ')
            outFile.writelines('Spring Quarter: \n')        
            currentQuarter += 1
        else:
            print('Summer Quarter: ')
            outFile.writelines('Summer Quarter: \n')
            currentQuarter += 1
        for j in range(len(chartPlan[i])):
            print(chartPlan[i][j],end=' ')
            outFile.write(chartPlan[i][j])
            if chartPlan[i][j]!= 'NoClass':
                count+=1
        print(' ')    
        print(' ')
        outFile.write('\n\n')
    outFile.write('key class(class With Prerequisits): ')
    outFile.write(str(count))
    print('key class(class With Prerequisits): ',count)
    print('')
    print('-----------------------------------------------------------')
    print('The class plan is successfully save to your file directory!')
    print('Please check output2.txt file in your folder.')
    print('-----------------------------------------------------------')
    print('')
    
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
        
    d = schemdraw.Drawing(file='chart1.pdf')    
    d.config(fontsize=32)
    
    quarterNumb = int(quarter)    
    start = 0
    
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
            
    d.save('chart1.jpg',False, 70)
    
    
    print('')
    print('-----------------------------------------------------------')
    print('The flow chart is successfully save to your file directory!')
    print('Please check chart1 in your folder.')
    print('-----------------------------------------------------------')
    print('')
    del boxName
    del qName
    del rmbboxName 
 
def createPlanWO():
    chartPlan.clear()
    currentQuarter = '1'
    numbClass= len(classCode)

    count = 0
    classTaken = 0
    

    #While loop until number of class = classTaken
    while classTaken<numbClass:    
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
    
    
    s = schemdraw.Drawing(file='chart2.jpg')
    s.config(fontsize=32)          
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
           
    s.save('chart2.pdf', False,  72)
    
    print('')
    print('-----------------------------------------------------------')
    print('The flow chart is successfully save to your file directory!')
    print('Please check chart2 in your folder.')
    print('-----------------------------------------------------------')
    print('')
   

  
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
  
def userMenu():

    userOption = 8
    fileReaded = False
    infoAdded = False
    while(userOption!=6):
        
        print('1. Read File')
        print('2. Print class plan WITH Credit and Starting Quarter')
        print('3. Print class plan WITHOUT Credit and Starting Quarter')
        print('4. Draw flow chat of class plan WITH credit and Starting Quarter')
        print('5. Draw flow chat of class plan WITHOUT credit and Starting Quarter')
        print('6. Quit the program')
        userSelect = input('Please type the number(1,2,3...) of options below: ')
        
        
        try:
            if (type(int(userSelect)))==int :
                userOption = int(userSelect)
                pass

        except ValueError:      
          userOption = 8
        
        
        
        print('')    
        
        if userOption == 1:  
            readFile()
            seperateClass()
            createPlanWO()
            fileReaded = True
            infoAdded = False      
            
        elif userOption == 2:
            
            if fileReaded == False:
                print('---------------------------')
                print('Please read the file first!')
                print('---------------------------')
                print('')
            
            else:  
                print('1 - Fall Quarter ')
                print('2 - Winter Quarter ')
                print('3 - Spring Quarter ')
                print('0 - Summer Quarter ')
                quarterPass = True
                while(quarterPass):
                    quarter = input("Please type the starting quarter: ")    
                    try:
                        if int(quarter) == 1 or int(quarter) == 2 or int(quarter) == 3 or int(quarter) == 0:
                                quarterPass = False
                        else:
                            print('Invalid input. Please type the number between 0 - 3')
                            print('')
                    except ValueError:
                        print('Invalid input.')
                        print('')
            
                creditPass = True
                maxCredit = findMinCredit()
            
                while(creditPass):
                    credit = input("Please type the maximum credit per quarter: ")
                    print('')
                    try:
                        if int(credit)<maxCredit:
                            print('The maximum Credit need to be larger than: ',maxCredit)
                            print('')
                        else:
                            creditPass = False    
                    except ValueError:
                        print('Invalid input.')
                        print('')
                    
                seperateClass()
                createPlan(quarter,credit)
                printPlan(quarter)
                infoAdded = True
                        
        elif userOption == 3:
            if fileReaded == False:
                print('---------------------------')
                print('Please read the file first!')
                print('---------------------------')
                print('')
            else:  
                printPlanWO()
            
        elif userOption == 4:
            if fileReaded == False:
                print('---------------------------')
                print('Please read the file first!')
                print('---------------------------')
                print('')            
            elif infoAdded == False:
                print('----------------------------------------------------------------')
                print('Please input starting Quarter and Maximum credit from Option 2!')
                print('----------------------------------------------------------------')
                print('')            
            else:    
                drawClassPlan(quarter,credit)
            
        elif userOption == 5:
            if fileReaded == False:
                print('---------------------------')
                print('Please read the file first!')
                print('---------------------------')
                print('')            
            else:
                drawFlowChart()
            
        elif userOption == 6:
            print('-----------------------------')            
            print('Thanks for using Our Program!')
            print('-----------------------------')
            print('')
        else:
            print('')
            print('---------------------------------')
            print('Invalid Input, please Type Again!')
            print('---------------------------------')
            print('')
        if userOption=='6':
            break      
        '''                      
        '''

userMenu()