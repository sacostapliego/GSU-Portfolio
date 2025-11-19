from tkinter import Tk, Entry, Text, END

#Creates the app, title, and the size
app = Tk()
app.title("Lab 10")
app.geometry('300x150')

#Creates the entry widget
entry_widget = Entry(app)
entry_widget.pack(side="top")

#Creates the text widge
text_widget = Text(app)
text_widget.pack(side="bottom")

#Key Function
def key_function(record):
    #Adds the recoreded key to a cursor
    cursor = record.keysym

    #Checks if it is a non-aplhanumeric key
    if len(cursor) > 1:
        #Insert the message to the text widget if true... 
        text_widget.insert(END, "It is a non-aphanumeric key.\n")

    #Checks if the key is a upper letter
    elif cursor.isupper():
        #Insert the message to the text widget if true... 
        text_widget.insert(END, "It is a uppercase letter.\n")

    #Checks if the key is a lower letter
    elif cursor.islower():
        #Insert the message to the text widget if true... 
        text_widget.insert(END, "It is a lowercase letter.\n")

    #Checks if the key is a digit
    elif cursor.isdigit():
        #Insert the message to the text widget if true... 
        text_widget.insert(END, "It is a number.\n")

#Entry widget key bind
entry_widget.bind("<Key>",key_function)

app.mainloop()