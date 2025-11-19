#Define a class named node, to represent the node in a linked list
class Node:
    #Initialize a new node 
    def __init__(self, data):
        #Each node has an attribute for next and none
        self.data = data
        self.next = None

#Define a class named LinkedList, to represent the linked list 
class LinkedList:
    #Intitialize a new linked list with a head intially set to none
    def __init__(self):
        self.head = None

    #Appends a new node with the data given
    def append(self, data):
        #Creates a new node
        new = Node(data)
        #Checks if empty
        if not self.head:
            self.head = new
            return
        #pointer
        current = self.head
        #traverse till the last node
        while current.next:
            #Moves the pointer to the next node
            current = current.next
        #Appends the new node to the end of the list
        current.next = new

    #Deletes the n node from list
    def delete(self, n):
        #"dummy" node with 0
        temp = Node(0)
        temp.next = self.head
        #Set two pointers to the head of the list
        fast = slow = temp
        
        #counter
        counter = 0

        #While the counter is less than n then
        while counter <= (n):
            #Advances the fast point
            fast = fast.next
            #Counter is added to one
            counter += 1

        #move both fast and slow until fast reaches the end
        while fast:
            fast = fast.next
            slow = slow.next

        #Removes the n node from the end end by updating the pointer before
        slow.next = slow.next.next

    #Display
    def display(self):
        #Empty list
        final = []
        #Intialize a pointer
        current = self.head
        #Appends the string
        while current:
            final.append(str(current.data))
            current = current.next
        #Seperates the comments
        print(", ".join(final))
    
#Runs the program
linked = LinkedList()
elements = [50, 11, 33, 21, 40, 71]

for i in elements:
    #Appends each item to the link list 
    linked.append(i)

#Calls for the functions in the classes
print(f"Before: ", end="")
linked.display()

n = 2
linked.delete(n)

print("After: ", end="")
linked.display()

"""
THe way that I would go about my test cases is through exceptions, if the user were to input the wrong
number than an error message will appear. Such as the following:
"""

#Exception for the user input
while True:
    try:
        #User inputs the elements needed for the linked list
        userInput = (input("Please enter your elements for the linked list, please seperate each element with a space: "))
        #As long as the number for n
        nInput = (input("Please enter which number to remove from the linked list: "))
        #Empty list
        userElements = []
        #Add to the list
        for element in userInput.split():
            userElements.append(int(element))
        #If the user pressses enter
        if userInput == '':
            break

        #Else the program will run fine.
        else:
            #Takes the user entered data and repeats as the previous test code
            userLinked = LinkedList()
            for i in userElements:
                userLinked.append(i)

            print("Before: ", end="")
            userLinked.display()

            userLinked.delete(int(nInput))

            print("After: ", end="")
            userLinked.display()
    #If the user enters the wrong numbers, strings, or a large n then an error message will appear.
    except:
        print("Error")