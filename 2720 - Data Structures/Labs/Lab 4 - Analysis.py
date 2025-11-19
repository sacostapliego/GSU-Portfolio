"""Exercise 3"""
#Big-O time analysis for selection sort
def selection(arr):
    n = len(arr) # 1 step
    for i in range(n - 1): # n times
        low = i # 1 step
        for j in range(i + 1, n): # n times
            if arr[j] < arr[low]: # 2 steps
                low = j # 1 step
        arr[i], arr[low] = arr[low], arr[i] # 2 steps
    return arr
#Time Complexity: O(n x n) x O(1) = O(n^2)

#Big-O space analysis for selection sort
def selection(arr):
    n = len(arr) # input size: n
    for i in range(n - 1): # 1 space for i
        low = i # no space
        for j in range(i + 1, n):# 1 space for j
            if arr[j] < arr[low]: # no space
                low = j # no space
        arr[i], arr[low] = arr[low], arr[i] # no space
    return arr
#Space Complexity: O(1)

#Big-O time analysis for insertion sort
def insertion(arr):
    for j in range(1 , len(arr)): #arr/n times
        key = arr[j] # 1 step
        i = j - 1 # 1 step
        while i >= 0 and arr[i] > key: # arr/n times
            arr[i + 1] = arr[i] # 1 step
            i = i - 1 # 1 step
        arr[i + 1] = key # 1 step
    return arr
#Time Complexity: O(n x n) x O(1) = O(n^2)

#Big-O space analysis for insertion sort
def insertion(arr):
    for j in range(1 , len(arr)): # 1 space for j
        key = arr[j] # no space
        i = j - 1 # no space
        while i >= 0 and arr[i] > key: # 
            arr[i + 1] = arr[i] #no space
            i = i - 1 # no space
        arr[i + 1] = key # no space
    return arr
#Space Complexity: O(1)

"""
Both the time and space complexity analysis are the same for the Insertion and Selection alogorithms.
Both having a time complexity of O(n^2) and a space complexity of O(1).
"""