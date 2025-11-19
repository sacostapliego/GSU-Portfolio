#Defines the makelist function
def makelist():
    #Asks for the input from the user to carry out all the functions
    userNum = int(input('Enter number to make a list: '))
    #Creates a for loop in a certain range, 0 and userNum + 1
    list = []
    for i in range (0,userNum):
        #As the loop goes through each number it adds to the list
        list.append(i)
    #Prints the list
    print(list)
makelist()

#Defines the rockcountdown function
def rocketcountdown():
    #Asks for the input from the user to carry out all the functions
    userNum = int(input('Enter Number for Countdown: '))
    #Creates an empty list
    list = []
    #Creates a for loop in a certain range, 0 and userNum + 1
    for i in range (0,userNum + 1):
        #As the loop goes through each number it adds to the list
        list.append(i)
    #Reverses our list
    list.reverse()
    #Removes the final number from the list which is 0
    list.pop(-1)
    #Adds a value at the end of our list which is the statement on the instructions
    list.append("We have lift off!")
    #Prints the list
    print(list)
rocketcountdown()


def doubleloop():
    #Asks for the inputs
    doubleLoopNum1 = int(input("Please enter your first number: "))
    doubleLoopNum2 = int(input("Please enter your second number: "))
    #Creates an empty list
    list = []
    #Creates a nested loop
    for i in range(doubleLoopNum1):
        for j in range(doubleLoopNum2):
            #Appending the list with the proper format
            list.append('{}:{}'.format(i,j))
    #prints out the final list
    print(list)
doubleloop()
