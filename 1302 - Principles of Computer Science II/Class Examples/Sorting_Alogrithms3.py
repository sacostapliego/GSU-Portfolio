def partition(arr, low, high):
    pivot = arr[high]

    i = low

    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]

    return i

def quick_sort (arr, start, end):
    if start >= end:
        return
    k = partition(arr, start, end)
    quick_sort(arr, start, k - 1)
    quick_sort(arr, k + 1, end)

