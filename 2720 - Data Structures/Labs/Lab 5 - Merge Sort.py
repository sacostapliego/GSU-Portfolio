#Time Complexity: O(nlog(n))
def merge(arr):
    #Checks the length, if it is 0 or 1 than it is already sorted
    if len(arr) > 1:
        #Middle of the unsorted array
        mid = len(arr) // 2
        #Split into two halves using slicing
        left = arr[:mid]
        right = arr[mid:]

        #Recursive for both halves
        merge(left)
        merge(right)

        #Intilizes the pointers to 0
        i = 0
        j = 0
        k = 0

        #Goes through both the left and right halves
        while i < len(left) and j < len(right):
            #If left is greater than right
            if left[i] < right[j]:
                #Left is placed in array
                arr[k] = left[i]
                i += 1
            #If right is greater than left
            else:
                #Right is placed in array
                arr[k] = right[j]
                j += 1
            #Next...
            k += 1

        #Remaining numbers from either halves are than placed into the array
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

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
merge(arr)
finalList = deDuplication((arr))
print(f"Test Input List After DeDuplication Program: {finalList}\n")


"""
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
            merge(arr)
            finalList = deDuplication((arr))
            print(f"Test Input List After Selection sort: {finalList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")