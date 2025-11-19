# Prolog
# Author: Steven Acosta
# Section: 26

'''
 Purpose: Phone number breakdown
 Pre-conditions (input): (Enter the 10-digit phone number)
 Post-conditions (output): Breakdown of phone number (area code, prefix, line number)
'''

def main():
# Design and implementation
# 1. Output a message to identify the program, and a blank line
    print("Breakdown of phone number to area code, prefix, line number")
    print()
# 2. Input the 10-digit phone number
    phone_number = int(input ('Enter phone number? '))
# 3. Breakdown the phone number

    line_number = phone_number%10000
    phone_number = phone_number//10000
    prefix = phone_number%1000
    phone_number = phone_number//1000
    area_code = phone_number

# 4. Output breakdown to area code, prefix, line number
    print()
    print('Phone number is converted to the area code=', area_code, ', prefix =', prefix, ', line number=', line_number)
main()
# end of program file

#Syntax error 1: 1. The wrong character was used and there wasn't a paranthesis 
#                2. SyntaxError: invalid character '‘'
#                3. I removed those characters and added the proper ones and added one more paranthesis
#Syntax error 2: 1. The progam was not indented properly
#                2. IndentationError: expected an indented block after function definition on 
#                3. I indented it properly
#SemanticsError: 4. There wasn't any calculations in the breaking down portion
#                5. Lines 21-25
#                6. I fixed it by diving the current phone number 2 times, in order to match the 3 commads (area code, prefix, and line number)
#                7. The requirments for this to work was by asking for the user to input, line 18, and than calculating to remove 
#                   the numbers from the user input, lines 21-25, than printing out the message on line 29. Also would mention that I changed the final print message
#                   to match the output that was provided
