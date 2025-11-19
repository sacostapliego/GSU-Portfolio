class BankAccount:
    #Constructor with stated parameters
    def __init__(self, new_name, checking_balance, savings_balance):
        #Initialize the instance attributes
        self.name = new_name
        self.checking_balance = checking_balance
        self.savings_balance = savings_balance

    def deposit_checking(self, amount):
        #Checks if amount is positive, if so adds amount to current checking balance
        if amount > 0:
            self.checking_balance += amount
        #If amount is positive, or zero, then nothing will be added to account
        else:
            print("Invalid amount.")

    def deposit_savings(self, amount):
        #Checks if amount is positive, if so adds amount to current savings balance
        if amount > 0:
            self.savings_balance += amount
        else:
            print("Invalid amount.")

    def withdraw_checkings(self, amount):
        #Checks if amount is positive, if so removes amount from current checking balance
        if amount > 0:
            self.checking_balance -= amount
        else:
            print("Invalid amount.")

    def withdraw_savings(self, amount):
        #Checks if amount is positive, if so removes amount from current savings balance
        if amount > 0:
            self.savings_balance -= amount
        else:
            print("Invalid amount.")
        
    def transfer_to_savings(self, amount):
        #Checks if amount is positive, if so removes amount from current checking balance
        #And adds the amount to savings balance
        if amount > 0:
            self.checking_balance -= amount
            self.savings_balance += amount
        else:
            print("Invalid amount.")

#Demo Code/Test Case
account = BankAccount("Mickey", 500.00, 1000.00)
account.checking_balance = 500
account.savings_balance = 500
account.withdraw_savings(100)
account.withdraw_checkings(100)
account.transfer_to_savings(300)
print(account.name)
print(f"${account.checking_balance:.2f}")
print(f"${account.savings_balance:.2f}")
