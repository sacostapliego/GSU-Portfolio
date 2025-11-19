"""Exercise 1"""

def insertion(arr):
    for j in range(1 , len(arr)):
        #The current number, j, is stored as j
        key = arr[j]
        #Intilizes the element before the key
        i = j - 1
        #Checks if i is in the array, and if it is greater than the key
        while i >= 0 and arr[i] > key:
            #Makes space for the key
            arr[i + 1] = arr[i]
            #Compares prevouis numbers
            i = i - 1
        #Adds the key back to the right place.
        arr[i + 1] = key
    return arr

#Input list provided in the lab instructions
arr = [50, 11, 33, 21, 40, 50, 40, 40, 21]
print(f'Test Input List {arr}')
sortedList = insertion(arr)
print(f"Test Input List After Insertion sort: {sortedList}\n")

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
            print(f'Test input list: {arr}')
            sortedList = insertion(arr)
            print(f"Test Input List After Insertion sort: {sortedList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")
