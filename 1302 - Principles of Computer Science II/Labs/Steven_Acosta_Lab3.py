class Location():
    #Constructor: Assign variables x and y
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    #Less than or equal to operator
    def __lt__(self, other):
        #Checks if the variables x and y and less than or equal to
        #the other location x and y 
        if (self.x <= other.x) and (self.y <= other.y):
            return True
        else:
            return False
        
    #Greater than or equal to operator
    def __ge__(self, other):
        #Checks if the variables x and y and greater than or equal to
        #the other location x and y 
        if (self.x >= other.x) and (self.y >= other.y):
            return True
        else:
            return False

    #Equal to operator
    def __eq__(self, other):
        #Checks if the values of x and y are the same as the values of x and y
        #at the other location
        if (self.x == other.x) and (self.y == other.y):
            return True
        else:
            return False

#Driver code/Test case
loc1 = Location(3,4)
loc2 = Location(5,8)
print(loc1 == loc2)
print(loc1 <= loc2)
print(loc1 >= loc2)