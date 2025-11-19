def has_duplicates_word_finder(n, words):
    #Uses the set operator, which checks the unique elements in the list, 
    #If the set counter is less than the length of the list, than that means there ia a duplicate,
    #Which will make the return false
    if len(set(words)) < n:
        return False
    #Otherwise it will be True.
    else:
        return True

def sort_flowers(n, flower):
    #Selection sort
    for i in range(n):
        #Lowest index
        low = i
        for j in range(i + 1, n):
            #Checks j and minimum index, if it is smaller, than the low/minimum is updated to j
            if flower[j] < flower[low]:
                low = j
        #Swaps the current postion for i with the lower number
        flower[i], flower[low] = flower[low], flower[i]
    return flower

def reverse_list(nums):
    #Initilize the start and end
    start = 0
    end = len(nums) - 1

    #While start is less than end...
    while start < end:
        #The elements swap places
        nums[start], nums[end] = nums[end], nums[start]
        #start and end keep getting added and subtracte respectivly till stat<end is met
        start += 1
        end -= 1 

    return nums

"""Duplitcates Test Case"""
falseTest = ["Spring", "Summer", "Fall", "Summer", "Winter"]
trueTest = ["Spring", "Summer", "Fall", "Winter"]

print(f"Duplitcates Case 1: \nInput: {falseTest}\nOutput: {has_duplicates_word_finder(5,falseTest)}\n")
print(f"Duplitcates Case 2: \nInput: {trueTest}\nOutput: {has_duplicates_word_finder(4,trueTest)}\n")

"""Flower Test Case"""
flowerTest = ["Rose", "Lily", "Tulip"]

print(f"Flower Case 1: \nBefore: {flowerTest} \nAfter: {sort_flowers(3,flowerTest)}\n")

"""Reverse Test Case"""
reverseTest = [3, 4, 7, 6, 1]

print(f"Reverse Case 1: \nBefore: {reverseTest}\nAfter: {reverse_list(reverseTest)}\n")

"""Test Cases for Each Function"""

"""
For the Has Duplicates word finder function the user will be asked for enter words which is sepereated by a space.
The input will than be split and appended into a empty list, n will be taken for the length of the list for the input.
The way that it will check if the user does not enter a proper list is through exception.
"""
print("\n\n---To leave each function, press enter.---\n\n")
print("Has Duplicates Word Finder Function")
while True:
    try:
        #User input
        userInput = input("Enter words to place into a list seperated by a space: ")
        #Empty list
        duplicatesList = []
        
        #For each word in the user input after it is split from the space...
        for words in userInput.split():
                #It is added to the empty list
                duplicatesList.append((words))
        #Length of the list
        n = len(duplicatesList)
        #If the user presses enter
        if userInput == '':
            print('')
            break
        #Function is performed
        else:
            print(f"Input: {duplicatesList}\nOutput: {has_duplicates_word_finder(n,duplicatesList)}\n")
    #If what the user enters is not a proper string, than it will provide the following message.
    except:
        print('Error')

"""
For the sorting flowers function it is similar to the has duplicates word finder. However, there is not a way
to check if the user is entering actaul flowers or not.
"""
print("\nSorting Flowers Function")
while True:
    try:
        #User input
        userInput = input("Enter flowers to place into a list seperated by a space: ")
        #Empty list
        duplicatesList = []
        
        #For each word in the user input after it is split from the space...
        for words in userInput.split():
                #It is added to the empty list
                duplicatesList.append((words))
        #Length of the list
        n = len(duplicatesList)
        #If the user presses enter
        if userInput == '':
            print('')
            break
        #Function is performed
        else:
            print(f"Before: {duplicatesList} \nAfter: {sort_flowers(n,duplicatesList)}\n")
    #If what the user enters is not a proper string, than it will provide the following message.
    except:
        print('Error')

"""
Simliar to the first two, however, if the user does not enter numbers than the except will handle that problem.
"""
print("\nReverse List Function")
while True:
    try:
        #User input
        userInput = input("Enter numbers to place into a list seperated by a space: ")
        #Empty list
        duplicatesList = []
        
        #For each word in the user input after it is split from the space...
        for words in userInput.split():
                #It is added to the empty list
                duplicatesList.append(int(words))
        #If the user presses enter
        if userInput == '':
            print('')
            break
        #Function is performed
        else:
            print(f"Before: {duplicatesList} \nAfter: {reverse_list(duplicatesList)}\n")
    #If what the user enters is not a proper number list, than it will provide the following message.
    except:
        print('Error')