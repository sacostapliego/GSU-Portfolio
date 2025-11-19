"""     Exercise 2     """
#Notes on DeDuplication file on how the
#DeDupilicaion function works.
def deDuplication (user):
    maximum = max(user)
    counting = [0] * (maximum + 1)
    for i in user:
        counting[i] += 1
    final = []
    for i in range(len(counting)):
        if counting[i] > 0:
            final.append(i)
    return final

def binary_search(arr, target):
    #Start
    low = 0
    #"Checks"/iterations
    count = 0
    #End
    high = len(arr)
    while low <= high:
        #Each iteration the counter goes up
        count += 1
        #Middle of the low and high
        mid = (low + high) // 2
        #If the current iteration == targert, than the program ends
        if target == arr[mid]:
            #Prints the message following the lab instructions
            print(f"Integer {target} was found! It was found at index {mid} and it took {count} 'checks.'\n")
            return mid
        #Repeats if not found, if it is too high
        elif target < arr[mid]:
            high = mid - 1
        #Repeats if not found, if it is too low
        else:
            low = mid + 1
        #If nothing is foud
        if low > high:
            print(f"Failed to find the input number.\n")
            return

'''Test Case 1'''
test1 = [50, 11, 33, 21, 40, 50, 40, 40, 21]
sortedTest = deDuplication(test1)
print(f"List before deDuplication: {test1}\nList After: {sortedTest}")
userTest = int(input(f'From the sorted list, please enter an integer to search: '))
binary_search(sortedTest,userTest)

'''Test Case 2'''
test2 = [22, 33, 33, 99, 11, 66, 22, 22, 11]
sortedTest = deDuplication(test2)
print(f"List before deDuplication: {test2}\nList After: {sortedTest}")
userTest = int(input(f'From the sorted list, please enter an integer to search: '))
binary_search(sortedTest,userTest)


'''Test Case 3'''
test3 = [10, 10, 10, 10, 10, 62, 23, 19, 99]
sortedTest = deDuplication(test3)
print(f"List before deDuplication: {test3}\nList After: {sortedTest}")
userTest = int(input(f'From the sorted list, please enter an integer to search: '))
binary_search(sortedTest,userTest)
