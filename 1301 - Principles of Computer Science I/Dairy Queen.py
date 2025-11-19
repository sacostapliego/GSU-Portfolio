#Author: Steven Acosta-Pliego
#Course: CSCI 1301 - 21021
#Section: 26
#Python Lab 6

'''
    Purpose: offer the user a choice of food items, calculate total bill
    Pre-conditions: user enters 5 or 6 y's or n's depending on desired items(strings)
    Post-conditions: prompts for choices, total bill before (float) and after tip, (float) and parting message.
'''

#Stores teh food values
food_rate = {"Grilled Cheese":7,"Nachos":5,"Chicken":8,"Hamburger":8,"Cheeseburger":10,"Hot Dog":6}

#Calculates the tip rate
tip = 20/100

def main():
    #Sets the bill to 0
    bill = 0
    #Prompts the user with directions on how to answer each question
    print(f"Pleas answer each question with y (yes) or n (no)")
    #Greets the user
    print(f"Welcome to Dairy Queen")

    #Asks the first choise, Grilled Cheese
    grilledCheese = input("Do you want a Grilled Cheese Sandwhich? ")
    if (grilledCheese == 'y'):
        #Extracts the grilled cheese vaule from our food_rate dictionary
        bill+= food_rate["Grilled Cheese"]

    #Asks if the user wants a  nachos
    nachos = input("Do you want a serving of nachos? ")
    if (nachos == 'y'):
        #Extracts the nachos vaule from our food_rate dictionary
        bill+= food_rate["Nachos"]

    #Asks if the user wants a  chicken sandwhich
    chicken = input("Do you want a chicken sandwhich? ")
    if (chicken == 'y'):
        #Extracts the chicken sandwhich vaule from our food_rate dictionary
        bill+= food_rate["Chicken"]

    #Asks if the user wants a  hamburger
    hamburger = input("Do you want a hamburger? ")
    if (hamburger == 'y'):
        #Extracts the hameburger vaule from our food_rate dictionary
        bill+= food_rate["Hamburger"]
        #Asks the user if he would like cheese on that
        cheeseburger = input("Do you want cheese on that? ")
        if (cheeseburger == 'y'):
            bill+= 2

    #Asks if the user wants a hotdog
    hotdog = input("Do you want a hotdog? ")
    if (hotdog == 'y'):
        #Extracts the hotdog vaule from our food_rate dictionary
        bill+= food_rate["Hot Dog"]

    #Prompts the user with the bill
    print(f"Your total for your food is ${bill}")

    #Gives the user the total bill with 20% tip rate and rounds up to two decimal points if needed
    print(f"The total with {tip * 100}% tip is ${round(bill*tip+bill,2)}")

    #Gives the user a thank you message
    print("Thank you for your business!")
main()