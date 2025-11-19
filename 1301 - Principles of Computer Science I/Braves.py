import unittest

def main():

# initial roster
    brave_roster = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273",
		"Ronald Acuna": "AB: 467, R: 71, H: 124, HR: 15, AVG: 0.266",
  }
# your code here 

#Purpose:
  #The purpose is to look up, add, delete players from the braves roster
#Pre-conditions:
  #The pre-conditions include a menu from the user to choose from (looking up, adding, deleting players).
  #The user would than be asked to provide the player they want to look up, add, or delete.
  #Depending on the choice, the user would than be asked to provide the stats for the new player joining the roser.
#Post-conditoins
  #The post-conditions depend on the users choices, for example if they do not choose from the starting menu, they would be asked to choose one from the following.
  #For both adding and deleting, the user would be shown the updated roster, and if looking up the user would only be shown the player they looked up.

#Start with the braves Roster
brave_roster = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273",
		"Ronald Acuna": "AB: 467, R: 71, H: 124, HR: 15, AVG: 0.266",
  }

#Define the lookup_player function | Requires the roster and the player's name
def lookup_player(roster,look):
    #Checks if the player the user searched up is in the roster
    if look in roster:
        #If the player is in the roster, the user will be given a message with that player and his stats
        print(f"\nHere's {look} stats: {roster[look]}")
        print("\nThanks for using My Braves Stats")
        return roster[look]
    else:
        #If the player is not in the roster, the user will be notified
        print(f"\nuh typo? {look} doesn't play for us :)")
        return "N/A"

#Define the add_player_to_dict function | Requires the roster, the new player's name, and their stats
def add_player_to_dict(roster,add,stats):
    #Checks if the added player already exists in the roster
    if add in roster:
       #Adds (2) to the end of their name
       add += '(2)'
    #Adds the stats to the new player
    roster[add] = stats
    #Prints out the statement for a new roster
    print(f"\nHere's the complete team roster: \n")
    #Prints each player in the roster
    for name in roster:
        #First the name, than the players stats
        print(f"     {name}: {roster[name]}")
    print()
    return roster

#Define the delete_in_dict function | Requires the roster, and the player's name to be deleted with their stats
def delete_in_dict(roster,delete):
    #Checks if the player is in the roster
    if delete in roster:
        #If the player is in the roster, than the player will be deleted from the dictionary
        del roster[delete]
        #Prints out the new roster
        print(f"\nHere's the new team roster: \n")
        #Prints each player in the roster
        for name in roster:
            #First the name, than the players stats
            print(f"     {name}: {roster[name]}")
        return roster
    else:
        #If the player is not in the roster, than this message will print
        print(f"\nuh typo? {delete} doesn't play for us :)")
        return roster

#Defines the users function
def user():
    #Prompt the user with selections/screen
    print("    ***  Braves States ***\n")
    print("Welcome to My Braves States! What can I do for you?\n ")
    print("   1. Search for a player\n   2. Add a new player\n   3. Remove a new player\n")
    #Asks the user for their input from the options above
    userInput = int(input('Please type your choice number: '))
    #If the user chooses option 1...
    if userInput == 1:
        #Than the user will be asked to serach the player they want to look up...
        look = str(input('\nEnter the name of the player you want to look up: '))
        #and calls for the lookup_player function
        lookup_player(brave_roster,look)
    #If the user chooses option 2...
    elif userInput == 2:
        #Than the user will be asked for the new player's name and...
        add = str(input('\nEnter the name of the player you want to add: '))
        #the new player's stats...
        stats = str(input(f"\nPlease add {add}'s stats: "))
        #and calls for the add_player_to_disct function
        add_player_to_dict(brave_roster,add,stats)
    #If the user chooses option 3:
    elif userInput == 3:
        #Than the uesr will be asked for the player they want deleted from the roster...
        delete = str(input('\nEnter the name of the player you want to remove: '))
        #and calls for the delete_in_dict function
        delete_in_dict(brave_roster,delete)
    #If the user doesn't select from the 3 options, than they will be asked to move on.
    else:
        print("\nPlease select from the following three options above.")
    #This is to seperate from the testing code
    print('\n')
user()

# Testing code
class TestDictFunctions(unittest.TestCase):

  def test_search_player_success(self):
    test_dict = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"
    }
    actual = test_dict["Austin Riley"]
    expected = lookup_player(test_dict, "Austin Riley")
    self.assertEqual(actual, expected)

  def test_search_player_no_result(self):
    test_dict = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"
    }
    actual = "N/A"
    expected = lookup_player(test_dict, "Ronald Acuna")
    self.assertEqual(actual, expected)

  def test_add_player_sucess(self):
    test_dict = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"
    }
    actual = {
		"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273",
		"Ronald Acuna": "AB: 467, R: 71, H: 124, HR: 15, AVG: 0.266"
    }
    expected = add_player_to_dict(test_dict, "Ronald Acuna", "AB: 467, R: 71, H: 124, HR: 15, AVG: 0.266")

    self.assertEqual(actual, expected)

  def test_add_player_duplicate(self):
    test_dict = {"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"}
    actual = {"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273", "Austin Riley(2)": "AB: 350, R: 20, H: 120, HR: 5, AVG: 0.214"}
    expected = add_player_to_dict(test_dict, "Austin Riley", "AB: 350, R: 20, H: 120, HR: 5, AVG: 0.214")
    self.assertEqual(actual, expected)

  def test_delete_player_sucess(self):
    test_dict = {"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"}
    expected = {}
    actual = delete_in_dict(test_dict, "Austin Riley")
    self.assertEqual(actual, expected)

  def test_delete_word_no_result(self):
    test_dict = {"Austin Riley": "AB: 615, R: 90, H: 168, HR: 38, AVG: 0.273"}
    expected = test_dict
    actual = delete_in_dict(test_dict, "Shohei Ohtani")
    self.assertEqual(actual, expected)


#uncomment to run tests
unittest.main()

