import numpy as np

#Operation 1
arr = np.full((4,5),0)
print(arr,"\n")

#Operation 2
arr = np.insert(arr,1,7,0)
print(arr,"\n")

#operation 3
arr = np.insert(arr,1,5,1)
print(arr,"\n")

#Operation 4
arr = np.delete(arr,0,0)
print(arr,"\n")

#Operation 5
arr = np.delete(arr,0,1)
print(arr,"\n")

#Ooperation 6
arr = np.sort(arr,0)
print(arr,"\n")

#Operatoin 7
arr = np.ravel(arr, order='C')
print(arr)