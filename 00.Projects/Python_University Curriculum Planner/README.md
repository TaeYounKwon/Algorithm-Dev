# Creating a Flowchart

Here you will describe your term project. Remember to write your names.
[More detailed instructions here](Flowchart-Graph.pptx)

You will need to include in this repository:
- `major1.txt` contains the courses a student needs to take to fulfill one major
- `major2.txt` contains the courses a student needs to take to fulfill another major
- The source code of your program

This document should be organized as follows:

# Creating a Flowchart from a Dependency List
A work by: McDonald Berger and Igor Tzankoven

In this programming project, we worked with various softwares, data structures, and algorithms we have learned throughout our student careers. The goal of this project was to learn to choose the most efficient ways to implement a program while also gaining real world experience. 

With this project, we got a feel for solving a real-world problem and learning to work in a group environment. Along with that, we gained valuable knowledge about using third-party libraries, graphs, and time complexity.

There was a lot of planning, testing, and team meetings to be able to properly and successfully execute the program.


## Description


Our program will be reading a text file that will contain a list of school courses. The information received from the files will be in this format: 
CSC 1230, Problem Solving and Programming, 5, [], [1,2,3]. 

The program will take the data from a .txt file and save the information:
- Course code
- Course name
- Credits
- Requirements
- Quarters offered

After the program will create two 2D lists that will have classes with prerequisites(classWpreInfo) and classes without prerequisites(classWOpre). Both lists save the information like this: 
- Course code('CSC1230')
- Class Taken(False)
- Quarter('1,2')
- Credit('5')
- Prerequisite fullfilled(False)

With this information we will create text outputs and graphs to help visualize the courses students will be expected to take. Each quarter is represented using a different number:

-	Summer quarter as a 0
-	Fall quarter as a 1
-	Winter quarter as a 2
-	Spring quarter as a 3. 

This information is crucial for our project since we will be grouping the classes by quarters offered in the text output and graph we will create that will include constraints. Another constraint to consider will be the minimum and maximum number of credits that can be taken per quarter. 

Overall, our project has two text outputs, one representing courses with the prerequisites and another text output showing the courses with constraints. We also have two graphs one showing the sequence of the courses with constraints and one flowchart that is built with the classes with prerequisites. 


## Requirements
The program uses 'SchemDraw' to visualize our data and create the flow chart. To install ShcemDraw, users need to follow the steps described below.
For the programming language we used python so you will also need to have python installed. The code was written and tested on python version 3.8.8. Therefore, equal or higher version of python is mandatory to operate our program.

Steps to follow to make program work: 

- Make sure python installed by doing: pyhton3 --version. If installed you will get this output: 
    ![image](https://user-images.githubusercontent.com/71113179/158252427-2ed55f72-1023-4e7c-80f7-5c82d294bd31.png)
    
    If not installed make sure to install before moving forward.

- Check that you have pip command line to install software packages like schemdraw. You can do this by adding this command:
    ![image](https://user-images.githubusercontent.com/71113179/158253068-6ebb809c-9f78-44b2-b7ab-590794cadee2.png)
    If not installed you will have to install by running this command: sudo apt install python3-pip
    
    Once installed you make sure to double check again that it was successfully completed by doing: pip3 --version and you should get this ouput. 
    ![image](https://user-images.githubusercontent.com/71113179/158253660-874ecc3d-a06e-44bc-b314-0b1d9e4a0bc4.png)

- Once you have made it to this point you can install schemdraw! Install by adding comman: pip install schemdraw
    If installed correctly you will see this message: 
    
![image](https://user-images.githubusercontent.com/71113179/158253902-66f43c60-e538-43bc-897d-4644f11c1fa5.png)


- Lastly, for schemdraw to work at its best you need to also install matplotlib which is another python library for animated and interactive visualizations. You install this by typing this command: sudo apt-get install python3-matplotlib


 After all previous steps have been completed you are ready to go to the directory where your code is!!!

*The requirements of the program, i.e. Python 3.1, what libraries are needed*

## User Manual

    
*Once a person clones this into their computer how the person is supposed to run the program, add screenshots showing how your program works, also add here the link to the Youtube video showing the program running*

Yay, you have made it to this point! 

- Now, that you have all the libraries needed to successfully execute the code you will need to go into the directory that you have the files saved. Here is an example of a path to access the folder with the program and files needed: 

![image](https://user-images.githubusercontent.com/71113179/158477576-37d00c20-78c8-4c77-ad6d-4b5b1662c62b.png)
 
- Once inside the folder open the program by typing python3 filename.py as shown below: 

![image](https://user-images.githubusercontent.com/71113179/158479665-865bee81-023e-4114-8e70-1552b90fe6ca.png)

   As shown in the picture from this point you can start looking at the options avaible to you! Now, lets dive in deeper to the program and start displaying some flowcharts!
   
- The first option is the most important which is to read a file! So, start out by choosing option 1 and inputing the text file name to make sure to read the data.
       ![image](https://user-images.githubusercontent.com/71113179/158480847-ad9b06cb-8615-4c88-9262-fb34cee0cdf1.png)
       
       If read successfully you will get a message letting you know and can continue with the next step.
 
For options 3 and 5 which create the text output and flowchart without constraints you can access it without having to choose option 2. Option two requires input starting quarter and maximum credits which is used for option 2 and option 4. 

- Lets start with option 3. If you choose option 3 you will get these outputs which will show the schedule without contraints and total number of classes. It will also save the plan into the folder called "output2" to be accessed at any time: 

     ![image](https://user-images.githubusercontent.com/71113179/158482126-5a6d20fb-66d5-4e5e-80ba-8ac22e9b6a8b.png)
     ![image](https://user-images.githubusercontent.com/71113179/158482219-3e35580f-2afc-426b-9ac0-ca820bda5cfe.png)
     ![image](https://user-images.githubusercontent.com/71113179/158482546-af085c2b-b9bf-4adb-bc99-72907385f577.png)
 
- Now, if we go with option 5 this is the output you will see: 
      ![image](https://user-images.githubusercontent.com/71113179/158483887-bebc3753-87dd-4709-a807-ebfccd7acf95.png)

    With this option the flowchart is saved directly into the folder and you will have to access it from there by just clicking on the pdf file.
    ![image](https://user-images.githubusercontent.com/71113179/158484017-73bd7262-8674-42f2-94c3-f954a7be7729.png)

- Moving forward we will choose option 2. Once we input the two required fields we will once again have the schedule displayed but this time with the constraints in consideration. The class plan will also be saved to the local folder called "output1".
    
    The process will look like this: 
    ![image](https://user-images.githubusercontent.com/71113179/158484698-79149e31-74a8-417d-a397-d1183efe2a1a.png)
    ![image](https://user-images.githubusercontent.com/71113179/158486270-f334ab4b-3ffe-4d18-91dd-8886b3524b05.png)


- Finally, we will choose option 4. With option 4 since we already have the text file, the start quarter, and the max credits inputted we no longer have to do anything else but select option 4 which will look like this. 

    ![image](https://user-images.githubusercontent.com/71113179/158485100-d2fe9c90-5bdf-4676-8d58-330725f090f2.png)
    
    The flowchart is also saved in folder and can be accessed by just a click! 
    ![image](https://user-images.githubusercontent.com/71113179/158485326-092373ca-a7b6-4363-909b-b727919bad84.png)

    Note: to access option 4 you will need to always do option 2 first or you will not be able to print out the flowchart and will get this message: 
    ![image](https://user-images.githubusercontent.com/71113179/158486081-829e781c-e27c-4004-ae05-ee6f6ce346e7.png)


- To exit you just simply choose option 6 and you are done with the program!

- Here is the YouTube link of How to run our code in Ubuntu terminal: https://www.youtube.com/watch?v=bgT0-F493cw&feature=youtu.be

## Reflection
We learned how to work together to achieve a big project like this throughout this project. We achieved this task because we continuously gathered to talk about this project and update and fix the errors while writing the code. We also learned lots of new algorithms, techniques, and skills during the project. For example, we learned how to use various third-party libraries from python. We also learned the concepts of topology sort and how to implement that knowledge into our project. 



