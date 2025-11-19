from tkinter import Tk, Entry, Text, END, font, Label, Button, BOTH
import sqlite3
from tkinter.messagebox import showinfo
from datetime import datetime

import csv

# Create the main application window
app = Tk()
app.title('Student Records')
#!!! Update the space so the button can be seen.
app.geometry('900x600')

# Create a custom font with your desired size and other attributes
custom_font = font.nametofont("TkDefaultFont")  # Start with the default font
custom_font.configure(size=18)  # Set the desired font size

# Set the custom font as the default font for the application
app.option_add("*Font", custom_font)

# Connect to the SQLite database and create a cursor
conn = sqlite3.connect('records.db')
cursor = conn.cursor()

# Create a 'students' table in the database if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS students (pantherid INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

# Create and place labels for PantherID, Name, and Email
pantherid_label = Label(master=app, text='PantherID')
pantherid_label.grid(row=0, column=0)
name_label = Label(master=app, text='Name')
name_label.grid(row=1, column=0)
email_label = Label(master=app, text='Email')
email_label.grid(row=2, column=0)

# Create and place entry widgets for PantherID, Name, and Email
pantherid_entry = Entry(master=app)
pantherid_entry.grid(row=0, column=1)
name_entry = Entry(master=app)
name_entry.grid(row=1, column=1)
email_entry = Entry(master=app)
email_entry.grid(row=2, column=1)

# Define a function to handle adding a student record
def on_add_student_button_clicked():
    # Step-1: Obtain info from entry widgets
    pantherid = int(pantherid_entry.get())
    name = name_entry.get()
    email = email_entry.get()

    # Step-2: Insert these info into the database
    cursor.execute('INSERT INTO Students (PantherID, Name, Email) VALUES (?,?,?)', (pantherid, name, email))
    conn.commit()

    # Clear the entry fields
    pantherid_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)

    # Show an information message
    showinfo(message='Student record added to the database...')

# Define a function to list student records
def on_list_student_button_clicked():
    cursor.execute('SELECT * from Students')
    records = cursor.fetchall()
    txt.delete(0.0, END)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    txt.insert(END, f'--- Student list as of {timestamp} ---\n')
    for record in records:
        txt.insert(END, f"PantherID: {record[0]}   Name:{record[1]}   Email:{record[2]}\n")





# Define a new function for seraching a record
def on_search_record_button_clicked():
    try:
        #Gets the pantherID from the entry widget
        pantherid = int(pantherid_entry.get())
        #Selects the entire record from the pantherID that is entered
        cursor.execute('SELECT * FROM Students WHERE PantherID = (?)',(pantherid,))
        #The record is fetch one, the input, instead of fetching all.
        record = cursor.fetchone()
        #The reason why I use if the record is not none is to remove the NoneType error
        if  record != None:
            #Deletes whatever is inside the text widget and makes it blank.
            txt.delete(0.0, END)
            txt.insert(END, "")

            #Insersts the record of which pantherID # the user wanted to search for in the text widget
            txt.insert(END, f"PantherID: {record[0]}   Name:{record[1]}   Email:{record[2]}\n")
        #If the number entered isn't in the data base than...
        else:
            #this message will appear.
            showinfo(message=f'No record was found in PantherID {pantherid}')

    #If the user does not put in any value in the pantherID entry widget than the following message will appear.
    except ValueError:
        showinfo(message='Please enter a PantherID to search for a record.')
        return
    
# Define a new function for deleteing a record.
def on_delete_record_button_clicked():
    try:
        #Gets the pantherID from the entry widget
        pantherid = int(pantherid_entry.get())
        #Selects the entire record from the pantherID that is entered
        cursor.execute('SELECT * FROM Students WHERE PantherID = (?)',(pantherid,))
        #The record is fetch one, the input, instead of fetching all.
        record = cursor.fetchone()

        #Resets the text widget, so if list button is clicked won't show old records
        txt.delete(0.0, END)
        txt.insert(END, "")

        if record != None:
            cursor.execute('DELETE FROM Students WHERE PantherID = (?)',(pantherid,))
            #Commits the message, which will update the database
            conn.commit()
            #Removes the user's input in the entry widget.
            pantherid_entry.delete(0,END)
            #shows msessage if successful
            showinfo(message=f'Sucessfully deleted {pantherid}.')
        #If the number entered isn't in the data base than...
        else:
            #this message will appear.
            showinfo(message=f'No record was found in PantherID {pantherid}')        

    #If the user does not put in any value in the pantherID entry widget than the following message will appear.
    except ValueError:
        showinfo(message='Please enter a PantherID to delete a record')
        return

# Define a new function for updating a record.
def on_update_record_button_clicked():
    try:
        #Gathers the data from all three entry widgets
        pantherid = int(pantherid_entry.get())
        name = name_entry.get()
        email = email_entry.get()

        #Resets the text widget, so if list button is clicked won't show old records
        txt.delete(0.0, END)
        txt.insert(END, "")

        #Selects the pantherID from the database
        cursor.execute('SELECT * FROM Students WHERE PantherID = (?)', (pantherid,))
        record = cursor.fetchone()

        if record != None:
            #Updates the name and email of the selected pantherID (key field)
            cursor.execute('UPDATE Students SET Name = ?, Email = ? WHERE PantherID = ?',(name, email, pantherid))
            #Command is sent to the database
            conn.commit()
            #The entry widgets are than cleared.
            pantherid_entry.delete(0, END)
            name_entry.delete(0, END)
            email_entry.delete(0, END)
            #shows message if successful
            showinfo(message=f'Successfully updated {pantherid}!')
        #If the number entered is not in the database than this message will show
        else:
            showinfo(message=f"No record was found for {pantherid}")

    #If the user does not put in any value in the pantherID entry widget than the following message will appear. 
    except ValueError:
        showinfo(message='Please enter a PantherID, Name, and Email to update a record.')
        return
    
# Define a new function for exporting a file to CSV 
def on_CSV_button_clicked():
    #Selects the entire database
    cursor.execute('SELECT * From Students')
    #The record is fetch all instead of fetch one.
    records = cursor.fetchall()

    if records != None:
        #Creates and opens a new csv file named "students.csv" with the writer
        with open('students.csv','w') as csvfile:
            #Creater the writer
            writer = csv.writer(csvfile)
            #Writes a the entire reocrd for each pantherid in the new csvfile in rows
            writer.writerows(records)
            #Shows that the transfer was successful
            showinfo(message="Succesfully exported to CSV")
    #If anything goes wrong than the message will show up.
    else:
        showinfo(message='Error')




# Create buttons for adding and listing student records
button_add = Button(master=app, text='Add Student', command=on_add_student_button_clicked)
button_add.grid(row=3, column=0, columnspan=1)

button_list = Button(master=app, text='List Students', command=on_list_student_button_clicked)
button_list.grid(row=4, column=0, columnspan=1)




# Create new buttons for search record, delete record, update record, and export to CSV
button_add = Button(master=app, text='Search Record', command=on_search_record_button_clicked)
button_add.grid(row=3, column=1, columnspan=1)

button_list = Button(master=app, text='Delete Record', command=on_delete_record_button_clicked)
button_list.grid(row=4, column=1, columnspan=1)

button_add = Button(master=app, text='Upate Record', command=on_update_record_button_clicked)
button_add.grid(row=3, column=2, columnspan=1)

button_list = Button(master=app, text='Export to CSV', command=on_CSV_button_clicked)
button_list.grid(row=4, column=2, columnspan=1)




# Create a Text widget to display student records
txt = Text(master=app, height=10, width=70)
txt.grid(row=5, column=0, columnspan=3)

# Start the main application loop
app.mainloop()
