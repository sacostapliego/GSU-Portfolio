"""-----Task 1-----"""
print("--- Task 1---")
#Binary tree node
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def inorder(root, result):
    #Checks if it exists
    if root:
        #Recursive for the left child of the current node
        inorder(root.left, result)
        #Appends the node to the result list
        result.append(root.val)
        #Recursive for the right child of the current node
        inorder(root.right, result)

def deleteRoot(root):
    #Base cases
    if root is None:
        return None
    if root.left is None:
        return root.right
    if root.right is None:
        return root.left
    
    #Checks the minium value in the right side
    mini = root.right
    while mini.left:
        mini = mini.left

    #Replaces the root value with the minimum value
    root.val = mini.val

    #Deletes teh node that had the minimum value
    root.right = deleteNode(root.right, mini.val)

    return root

def deleteNode(root, key):
    #Base case
    if root is None:
        return None
    #if the key is less than the value of the current node
    if key < root.val:
        #The key might be in the left side, recursively calls the function
        root.left = deleteNode(root.left, key)
    #If the key is more than the value of the current node
    elif key > root.val:
        #Key might be in the right side, recursively calls the function
        root.right = deleteNode(root.right, key)
    else:
        #If the node has no left child
        if root.left is None:
            #return the right child
            return root.right
        #If the node has no right child
        elif root.right is None:
            #return the left child
            return root.left
        #Has both left and right, find the mini
        mini = root.right
        while mini.left:
            mini = mini.left
        #After finding the minimum value, replaces teh value of the current node with the minimum
        root.val = mini.val
        #recursively calls deletenode to delet ethe node with the minimum value from the right side
        root.right = deleteNode(root.right, mini.val)
    return root

#Example code from assignment
root = TreeNode(4)
root.left = TreeNode(2)
root.right =TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)
root.right.left = TreeNode(5)
root.right.right = TreeNode(7)

#Execute new code
root = deleteRoot(root)
result = []
inorder(root, result)
print(result)

#The way that I would test the program is through exception the following a very basic binary tree creation to showcase 
#what would happen if the user enters the wrong data.

try:
    #Very basic binary tree creation to showcase how to handle test cases, when a user enters the wrong data.
    rootU = int(input('Please enter the root of the value: '))
    leftU = int(input('Please enter the right of the value: '))
    rightU = int(input('Please enter the left of the value: '))
    root = TreeNode(rootU)
    root.left = TreeNode(leftU)
    root.right = TreeNode(rightU)

    new = deleteRoot(root)
    result = []
    inorder(new, result)
    print(result)

except:
    print("Please enter a no other than a single digit at a time.")

"""-----Task 2-----"""
print("\n--- Task 2 ---")
def repeated(s):
    #intitilize two sets
    seen = set() #stores 10 unique letter sequenences
    repeated = set() #stores the ones that have been seen more than once

    #Checks through 10 letter substrings at a time starting  from i
    for i in range(len(s) - 9):
        #takes out a 10 letter substring from the index to i+10
        sub = s[i : i + 10]
        #If the substring is in seen set
        if sub in seen:
            #Added to repeated set
            repeated.add(sub)
        #Else would be added to the seen
        else:
            seen.add(sub)

    #Changes the repeated to a list to print
    return list(repeated)

s1 = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
print(f"DNA input:\n{s1}\nDNA output:\n{repeated(s1)}\n")
s2 =  "AAAAAAAAAAAAA"
print(f"DNA input:\n{s2}\nDNA output:\n{repeated(s2)}\n")
#THe way that I would test the program is through exception, when the user enters the DNA data, it will check if the user enters 
#proper inputs in order for the program to execute properly.
try:
    while True:
        uesrDNA = input("Enter the DNA sequence such as the following\nAAAAACCCCCAAAA\nPlease write here: ")
        if uesrDNA == '':
            break
        else:
            print(f"DNA input:\n{uesrDNA}\nDNA output:\n{repeated(uesrDNA)}\n")
except:
    print("Error in DNA sequence input")