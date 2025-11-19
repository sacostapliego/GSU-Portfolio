import heapq

"""Problem 1"""

def bst(lst):
    #Recursive
    def bstCheck(lst, curr):
        #Base case for recursive function
        if curr >= len(lst):
            return True
        
        #If the base case is not met, than it calculates the indices of the left and right children
        left = 2 * curr + 1
        right = 2 * curr + 2

        #Checks if left is exists and if the value is greater than or equal to the current node
        if left < len(lst) and lst[left] >= lst[curr]:
            return False
        
        #Checkf if right ecits and if teh value is greater than or equal to the current node
        if right < len(lst) and lst[right] <= lst[curr]:
            return False
        
        #If neither than it recursively calls bstCheck
        return bstCheck(lst, left) and bstCheck(lst, right)
    
    #The bst(lst) function is called with the input lst, and the result is printed for two example lists
    return bstCheck(lst, 0)

#Examples from lab instructions
example1 = [10, 5, 15, 2, 7, 11, 25, 1]
print("Example One list: ",example1,"\nOutput: ",bst(example1),"\n")

example2 = [2,4,5]
print("Example Two list: ",example2,"\nOutput: ",bst(example2),"\n")

"""One way that I would test multiple cases is through exception, if the user does not enter a proper 
dataset than it would ask them to please entere a proper dataset.
"""

"""Problem 2"""
print("_________________________\n\n")
#Sorting
def solution1(nums, k):
    #Initizlie count
    count = {}
    #Loops
    for num in nums:
        count[num] = count.get(num, 0) + 1

    #Sorting the dictionary by value in decending order
    sortnumber = sorted(count.keys(), key=lambda x: (-count[x], x))
    return sortnumber[:k]

#Examples from lab instructions
example1 = [1,2,1,3,2,2]
print("Sorting example One list: ",example1,"\nOutput: ",solution1(example1,2),"\n")

example2 = [1]
print("Sorting example One list: ",example2,"\nOutput: ",solution1(example2,1),"\n")


"""
The time complexity while calculating the frequency of each element takes O(n), which will make the time copmlexity
O(n), and the space complexity is also O(n) due to the usuage of the dictionary to store the frequencies.
"""

#Priority Queue (Heap)
def solution2(nums, k):
    #Initizile count
    count = {}
    for num in nums:
        count[num] = count.get(num, 0) + 1
    
    #Creating a max heap
    heap = [(-freq, num) for num, freq in count.items()]
    heapq.heapify(heap)
    
    #Extracting top k elements from the heap
    return [heapq.heappop(heap)[1] for _ in range(k)]

#Examples from lab instructions
example1 = [1,2,1,3,2,2]
print("Sorting example One list: ",example1,"\nOutput: ",solution2(example1,2),"\n")

example2 = [1]
print("Sorting example One list: ",example2,"\nOutput: ",solution2(example2,1),"\n")

"""
The time complexity while calculating the frequency of each element takes O(n), which will make the time copmlexity
O(n), while extracting each element takes O(logn), which results in O(klogn) for
extracting the top k elements. Therefore the time complexity is O(n+klogn), while
 the space complexity is also O(n) due to the usuage of the dictionary to store the frequencies and the heap to store the elements.
"""
