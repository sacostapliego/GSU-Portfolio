#imports the heapq module
import heapq

def kbiggest(lst, k):
    #Creates a minheap with the size of k
    heap = lst[:k]
    heapq.heapify(heap)

    #Iterate through the rest of the numbers
    for i in lst[k:]:
        #If the current index is larger than the smaller number...
        if i > heap[0]:
            #Replaces the smallest with the current index
            heapq.heappop(heap)
            heapq.heappush(heap, i)
    #The kth element will be returned
    return heap[0]

example = [1, 3, 2, 5, 6]
k = 2
print(example)
print("k = ",kbiggest(example, k),"\n")

#Time complexity: O(nlogk)
    #It is O(k) when creating the heap, and O((n-k)logk). beacuase it goes through the remaning list of the input list.
    #Therefore the time complexity is O(nlogk).
#Space complexity: O(k)
    #The space complexity is O(k) is because it stores the k largest element

"""
The way that I would test what the user would enter is through exception, if the user does not
enter the right data, than it would return an error message.
"""

try: 
    #User inputs the list and the key
    user = input("Please enter your numbers sepearted by a space: ")
    userk = int(input("Please enter your key: "))
    #Empty user list
    userlist = []

    #Enter the user data into a empty list
    for num in user.split():
        userlist.append(int(num))

    #Prints the user data
    print(userlist)
    print("k = ",kbiggest(userlist, userk))
except:
    print("Please enter numbers only.")