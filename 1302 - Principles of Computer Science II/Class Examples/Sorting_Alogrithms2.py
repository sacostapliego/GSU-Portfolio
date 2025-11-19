#Bubble sorting
def bubble(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

#Selection Sort
def selection(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = i   
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]: #change to > to change to decending order
                min_index = j
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

#Insertion Sort
def insertion(arr, n):
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j>= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


nums = [23,11,3,7,12]
print(f"Bubble Sort: {bubble(nums)}")
print(f"Selection Sort: {selection(nums)}")