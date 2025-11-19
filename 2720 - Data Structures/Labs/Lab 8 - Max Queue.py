from collections import deque

class MaxQueue:
    #Set two queues, main and max
    def __init__(self) -> None:
        self.mainQ = deque()
        self.maxQ = deque()

    #Ability to remove queues
    def add(self, value):
        self.mainQ.append(value)
        #Remoces elements from the back of the max queue
        while self.maxQ and self.maxQ[-1] < value:
            self.maxQ.pop()
        #Adds the current value to the max value
        self.maxQ.append(value)
    
    def dequeue(self):
        #Base case
        if not self.mainQ:
            return None
        
        #Removes the front element from the main queue
        removed = self.mainQ.popleft()

        #REmoces the from element from the max queue if it matches the removed
        if removed == self.maxQ[0] and self.maxQ:
            self.maxQ.popleft()
        
        return removed
    
    def maxValue(self):
        if not self.maxQ:
            return None
        return self.maxQ[0]
    
"""Example Test"""
testQueue = MaxQueue()

#Uses the add attribute from the MaxValue class
testQueue.add(1)
testQueue.add(4)
testQueue.add(2)
testQueue.add(3)

#Showcases main queue and max queue lists in reverse order to represent the example shown in the lab instructions and to give an idea on what is happening in the queue.
print(f"Main Queue: {list(testQueue.mainQ)[::-1]} << front of Queue\nMax Queue: {list(testQueue.maxQ)[::-1]} << front of Queue\n-------------\nMax Value: {testQueue.maxValue()}\n")

"""
The way that I would test the following program is through one exception, the use for the first one would be to see if the user
enters a number or not, when the user is given to dequeue, they just need to press space to dequeue the current queue, and press anyother key to exit.
"""
"""User Test/Base Cases"""
userQueue = MaxQueue()
while True:
    try:
        userInput = int(input("Please enter a number to add to queue or '-1' to stop: "))
        #Breaks the user out when they press -1
        if userInput == -1:
            break
        userQueue.add(userInput)
        #Showcases main queue and max queue lists in reverse order to represent the example shown in the lab instructions and to give an idea on what is happening in the queue.
        print(f"Main Queue: {list(userQueue.mainQ)[::-1]} << front of Queue\nMax Queue: {list(userQueue.maxQ)[::-1]} << front of Queue\n-------------\nMax Value: {userQueue.maxValue()}\n")
        
    except:
        print("Please enter a proper number to add to queue")

print("")
while True:
    userInput = (input("Please enter space to dequeue or any other key to exit: "))
    userQueue.dequeue()
    if userInput == "":
        #Uses the deqeueu attribute from the class
        userQueue.dequeue()
        #Showcases main queue and max queue lists in reverse order to represent the example shown in the lab instructions and to give an idea on what is happening in the queue.
        print(f"Main Queue: {list(userQueue.mainQ)[::-1]} << front of Queue\nMax Queue: {list(userQueue.maxQ)[::-1]} << front of Queue\n-------------\nMax Value: {userQueue.maxValue()}\n")

    else:
        break        
