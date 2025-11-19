class Vechicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    
    def get_info(self):
        print("Make: {0}, Model: {1}, Year: {2}".format(self.make,self.model,self.year))

    def __it__(self,other):
        if self.year < other.year:
            return True
        else:
            return False

    
class Car(Vechicle):
    def __init__(self, make, model, year, num_doors):
        Vechicle.__init__(self, make, model, year)
        self.num_doors = num_doors
        
    def honk(self):
        print("Honk! Honk! From Car.")
    
    def get_info(self):
        return("Make: {0}, Model: {1}, Year: {2}, Doors: {3}".format(self.make,self.model,self.year,self.num_doors))
    
class Motorcycle(Vechicle):
    def __init__(self, make, model, year, type):
        Vechicle.__init__(self, make, model, year)
        self.type = type
    
    def honk(self):
        print("Honk! Honk! From Motorcycle")
    
    def get_info(self):
        return("Make: {0}, Model: {1}, Year: {2}, Type: {3}".format(self.make,self.model,self.year,self.type))

class Truck(Vechicle):
    def __init__(self, make, model, year, capacity):
        Vechicle.__init__(self, make, model, year)
        self.capacity = capacity
    
    def honk(self):
        print(f"Honk! Honk! From {self.make}.")
    
    def get_info(self):
        return("Make: {0}, Model: {1}, Year: {2}, Capacity: {3}".format(self.make,self.model,self.year,self.capacity))
    
    def __lt__(self,other):
        if (self.capacity < other.capacity):
            return True
        else:
            return False

class PickupTruck(Truck,Car):
    def __init__(self, make, model, year, capacity, num_doors, has_cover):
        Car.__init__(self, make, model, year, num_doors)
        Truck.__init__(self, make, model, year, capacity)
        self.has_cover = has_cover
    
    def get_info(self):
        if self.has_cover == True:
            self.has_cover = "Yes"
        else:
            self.has_cover = "No"
        return("Make: {0}, Model: {1}, Year: {2}, Capacity: {3}, Doors: {4}, Has Cover: {5}".format(self.make,self.model,self.year,self.capacity,self.num_doors,self.has_cover))

#Driver Code
vechicle1 = Car("Honda","Civic",2013,4)                         #Car
vechicle2 = Motorcycle("Harley","Something",2009,"Cruise")      #Motorcycle
vechicle3 = Truck("Dodge","RAM",2022, 6)                        #Truck
vechicle4 = PickupTruck("Chevy","Silverado",2021,10,4,False)    #Pickup Truck

vechicle1.honk()    #Car
vechicle2.honk()    #Motorcycle
vechicle3.honk()    #Truck
vechicle4.honk()    #Pickup Truck

print(vechicle1.get_info())    #Car
print(vechicle2.get_info())    #Motorcycle
print(vechicle3.get_info())    #Truck
print(vechicle4.get_info())    #Pickup Truck
 
print(vechicle3 < vechicle4)    #Checking Truck < Pickuptruck capacity
