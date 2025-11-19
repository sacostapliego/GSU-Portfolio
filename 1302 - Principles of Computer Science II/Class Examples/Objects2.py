class Seat:
    def __init__(self, seatnum):
        self.seat_num = seatnum
        self.name = ''
        self.paid = 0.0

    def reserve(self, cname, amount):
        self.name = cname
        self.paid = amount

    def cancel(self):
        self.name = ''
        self.paid = 0.0

    def is_available(self):
        return self.name == ''
    
    def print_info(self):
        print(f'Seat: {self.seat_num}\nName: {self.name}\nPaid: {self.paid}\n')

total_seats = 5
seats = []
for i in range(total_seats):
    seats.append(Seat(i))
for i in range(total_seats):
    seats[i].print_info()

option = input("Choose one of the options:\nprint\nreserve\ncancel\nexit\n\n")

while option != 'exit':
    if option == 'print':
        seat_num = int(input("Enter your seat number: "))
        name = input("Enter your name: ")
        amount = input("Enter amount paid: ")
        seats[seat_num].reserve(name, amount)
        pass
    elif option == 'reserve':
        seat_num = int(input("Enter seat num: "))
        seats[seat_num].cancel()
        pass
    elif option == 'cancel':
        print('print cancel selected')
        pass
    else:
        print('Invalid input')
    option = input("Choose next option:\nprint\nreserve\ncancel\nexit\n\n")



