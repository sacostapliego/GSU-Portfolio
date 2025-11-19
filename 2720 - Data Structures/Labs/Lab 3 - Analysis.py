"""Exercise 3"""

#Big-O time analysis for bubble sort
def bubble(arr):
    n = len(arr) # 1 step
    for i in range(n - 1): # n times
        for j in range(n - i - 1):  # n times
            if arr[j] > arr[j + 1]: # 2 steps
                arr[j], arr[j + 1] = arr[j + 1], arr[j] #2 steps
    return arr
#Time Complexity: O(n x n) x O(1) = O(n^2)

#Big-O space analysis for bubble sort
def bubble(arr):
    n = len(arr) # input size: n 
    for i in range(n - 1): # 1 space for i 
        for j in range(n - i - 1): # 1 space for j
            if arr[j] > arr[j + 1]: # no space
                arr[j], arr[j + 1] = arr[j + 1], arr[j] # no space
    return arr
#Space Complexity: O(1)

#Big-O time analysis for counting sort
def counting(arr):
    k = max(arr) # 1 step
    count = [0] * (k + 1) # 1 step
    final = [0] * len(arr) # 1 step

    for i in range(len(arr)): # arr/n times
        j = arr[i]  # 1 step
        count[j] += 1 # 1 step

    for i in range(1, k + 1):   # k timess
        count[i] += count[i - 1]    # 1 step
    
    for i in range(len(arr)):   # arr/n times
        j = arr[i]  # 1 step
        count[j] -= 1   # 1 step
        final[count[j]] = arr[i]    # 1 step
    return final
#Time complexity: O(n + k)

#Big-O space analysis for counting sort
def counting(arr):
    k = max(arr) # input size: k
    count = [0] * (k + 1) # no space
    final = [0] * len(arr) # no space

    for i in range(len(arr)): # 1 space for i 
        j = arr[i] # no space
        count[j] += 1 # no space

    for i in range(1, k + 1): # 1 space for i 
        count[i] += count[i - 1] # no space
    
    for i in range(len(arr)): # 1 space for i
        j = arr[i] # no space
        count[j] -= 1 # no space
        final[count[j]] = arr[i] #Space for k
    return final
#Space complexity: O(k)

#Comparion
"""Bubble sort and counting sort both have their advantages and disadvantages. However, when comparing
   the time complexity of the two we can see that counting sort has a better, linear complexity when compared to
   bubble sorts quadratic time complexity. However, the space complexity is a different story, where counting sort
   takes up more space. Therefore, that being said it might be a better option to choose bubble sort when dealing with
   small data, and to choose counting sort for larger due to the time compmlexity."""