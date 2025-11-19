import math

class Location:
    #TODO: Implement the Location class according to the given UML class diagram and descriptions
    #Constructor: Assigning the x and y value
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Turnign the x,y cordinates into strings
    def __str__(self):
        x = str(self.x)
        y = str(self.y)
        return "({0}, {1})".format(x,y)
class Car:
    #TODO: Implement the Car class according to the given UML class diagram and descriptions
    #Constructor: Assigning the name, location, and cost
    def __init__(self, name, location, cost):
        self.name = name
        self.location = location
        self.cost = cost
    
    #Turing the cost into a string
    def __str__(self):
        cost = str(self.cost)
        return "[{0}, {1}, {2}]".format(self.name,self.location,cost)

    #Changing the x and y variables to the new location.
    def move_to(self, new_x, new_y):
        self.location.x = new_x
        self.location.y = new_y

class Passenger:
    #TODO: Implement the Passenger class according to the given UML class diagram and descriptions
    #Constructor: Assigning the name, location to the Passenger
    def __init__(self, name, location):
        self.name = name
        self.location = location
    
    #Returning the varibles into a string statement.
    def __str__(self):
        return "[{0}, {1}]".format(self.name, self.location)

    #Changing the x and y variables to the new location.
    def move_to(self, new_x, new_y):
        self.location.x = new_x
        self.location.y = new_y


class RideSharingApp:
    #TODO: Implement the RideSharingApp class according to the given UML class diagram and descriptions
    def __init__(self):
        self.car = []
        self.passenger = []

    #Add the given car object to "cars" attribute
    def add_car(self, Car):
        self.car.append(Car)

    #Add the given passenger object to the "passengers" attribute
    def add_passenger(self, Passenger):
        self.passenger.append(Passenger)
    
    #Remove the given car from the "cars" attribute
    def remove_car(self, Car):
        self.car.remove(Car)

    #Remove the given passenger from the "passenger" attribute
    def remove_passenger(self, Passenger):
        self.passenger.remove(Passenger)

    #Finds the cheapest car for the given passenger by comparing 
    #the cost between each car in the "cars" attribute
    def find_cheapest_car(self, Passenger):
        cheapest_car_price = 1
        cheapest_car_name = ''
        for cars in self.car:
            if cars.cost < cheapest_car_price:
                cheapest_car_price = cars.cost
                cheapest_car_name = cars.name
        print(f"Cheapest car for {Passenger.name}: {cheapest_car_name}, Cost per mile: {cheapest_car_price}")

    #Finds the nearest car for the given passenger by comparing the distance
    #between the car and the passenger using the distance formula
    def find_nearest_car(self, Passenger):
        nearest_car_distance = 999
        nearest_car_name = ''
        for cars in self.car:
            distance = math.sqrt(((cars.location.x - Passenger.location.x)**2)+((cars.location.y - Passenger.location.y)**2))
            if distance < nearest_car_distance:
                nearest_car_distance = distance
                nearest_car_name = cars.name
        print(f"Nearest car for {Passenger.name}: {nearest_car_name}, Distance: {nearest_car_distance:.2f}")

#For the remaining code (after this line), no modification is required
print('---------------------Object creation------------------')
location1 = Location(2,1)
location2 = Location(-4,1)
car1 = Car('car1', location1, 0.61)
car2 = Car('car2', location2, 0.50)
print('Car object 1 created:',car1)
print('Car object 2 created:', car2)

location3 = Location(-2,3)
location4 = Location(0,0)
passenger1 = Passenger('passenger1', location3)
passenger2 = Passenger('passenger2', location4)
print('Passenger object 1 created:', passenger1)
print('Passenger object 2 created:', passenger2)

mobileApp = RideSharingApp()
mobileApp.add_car(car1)
mobileApp.add_car(car2)
mobileApp.add_passenger(passenger1)
mobileApp.add_passenger(passenger2)
print('-----------------------Scenario 1---------------------')
mobileApp.find_cheapest_car(passenger1)
mobileApp.find_cheapest_car(passenger2)
mobileApp.find_nearest_car(passenger1)
mobileApp.find_nearest_car(passenger2)

print('-----------------------Scenario 2---------------------')
car1.move_to(0,-5)
passenger1.move_to(0,3)
print('car1\'s location has been updated:',car1)
print('passenger1\'s location has been updated:', passenger1)
mobileApp.find_cheapest_car(passenger1)
mobileApp.find_cheapest_car(passenger2)
mobileApp.find_nearest_car(passenger1)
mobileApp.find_nearest_car(passenger2)

print('-----------------------Scenario 3---------------------')
car3= Car('car3', Location(0,2), 0.3)
mobileApp.add_car(car3)
print('New car added:',car3)
mobileApp.find_cheapest_car(passenger1)
mobileApp.find_cheapest_car(passenger2)
mobileApp.find_nearest_car(passenger1)
mobileApp.find_nearest_car(passenger2)