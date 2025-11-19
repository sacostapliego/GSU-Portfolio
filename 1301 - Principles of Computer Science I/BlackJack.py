import random

def random_card(card):
    #Selects card from 1 in 52
    cardOdds = random.randint(1,52)
    if cardOdds <= 48:
        #If card less than 48, select from 
        #the 1-10 values of cards
        card = random.randint(1,10)
    else:
        #if card more than 48, than its an ace
        card = 11
    return card

def create_deck(deck):
    #Creates the decks
    card = 0
    #Creates an empty deck
    deck = []
    #Adds two random cards to the list
    deck.append(random_card(card))
    deck.append(random_card(card))
    #Adds the two in the deck to get total
    total = deck[0] + deck[1]
    return deck, total

def check(total,dealer,bet):
    print(f"\n___________\nYour total: {total}\nDealer's total: {dealer}\n___________")
    #If total is 21, return blackjack
    if total == 21:
        print(f'Blackjack. You just won ${bet}!')
        return bet
    #If total is more than 21, return bust
    elif total > 21:
        print('\nOver 21, bust.')
        return 0
    #If total is more than dealer total, winner
    elif total > dealer:
        bet *= 2
        print(f'\nYou won! you now have ${bet}')
        return bet
    #If total is less than dealer, loser
    elif dealer > 21:
        bet *= 2
        print(f'\nDealer had over 21, you won! You now have ${bet}')
    #If none of the options are selected, than loser
    else:
        print(f'\nYou lost.')
        return 0

def main():
    #Print beginning message
    print("   *** Blackjack ***")
    print("Hello! Welcome to blackjack.")
    print("*** Repersents the player\n+++ Repersents the dealer")
    #User input
    userBet = float(input("How much money do you want to bet? $"))
    currentBet = userBet
    while True:
    #Variables
        userBet = currentBet
        userDeck = []
        houseDeck = []
        userCheck = ''
        #Create user deck
        userDeck, usertotal = create_deck(userDeck)

        #Inform user whats in their deck
        print(f'\n********************\nYour first card is: {userDeck[0]}')
        print(f'Your second card is: {userDeck[1]}')
        print(f'Your total is: {usertotal}\n********************\n')
        #Checks if user gets a Blackjack, an automatic win.
        if (usertotal == 21):
            userBet *= 1.5
            print(f'Blackjack. You just won ${userBet}!')
        else:
            #Creates the dealer deck
            houseDeck, houseTotal = create_deck(houseDeck)
            
            #Shows the dealers first card, to make the user choose
            print(f"++++++++++++++++++++\nDealer's first card is: {houseDeck[0]}\n++++++++++++++++++++\n")

            #The users choices
            print('Select from the following options:\n   1. Stand\n   2. Add another card\n   3. Double-Down')
            userSelection = int(input(('What would you like to do: ')))
            print()

            #If user stands, the game plays on
            if (userSelection == 1):
                print(f"\n++++++++++++++++++++\nDealer's other card is: {houseDeck[1]}")
                print(f"Dealer's total is: {houseTotal}.\n++++++++++++++++++++\n")
                currentBet = check(usertotal,houseTotal,userBet)

            #If the user adds, the game adds another random card
            elif (userSelection == 2):
                #While loop, ending when user types no
                while userCheck != ('n'):
                    #Adds new random card
                    userDeck.append(random_card(0))
                    usertotal += userDeck[-1]
                    #Informs user about new card and new total
                    print(f'\n***********\nYour new card is: {userDeck[-1]}')
                    print(f'Making your new total: {usertotal}\n***********')
                    #If the user goes above 21, than it is an automatic lost
                    if usertotal > 21:
                        break
                    userCheck = str(input("Add another card or no (y/n)? "))
                #Shows off dealer second card
                print(f"\n++++++++\nDealer's second card is: {houseDeck[1]}")
                print(f"Dealer's total is: {houseTotal}.\n++++++++\n")
                currentBet = check(usertotal,houseTotal,userBet)

            #If user doubles down, the game adds another card, but doubles that value of the card, making the bet more if won
            elif (userSelection == 3):
                #Gives the user one random card
                userDeck.append(random_card(0))
                usertotal += userDeck[-1]
                #Doubles the users bet
                userBet *= 2
                #Shows the user their new card and their total
                print(f'\nYour new card is {userDeck[-1]}, and your new bet is rised to ${userBet}')
                print(f'Making your new total {usertotal}')
                #Showcases the dealer's second card and their total
                print(f"\n***\nDealer's second card is: {houseDeck[1]}")
                print(f"Dealer's total is: {houseTotal}.\n***\n")
                #Checks to see if the user won or not.
                currentBet = check(usertotal,houseTotal,userBet)
            #If the user does not select one of the options...
            else:
                print('Please select one of the selections next time.')
                break
        #Checks the current bet and if it is zero, the loop will break automatically
        if currentBet == 0:
            break
        #Gives the user the option to play again and if not, the loop will break and end the game
        userCheck = str(input("\nWould you like to play again with your current bet? If not, press enter to quit: "))
        if userCheck == (""):
            break
    print()
main()