"""     Exercise 1     """
#Function to make sure that the user input is not blank
def PersonalizedHelloWorld(userInput):
    #Checks if the user input is blank/ENTER is pressed
    if userInput == '':
        userInput = input("Please enter your name: ")
        #A loop will occur till the user enters their name
        return PersonalizedHelloWorld(userInput)
    else:
        print(f"Hello, {userInput}!")

#Driver code
userInput = input("What is your name? ")
PersonalizedHelloWorld(userInput)
