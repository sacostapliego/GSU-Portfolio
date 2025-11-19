#Input of name and age
name = input("What is your name? ")
age = int(input("What is your age? "))
#Checks if they are eligible to vote
if age >= 18:
    print(f"{name}, you can vote.")
else:
    print(f"{name}, you can't vote.")