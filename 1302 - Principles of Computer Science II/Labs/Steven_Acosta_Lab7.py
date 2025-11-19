def merge_sort(arr, left, right):
    if left < right:
        mid = (left + right) // 2
        #We split the array in half recursively
        #in order to get more simplier arrays to sort.
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        #Now after the dividing process, 
        #they all contain one element.
        
        #Now we start the combing process
        merge(arr, left, mid, right)

def merge(arr, left, mid, right):
    merged_size = right - left + 1
    merged = [0] * merged_size
    #We create the indexs for the arrays.
    #i being the most left
    i = left
    #j being to the right of the middle
    j = mid + 1
    #k is a counter
    k = 0

    #While both i and j are in their respective side.
    while i <= mid and j <= right:
        #If the i index is greater then j index...
        if arr[i] > arr[j]:
            #...place the i index in our merged array at k index, while also increase the i index
            merged[k] = arr[i]
            i += 1
        else:
            #Repeat except if j index is greater than i index
            merged[k] = arr[j]
            j += 1
        #Increase the k index after each iteration
        k += 1
    
    #While there are still elements in the left.
    while i <= mid:
        #Place the i index in the merged array at the k index
        merged[k] = arr[i]
        #Increase both i and k
        i += 1
        k += 1

    #While there are still elemenets in the right.    
    while j <= right:
        merged[k] = arr[j]
        j += 1
        k += 1

    #Set the counter back to zero
    k = 0
    while k < merged_size:
        #Copy each element in the merged array into the origanl array.
        arr[left + k] = merged[k]
        k += 1


nums= [12, 3, 0, 6, 9, 15]

print("Unsorted: ", end="")    
for num in nums:
    print(num, end=" ")
print("\nSorted:   ", end="")    
merge_sort(nums, 0, len(nums) - 1)
for num in nums:
    print(num, end=" ")