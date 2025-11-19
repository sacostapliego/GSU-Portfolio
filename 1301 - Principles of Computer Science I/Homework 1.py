# Author: Steven Acosta-Pliego
# Section: 26

# Purpose: Calculate how many dies (individual CPUs) can be cut from a certain wafer size.
# Pre-conditions: The diameter of the wafer (mm) and the area of a single die (mm^2). 
# Post-conditions: The area the wafer (mm^2) and how many dies can be cut.

#Def main - The reason why to def main is to create a nice starting point and keep everything together
def main ():
    #Print out the title/Introductory message - The reason why I print the title is both make the program look clean and make it clear what the program does.
    print ("    *** Slicing Wafers ***")
    #Import math - The reason why we need to import math is for both '.sqrt' and '.pi'
    import math
    #Ask for inputs - Both the diameter of the wafer and the area of a single die is important for the later calculations
    waferDiameter = float(input('What is the diameter? (mm) '))
    dieArea = float(input('What is the area of a single die? (mm^2) '))
    #Space
    print()
    #Calculate the Wafer Area - The Wafer Area can be calculated using the circle formula, using the the diameter (input) and pi
    waferArea = ((math.pi * (waferDiameter) **2)/4)
    #Calculate the Dies Per Wafer - Using the formula provided, and now having all the values, we caluclate how many dies per wafer.
    diesPerWafer = ((waferArea / dieArea) - ((math.pi * waferDiameter) / math.sqrt(2 * dieArea)))
    #Print out results - We than print the result, to provide the user with the correct values and hopefully solve the intial problem.
    print('From a wafer with an area of',round(waferArea, 2), 'square milimeters you can cut', int(diesPerWafer), 'dies.' )
    print("This does not take into account defective dies, alignment markings and test sites on the wafer's surface.")
main ()