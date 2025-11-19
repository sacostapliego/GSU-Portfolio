""" Solution 1 - O(mn)"""
def brute_sort(list1, list2):
    #Create an empty final list
    final = []
    
    #Goes through each number in the 1st list
    for num1 in list1: # m times
        #Goes through each number in the 2nd list
        for num2 in list2: # n times
            #Checks for each iteration, if 1. the numbers are equal 2. if num1 is not already in the final array
            if num1 == num2 and num1 not in final:
                #appends that number into the final list
                final.append(num1)
    
    #Returns the final list
    return final


""" Solution 2 - O(nlog(m))"""
#Binary search alogorithm 
def binary(arr, targert):
    #start
    low = 0
    #End
    high = len(arr)
    while low <= high:
        #Middle of high andn low
        mid = (low + high) // 2
        #If the current iteration equals the target, than the program ends.
        if targert == arr[mid]:
            return mid 
        #If it is too high
        elif targert < arr[mid]:
            high = mid - 1
        #If it is too low
        else:
            low = mid + 1
    #if not found at all than it would return -1
    return -1

def binary_sort(list1, list2):
    #Create an empty final list
    final = []

    #Iterates through, the first list
    for num in list1: # m times - list1
        #Through each iteration of the first list, binary search is usde to look for the current iteration
        #of the current number in list 1, and if it meets the creitera:
        #1. If it doesn't equal -1   2. the number isn't in the final list
        if binary(list2, num) != -1 and num not in final: # log(n) times - list2
            #If it meets crietia, the current number is added into the final list
            final.append(num)
    return final
# O(m) * O(log(n)) = O(m * log(n))


"""     How Solution 2 can be better

    The way that solution 2 can be better is through a time complexity of O(m + n) rather than O(m * log(n)).
    To achieve this time complexity would be to have two iterations traverse at the same time. One way to 
    get this is by implementing two pointers that checks through each iteration. Each poitner compares itself to each other, than 
    if it were to meet the requirements, than it would add itself to the final list.

"""

"""     Test cases problems

    The way that I would check if the user's input list is valid is through the use of exception.
    The try would be the program prompting the user to input their numbers, sepereted by a space, the program
    will then space each of these out and create a list using a for loop. However, if the user were to place anything else
    other than a number, such as a letter or special character, the except: will handle those input errors.

"""

"""Driver code for both implementations"""

lst1 = [1, 5, 6, 9, 9, 9, 11, 11, 21]
lst2 = [6, 6, 9, 11, 21, 21, 21]

print(f"LST1 = {lst1}. Here lenght of LST1 is m.\nLST2 = {lst2}. Here length of LST2 is n\n")

lst = brute_sort(lst1, lst2)
print(f"List returned using brute force method called 'loop-join': {lst}\n")

lst = binary_sort(lst1, lst2)
print(f"List returned using binary search: {lst}\n")