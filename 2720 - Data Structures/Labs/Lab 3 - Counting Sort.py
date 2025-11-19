"""Exercise 2"""

def counting(arr):
    #Maximum value 
    k = max(arr)
    #Intialize the count array
    count = [0] * (k + 1)
    #Initiailze the final array
    final = [0] * len(arr)

    #Counts the amount of times an element is shown up in the array
    for i in range(len(arr)):
        j = arr[i]
        #Counter goes up
        count[j] += 1

    #The count array is than modified to show the cumulative count
    for i in range(1, k + 1):
        count[i] += count[i - 1]
    
    #Starts from 0 and goes up the len of the array to create the final array
    for i in range(len(arr)):
        j = arr[i]
        count[j] -= 1
        final[count[j]] = arr[i]

    return final

#Input list provided in the lab instructions
arr = [50, 11, 33, 21, 40, 50, 40, 40, 21]
sortedList = counting(arr)
print(f"Test Input List: {arr}\nTest Input List After Couting sort: {sortedList}\n")

#Same code from exercise 1 for a user to give any array.
while True:
    try:
        #Input with instructions for the user to follow
        userInput = (input("Please enter a numbers that are seprated with a space (ENTER SPACE TO EXIT): "))
        #Initizlies an empty array
        arr = []
        #Splits the numbers in the input from the space
        for number in userInput.split():
            arr.append(int(number))
        #Checks if the user presses enter
        if userInput == '':
            break
        else:
            sortedList = counting(arr)
            print(f"Test Input List: {arr}\nTest Input List After Couting sort: {sortedList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")
