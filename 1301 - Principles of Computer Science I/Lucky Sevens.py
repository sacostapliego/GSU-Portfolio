"""
In the game of Lucky Sevens, the player rolls a pair of dice.
If the dots add up to 7, the player wins $4; otherwise,
the player loses $1. Suppose that, to entice the gullible,
a casino tells players that there are lots of ways to win: (1, 6), (2, 5), and so on.
A little mathematical analysis reveals that there are not enough ways to win to make the
game worthwhile; however, because many people's eyes glaze over at the first mention
of mathematics, your challenge is to write a program that demonstrates the futility of playing
the game. Your program should take as input the amount of money that the player wants to put
into the pot, and play the game until the pot is empty.
At that point, the program should print the number of rolls it took to break the player,
as well as maximum amount of money in the pot.
"""
"""
Program: Template

Simulate the game of lucky sevens until all funds are depleted.

1) Rules:
       roll two dice
       if the sum equals 7, win $4, else lose $1
2) The input is:
       the amount of money the user is prepared to lose 
3) Computations:
       use a random number generator to simulate rolling the dice
       loop until the funds are depleted 
       count the number of rolls
       keep track of the maximum amount
4) The outputs are:
       the number of rolls it takes to deplete the funds
       the maximum amount 
"""
#Import the random module for the program
import random
#Define the main function
def main():
       #Assign the bet variable to the user inptut
       bet = float(input('How much money are you ready to loose? $'))
       #Sets the rolls and max variable
       rolls = 0
       max = bet
       #While funcition that continues if the current bet is above 0
       while bet > 0:
        #While the bet isn't 0 the two dice get differnt numbers each loop, use the random module
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        #If statment: if the sum equals 7, win $4
        if dice1 + dice2 == 7:
             bet += 4
        #Else: lose $1 
        else:
             bet -= 1
        #If statement that keeps track of the maximum money made
        if max <= bet:
              #Updates the max varible if the current bet is higher than the max
              max = bet
        #Updates the rolls
        rolls += 1
       #Prints the outputs in messages that match their variable
       print(f"The number of rolls it takes to lose it all: {rolls} rolls")
       print(f"The maximum amount you had: ${max:.2f}")
main()