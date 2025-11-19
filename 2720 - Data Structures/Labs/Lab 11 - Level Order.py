#Tree node program provided
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def level(root):
    #Base case
    if not root:
        return
    
    #Initizlie a queue
    queue = []
    #Appends the root
    queue.append(root)

    while queue: # queue/n times
        #Removes the current element, and assign it to the current node.
        node = queue.pop(0)
        print(node.val, end=" ")
        #Checks if it has a lefet child
        if node.left:
            #If it does, than it is added to the queue
            queue.append(node.left)
        #Checks if it has a right child
        if node.right:
            #If it does, than it is added to the queue
            queue.append(node.right)

#Time complexity: O(n)
    #The reason why the time copmlexity is O(n) is because we go through each node once
#Space complexity: O(n)
    #The reason why the space complexity is O(n) is because if all the nodes are on the same level, the queue will hold all those nodes.

#Sample Binary Tree from lab instructions
root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)
root.right.left = TreeNode(5)
root.right.right = TreeNode(7)

print("Level Order Traversal:", end=" ")
level(root)
print("")

"""The way that I would test the user is whenever they type in a binary tree from input than it would check
   if their input are integers through the user of exception"""

try:
    #Very basic binary tree creation to showcase how to handle test cases, when a user enters the wrong data.
    rootU = int(input('Please enter the root of the value: '))
    leftU = int(input('Please enter the right of the value: '))
    rightU = int(input('Please enter the left of the value: '))
    root = TreeNode(rootU)
    root.left = TreeNode(leftU)
    root.right = TreeNode(rightU)

    level(root)

except:
    print("Please enter a no other than a single digit at a time.")