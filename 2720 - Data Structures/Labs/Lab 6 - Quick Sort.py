#Time complexity: O(nlog(n))

#Pivot
def partition(arr, low, high):
    #Piviot value
    pivot = arr[high] 
    #Initial Pivot index
    i = low
    #Loops from lowest to highest
    for j in range(low, high):
        if arr[j] < pivot:
            #Swaps the elemnets if the condition is true
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    #Swaps the pivot with the element in that postion
    arr[i], arr[high] = arr[high], arr[i]

    #Returns where the piviot is located
    return i

def quick_sort (arr, start, end):
    #Base case
    if start >= end:
        return
    k = partition(arr, start, end)
    #Recursive until base case is met
    quick_sort(arr, start, k - 1)
    quick_sort(arr, k + 1, end)

def deDuplication(arr):
    #Intialize a pointer
    n = 0

    #Starts at one because the first number will always be unique
    for i in range(1, len(arr)):
        #Checks if the current element is different than the pointer
        if arr[i] != arr[n]:
            n += 1
            arr[n] = arr[i]
    
    return arr[:n + 1]

#Input list provided in the lab instructions
arr = [50, 11, 33, 21, 40, 50, 40, 40, 21]
print(f'Test Input List {arr}')
quick_sort(arr, 0, len(arr) - 1)
finalList = deDuplication((arr))
print(f"Test Input List After DeDuplication Program: {finalList}\n")

"""
The way that I would test different cases is similar to last week's lab assigment.
One way that I would my test-cases is through the use of exceptions, where I will have a "try" which would
include my normal code, asking for the user to add a list. Along with an "except" which will detect if the user
does not put the proper input, such as characters rather than numbers.
"""

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
            quick_sort(arr, 0, len(arr) - 1)
            finalList = deDuplication((arr))
            print(f"Test Input List After Selection sort: {finalList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")