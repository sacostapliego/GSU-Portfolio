"""Exercise 2"""
def selection(arr):
    #Length of the array
    n = len(arr)
    for i in range(n - 1):
        #Lowest index
        low = i
        for j in range(i + 1, n):
            #Checks j and minimum index, if it is smaller, than the low/minimum is updated to j
            if arr[j] < arr[low]:
                low = j
        #Swaps the current postion for i with the lower number
        arr[i], arr[low] = arr[low], arr[i]
    return arr

#Input list provided in the lab instructions
arr = [50, 11, 33, 21, 40, 50, 40, 40, 21]
print(f'Test Input List {arr}')
sortedList = selection(arr)
print(f"Test Input List After Selection sort: {sortedList}\n")

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
            sortedList = selection(arr)
            print(f"Test Input List After Selection sort: {sortedList}\n")
    #However if the users input has a letter in it than the user would be greeted with the following message. 
    except:
        print("Please enter a proper list of numbers to test")

