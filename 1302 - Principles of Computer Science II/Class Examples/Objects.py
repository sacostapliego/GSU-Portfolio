class Location:
    def __init__(self):
        self.street = ""
        self.unit = ""

work = Location()
work.street = "1 Park Place"
work.unit = "Room 724"

home = Location()
home.street = "Patton Hall"
home.unit = "427"

print(f"Street address: {work.street}\nUnit: {work.unit}")
print(f"Street address: {home.street}\nUnit: {home.unit}\n\n")

########################
class Location:
    def __init__(self, st, ut, ct, zp):
        self.street = st
        self.unit = ut
        self.city = ct
        self.zip = zp

work = Location("Park Place","Room 724","Atlanta","30303")
print(f"Street address: {work.street}\nUnit: {work.unit}\nCity: {work.city}\nZip Code: {work.zip}")
print("\n\n")

#######################
class Car:
    name = 'Toyota'
    def __init__(self, md):
        self.model = md 
camry = Car('Camry')
rav4 = Car("Rav4")

print(camry.name, rav4.name)