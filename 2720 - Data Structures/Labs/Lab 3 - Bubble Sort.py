"""Exercise 1"""

def bubble(arr):
    n = len(arr)
    #Outerloop
    for i in range(n - 1):
        #Innter loop
        for j in range(n - i - 1):
            #If current element is larger than next element...
            if arr[j] > arr[j + 1]:
                #They switch places
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

#Input list provided in the lab instructions
arr = [50, 11, 33, 21, 40, 50, 40, 40, 21]
sortedList = bubble(arr)
print(f"Test Input List: {arr}\nTest Input List After Bubble sort: {sortedList}\n")

#Ensures that the user can put in any input list, however must select enter to end the loop
while True:
    try:
        #Input with instructions for the user to follow
        userInput = (input("Please enter a numbers that are seprated with a space (PRESS ENTER TO EXIT): "))
        
        #Initizlies an empty array
        arr = []

        for number in userInput.split():
            arr.append(int(number))

        #Checks if the user presses enter
        if userInput == '':
            break

        else:
            sortedList = bubble(arr)
            print(f"Test Input List: {arr}\nTest Input List After Bubble sort: {sortedList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")

