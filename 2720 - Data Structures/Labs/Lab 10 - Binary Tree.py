#Create a class, each node has a value, left, and right
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def pre(root):
    #Base
    if root is None:
        return
    #Empty stack
    nodeStack = []
    #Pushes the root node 
    nodeStack.append(root)
    while len(nodeStack) > 0:
        #Pops a node from the stack
        node = nodeStack.pop()
        #Prints the value
        print(node.val, end=" ")
        #Popped node has a right, pushes the right child onto the stack
        if node.right is not None:
            nodeStack.append(node.right)
        #Popped node has a left, pushes the left child onto the stack
        if node.left is not None:
            nodeStack.append(node.left)

def inorder(root):
    #Base
    if root is None:
        return
    #Empty stack
    nodeStack = []
    #current node to the root
    currentNode = root
    #While current node is not none and there are nodes in the stack
    while currentNode is not None or len(nodeStack) > 0:
        #Traverses down the left child chain starting from current 
        while currentNode is not None:
            #Pushes each node onto the stack
            nodeStack.append(currentNode)
            currentNode = currentNode.left
        currentNode = nodeStack.pop()
        #Prints the value
        print(currentNode.val, end=" ")
        #Moves to the right
        currentNode = currentNode.right

def post(root):
    #Base case
    if root is None:
        return
    #Recursively calls the post function on the left and right
    post(root.left)
    post(root.right)
    #Prints as part of the post-order traversal
    print(root.val, end=" ")

#Sample
root = TreeNode(4)
root.left = TreeNode(2)
root.right = TreeNode(6)
root.left.left = TreeNode(1)
root.left.right = TreeNode(3)
root.right.left = TreeNode(5)
root.right.right = TreeNode(7)

#Testing the sample
print("Pre-order Traversal:", end=" ")
pre(root)
print("\nIn-order Traversal:", end=" ")
inorder(root)
print("\nPost-order Traversal:", end=" ")
post(root)

"""The way that I would test different cases is through exception, the user must choose one of the following
   tasks to return the given traversal."""

try:
    userInput = input("Please enter one of the following\n------\nPre-order Traversal = p\nIn-order Traversal = i\nPost-order Traversal = t\n------\n")
    if userInput == 'p':
        pre(root)
    elif userInput == 'i':
        inorder(root)
    else:
        post(root)
except:
    print("Please enter proper command")