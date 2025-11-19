class MinStack:
    def __init__(self) -> None:
        self.stack = []
        self.minStack = []
    #Pushes the element val onto the stack
    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.minStack or val <= self.minStack[-1]:
            self.minStack.append(val)
    #Removes the element on the top of the stack
    def pop(self) -> None:
        if self.stack:
            if self.stack[-1] == self.minStack[-1]:
                self.minStack.pop()
            self.stack.pop()
    #Gets the top element of the stack
    def top(self) -> int:
        if self.stack:
            return self.stack[-1]
    #Retrievres the minimum element in the stack
    def getMin(self) -> int:
        if self.minStack:
            return self.minStack[-1]
        
stack1 = MinStack()
stack1.push(5)
stack1.push(2)
stack1.push(10)

print(stack1.getMin())
stack1.pop()
print(stack1.top())
print(stack1.getMin())
