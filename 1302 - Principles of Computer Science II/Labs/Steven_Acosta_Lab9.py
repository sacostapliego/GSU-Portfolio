import sqlite3
conn = sqlite3.connect('store_inventory.db')
cursor = conn.cursor()

#Create the database table
command = 'CREATE TABLE IF NOT EXISTS GROCERY (\
    ProductID INTEGER PRIMARY KEY,\
    ProductName TEXT,\
    UnitPrice REAL,\
    Quantity FLOAT\
    )'

#Executes the command
cursor.execute(command)

#Insert 3 products
command = "INSERT INTO Grocery Values (001, 'Egg', '2', '23')"
cursor.execute(command)
command = "INSERT INTO Grocery Values (002, 'Milk', '4', '30')"
cursor.execute(command)
command = "INSERT INTO Grocery Values (003, 'Rice', '19.99', '10')"
cursor.execute(command)

#Prints the entire database
command = 'SELECT * from GROCERY'
cursor.execute(command)
print(cursor.fetchall())

#Prints using the where clause
command = 'SELECT ProductName FROM Grocery Where UnitPrice between 1 and 5'
cursor.execute(command)
print(cursor.fetchall())

#Prints using the sum clause
command = 'SELECT SUM(UnitPrice * Quantity) FROM Grocery'
cursor.execute(command)
print(cursor.fetchall())

#Close
conn.close