#Author: Steven Acosta-Pliego
#Course: CSCI 1301 - 21021
#Section: 26
#Python Lab 6

def main():
    #Ask user input three row: Row 0, Row 1, Row 2
    print("PLease input 3 combine of 'X', 'O', or 'E' as XOE, XXE, EXX, and so on")
    ROW0 = input("ROW0: ")
    ROW1 = input("ROW0: ")
    ROW2 = input("ROW0: ")

    #Set the orginal booolean variable horizontal, vertical, diagonal to be False
    horizontal = False
    vertical = False
    Diagonal = False

    # Check if ther are horizonal XXX or OOO
    if ROW0[0] == ROW0 [1] == ROW0[2] == 'X' or ROW1[0] == ROW1[1] == ROW1[2] == 'X' or ROW2[0] == ROW2[1] == ROW2[2] == 'X':
        horizontal = True
        print('X is GOOD in horizontal')
    if ROW0[0] == ROW0 [1] == ROW0[2] == 'O' or ROW1[0] == ROW1[1] == ROW1[2] == 'O' or ROW2[0] == ROW2[1] == ROW2[2] == 'O':
        print('O is GOOD in horizontal')
        horizontal = True

    # Check if there are diagonal XXX or OOO
    if ROW0[0] == ROW1 [1] == ROW2[2] == 'X' or ROW0[2] == ROW1[1] == ROW2[0] == 'X':
        Diagonal = True
        print('X is GOOD in Diagonal')
    if ROW0[0] == ROW1 [1] == ROW2[2] == 'O' or ROW0[2] == ROW1[1] == ROW2[0] == 'O':
        print('O is GOOD in Diagonal')
        Diagonal = True

    # Check if there are vertical XXX or OOO
    if ROW0[0] == ROW1 [0] == ROW2[0] == 'X' or ROW0[1] == ROW1[1] == ROW2[1] == 'X' or ROW0[2] == ROW1[2] == ROW2[2] == 'X':
        vertical = True
        print('X is GOOD in vertical')
    if ROW0[0] == ROW1 [0] == ROW2[0] == 'O' or ROW0[1] == ROW1[1] == ROW2[1] == 'O' or ROW0[2] == ROW1[2] == ROW2[2] == 'O':
        print('O is GOOD in vertical')
        vertical = True

    # If none of the arguments above work and change our boolean statements true, than it is considered a tie
    if vertical == False and Diagonal == False and horizontal == False:
        print('THIS IS A TIE')
main()