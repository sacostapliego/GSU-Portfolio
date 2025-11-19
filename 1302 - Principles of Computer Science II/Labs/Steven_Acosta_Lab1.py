#input the year
year = int(input("Enter your year: "))
#check if divisible by 4 and NOT divisible by 100
if ((year % 4) == 0) and ((year % 100) != 0):
    print("leap year")
#check if the year is divisible by 400
elif ((year % 400) == 0):
    print("leap year")
#if not any, then not a leap year
else:
    print("Not leap year")