import sqlite3
conn = sqlite3.connect('cs_dept.db')
cursor = conn.cursor()

#cursor.execute(command)

command = 'CREATE TABLE IF NOT EXISTS STUDENTS (\
    PantherID INTEGER PRIMARY KEY,\
    NAME TEXT,\
    EMAIL TEXT\
    )'

cursor.execute(command)

command = "INSERT INTO Students Values (0001, 'A B', 'ab1@student.gsu.edu')"
cursor.execute(command)
command = "INSERT INTO Students Values (0002, 'A B', 'ab1@student.gsu.edu')"
cursor.execute(command)
command = "INSERT INTO Students Values (0003, 'A B', 'ab1@student.gsu.edu')"
cursor.execute(command)

#Update operations
"""command = "UPDATE <table_name> SET <col> = <new val> Where <?>"""
command = "UPDATE Students SET Email = 'ab3' Where PantherID=1"
cursor.execute(command)

"""
#Where / Between caluse
command = 'SELECT * FROM Students Where PantherID between 2 and 3'
cursor.execute(command)

"""

command = 'SELECT * from STUDENTS'
cursor.execute(command)
print(cursor.fetchall())

conn.close