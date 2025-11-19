#Creates for the swap function
def swap_values(user_val1, user_val2, user_val3, user_val4):
    #Swaps the 1st and 2nd values
    i = user_val1
    user_val1 = user_val2
    user_val2 = i
    #Swaps the 3rd and 4th values
    j = user_val3
    user_val3 = user_val4
    user_val4 = j
    return user_val1, user_val2, user_val3, user_val4

#Calls for the main function
def main():
    #Inputs
    user_val1 = int(input('Val 1: '))
    user_val2 = int(input('Val 2: '))
    user_val3 = int(input('Val 3: '))
    user_val4 = int(input('Val 4: '))
    #Calls the function with new values
    user_val1, user_val2, user_val3, user_val4 = swap_values(user_val1, user_val2, user_val3, user_val4)
    print(f"{user_val1} {user_val2} {user_val3} {user_val4}")
main()