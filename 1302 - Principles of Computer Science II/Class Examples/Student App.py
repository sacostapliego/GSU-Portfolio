from tkinter import Tk, Button, Label, Entry, Text, END, NORMAL, DISABLED, font
import sqlite3
from tkinter.messagebox import showinfo

app = Tk()
app.title("Student Records")
app.geometry('1048x700')

conn = sqlite3.connect('student_rec.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS students (pantherid INTEGER
PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

custom_font = font.nametofont("TkDefaultFont")
custom_font.configure(size=18)

txt = Text(app)
txt.grid(row=5, column=0, columnspan=2)

#3 Labes, 3 Entries, 2 Buttons, 1 Text
pantherid_label = Label(master=app,text='PantherID')
pantherid_label.grid(row=0,column=0)
name_label = Label(master=app, text="Name")
name_label.grid(row=1,column=0)
email_label = Label(master=app,text="Email")
email_label.grid(row=2,column=0)

pantherid_entry = Entry(master=app)
pantherid_entry.grid(row=0,column=1)
name_entry = Entry(master=app)
name_entry.grid(row=1,column=1)
email_entry = Entry(master=app)
email_entry.grid(row=2,column=1)

def onAddStudentBUttonClicked():
    #Step 1:Obtain infro from entry widgets
    pantherid = int(pantherid_entry.get())
    name = name_entry.get()
    email = email_entry.get()

    #Step 2:
    cursor.execute('INSERT INTO Students (PantherID, Name, Email) VALUES (?, ?, ?)',(pantherid,name,email))
    conn.commit()

    pantherid_entry.delete(0,END)
    name_entry.delete(0,END)
    email_entry.delete(0,END)

def onListStudentButtonClicked():
    cursor.execute('SELECT * from Students')
    records = cursor.fetchall()
    txt.delete(0,END)
    for record in records:
        txt.insert(END, f"PantherID: {record[0]} Name:{record[1]} Email:{record[2]}\n")

button_add = Button(master=app, text="Add Student",command=onAddStudentBUttonClicked)
button_add.grid(row=3, column=0, columnspan=2)

button_list = Button(master=app, text='List Students',command=onListStudentButtonClicked)
button_list.grid(row=4, column=0, columnspan=2)


app.mainloop()