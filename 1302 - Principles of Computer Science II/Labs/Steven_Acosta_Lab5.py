#file = open('words.txt','r')
#Had problems with word file, used absoutle path which fixed the problem
file = open("/Users/mrboo/Documents/GSU/2023-24/CSC 1302/Labs/Lab 5/words.txt","r")
words = file.read().splitlines()
print('Number of words read:',len(words))

def binary_seach(arr,target):
    low = 0
    count = 0   #Iteration counter
    high = len(arr) - 1
    while low <= high:
        count += 1
        mid = (low + high) // 2
        if target == arr[mid]:
            print(f"Target = {target}, Found at index = {mid}, Number of iterations = {count}")
            return mid
        elif target < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    print(f"Target = {target}, Found at index = {-1}, Number of iterations = {count}") #NOT FOUND
    return -1
    

target = input('Enter search key: ').lower()

while target != 'exit':
    binary_seach(words,target)
    target = input('Enter search key: ').lower()