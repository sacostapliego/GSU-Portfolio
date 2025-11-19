"""     Exercise 1     """
def deDuplication (user):
    #The maximum value in the list
    maximum = max(user)

    #List counter
    counting = [0] * (maximum + 1)

    #Counts the frequency for each element
    for i in user:
        counting[i] += 1

    #Creates an empty/final list to put the elements in
    final = []
    for i in range(len(counting)):
        if counting[i] > 0:
            final.append(i)

    #Returns the final sorted list, with the removed duplicated items
    return final


test1 = [50, 11, 33, 21, 40, 50, 40, 40, 21]
test2 = [22, 33, 33, 99, 11, 66, 22, 22, 11]
test3 = [10, 10, 10, 10, 10, 62, 23, 19, 99]

print(f"{test1}\n{deDuplication(test1)}\n")
print(f"{test2}\n{deDuplication(test2)}\n")
print(f"{test3}\n{deDuplication(test3)}\n")
