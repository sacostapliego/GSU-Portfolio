import csv
import time

def chooseOption():
    print('--- --- --- Main Menu --- --- ---')
    option = input('Choose option:\n' \
         '[1] Create new text file\n' \
         '[2] Read text file content\n'
         '[3] Append to text file\n'
         '[4] Search text file\n' \
         '[5] Export to CSV\n' \
         '[6] Exit program\n'
         'option = ')
    return option

option = chooseOption()
while option != '6':
    if option == '1': #Create
        try:
            #User input for name of text file
            new_name = str(input("Type in the name of the file: "))
            #Add ".txt" to ensure that a text file is created and not a regular file
            new_name += ".txt"
            with open(new_name, 'w') as f:
                #Create a new file
                f.write('')
            print("Created a new text file!")
        #If any errors occur than this message will appear
        except:
            print("An error occurred during the CREATE operation!")

    elif option == '2':  # Read
        try:
            #User input for name of text file
            read_name = str(input("Type in the name of file to read: "))
            #Add ".txt" to ensure that a text file is created and not a regular file
            read_name += ".txt"
            with open(read_name,'r') as f:
                #Uses the read operator to read what is in the file
                content = f.read()
            print(content)
        #If any errors occur than this message will appear
        except:
            print("An error occurred during the READ operation!")

    elif option == '3':  # Append
        try:
            #User input for name of text file
            edit_name = str(input("Type in the name of file to read: "))
            #Add ".txt" to ensure that a text file is created and not a regular file
            edit_name += ".txt"
            #User input of what to put in the text file
            edit_text = (input("Type in what you want to add to file:\n"))
            with open(edit_name,'a') as f:
                #Uses the write operator 
                f.write(edit_text)
        #If any errors occur than this message will appear
        except:
            print("An error occurred during the APPEND operation!")

    elif option == '4':  # Find
        try:
            #User input for the name of text file
            find_name = input("Type in the name of the file: ")
            find_name += ".txt"
            #User input of what text to find in the file
            find_text = input("Type in what text to find: ")
            with open(find_name, 'r') as f:
                content = f.read()
                #Splits the content into individual words
                words = content.split()
                #Use the number of the index for the print message
                for index in range(len(words)):
                    if words[index] == find_text:
                        print(f"Text was found at index: {index}")
                    else:
                        print("No results")
        #If any errors occur than this message will appear
        except:
            print("An error occurred during the FIND operation!")

    elif option == '5':  # Export
        try:
            #User input for the text file name
            export_name = input("Type in the name of the file: ")
            export_name += ".txt"
            #User input for the new name for the csv file
            csv_name = input("Type in the name of the new CSV file: ")
            #Ensures that the file is a csv file
            csv_name += ".csv"
            #Opens both files, text file with reading and csv file with writing
            with open(export_name,"r") as text:
                with open(csv_name, "w") as csvfile:
                    #Using a writer from the csv module
                    writer = csv.writer(csvfile)
                    for i in text:
                        #Split the content in text file
                        content = i.strip()
                        content = i.split()
                        #Write each of the content into the new csv file
                        writer.writerow(content)
            print("Exported text file to a new CSV file!")
        except:
            print("An error occurred during the EXPORT operation!")
    else:
        print('Invalid option!')
    time.sleep(1.5) #1.5
    print('Going Back to main menu ',end='')
    for i in range(4):
        print('.', end='')
        time.sleep(0) #.4
    print()
    option = chooseOption()
