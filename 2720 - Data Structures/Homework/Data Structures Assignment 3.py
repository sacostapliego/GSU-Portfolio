"""Task 1"""
def hasBalancedParentheses(s):
    #Empty stack
    stk = []
    #Two sets, opening and closing
    opening = set(['(', '[', '{'])
    closing = {')':'(', ']':'[', '}':'{'}
    #iterates through each character in the string
    for char in s:
        #If char is an opening, than it is pushed into the stack
        if char in opening:
            stk.append(char)
        #If not...
        elif char in closing:
            #Also checks if it empty or the top element does not match the correspoindg element.
            if not stk or stk.pop() != closing[char]:
                #Not balanced
                return False
    #If none, than it has a balanced parathenses.
    return not stk
#Test case
test = [
    "()", 
    "([]{})", 
    "([{}])()", 
    ")", 
    "([)", 
    "()(()]){)}"
]
for i in test:
    print(f"String: '{i}'\nBalanced: {hasBalancedParentheses(i)}\n")
try:
    user = input("Please enter only parathenses: ")
    print(f"String: '{user}'\nBalanced: {hasBalancedParentheses(user)}\n")
except:
    print("Please enter a proper input\n")

#Time complexity: O(n) - the program iterates through each character of the string at once.
#Space complextiy: O(n) - The space being used by the stack

"""Task 2"""
class Calculator:
    
    def postfix(self, tokens):
        #Empty stack
        stk = []
        for token in tokens:
            #Checks if the token is a number, pushed into stack
            if token.isdigit():
                stk.append(int(token))
            #pops two operands from the stack, if the token is one of the 4 operators
            else:
                op2 = stk.pop()
                op1 = stk.pop()
                if token == '+':
                    stk.append(op1 + op2)
                elif token == '-':
                    stk.append(op1 - op2)
                elif token == '*':
                    stk.append(op1 * op2)
                elif token == '/':
                    #integer division
                    stk.append(int(op1 / op2))
        return stk.pop()

#Test cases
calculator = Calculator()
expressions = [
    ["10", "2", "*", "15", "+"],
    ["2", "1", "+", "3", "*"],
    ["4", "13", "5", "/", "+"]
]

for expression in expressions:
    result = calculator.postfix(expression)
    print(f"Expression: {' '.join(expression)} = {result}")

try:
    user = input("Please enter the numbers and operators in the correct format: ")
    tokens = user.split()  # Split the input string into tokens
    result = calculator.postfix(tokens)
    print(f"Expression: {user} = {result}\n")
except:
    print("Please enter a proper input\n")


#Time complexity: O(n) - the program iterates through each character of the string at once.
#Space complextiy: O(n) - The space being used by the stack

"""Task 3"""
class MyLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

def reverseLinkedList(head):
    if not head or not head.next:
        return head
    #Two pointesr
    prev = None
    current = head
    #Iterates through the linked list, 
    while current:
        nextNode = current.next
        current.next = prev
        prev = current
        current = nextNode

    return prev
#Takes ethe head of a linked list as input and prints the values of all nodes in the list
def printLinkedList(head):
    current = head
    while current:
        print(current.value, end=" ")
        current = current.next
#Takes a list of values as input and creates a single linked list with nodes
def createLinkedList(values):
    if not values:
        return None
    head = MyLinkedListNode(values[0])
    current = head
    for value in values[1:]:
        current.next = MyLinkedListNode(value)
        current = current.next
    return head
try:
    if __name__ == "__main__":
        values = list(map(int, input("Please enter numbers seperated by a space: ").split()))
        head = createLinkedList(values)
        reversed_head = reverseLinkedList(head)
        printLinkedList(reversed_head)
except:
    print("Please enter numbers.")

#Time complexity: O(n)
#Space complexity beyond input: O(1)
    
"""The way that I would handle test cases is through exception, I provided exception cases for each of the following tasks."""