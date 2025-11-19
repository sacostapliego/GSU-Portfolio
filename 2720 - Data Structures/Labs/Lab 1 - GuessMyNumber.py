"""     Exercise 2     """
#Function to make sure that the user input isn't a zero or negaive number
def checkNumber(num):
    if num <= 0:
        num = int(input('Enter a postive integer for n: '))
        #repeatdly asks the user until a proper number is given
        return checkNumber(num)
    else:
        return num - 1
    
#Function to make sure that the user input is one of the three inputs
def checkLetter(let):
    #Checks if each of these functions are  satisfied
    if (let != 'L') and (let != 'H') and (let != 'C'):
        let = input('Enter your response (H/L/C): ')
        #If they are satisfied, then it will loop till the user inputs a proper letter
        return checkLetter(let)
    else:
        return let


def guess(high, low):
        #Calclutes the middle number of the high and low
        mid = round((high + low) / 2)
        print(f"Is your number: {mid}?")
        user = input(f'Please enter C for correct, H for too high, or L for too low,\nEnter your response (H/L/C): ')
        user = checkLetter(user)
        #If the input is LOW than the new low will 
        #become middle + 1 
        if user == 'L':
            low = mid + 1
            return (guess(high,low))
        elif user == 'H':
        #If the input is HIGH than the new high will 
        #become middle - 1 
            high = mid - 1
            return (guess(high,low))
        #If the user input is C than the game will end.
        elif user == 'C':
            print('Thank you for playing Guess my Number!')
            
#Driver code
userNumber = int(input('Enter n: '))
userNumber = checkNumber(userNumber)
print('Welcome to Guess My Number!')
print(f'Please think of a number between 0 and {userNumber}')
guess(userNumber,0)

