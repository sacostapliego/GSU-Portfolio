import pandas as pd

#Creates the revenue panda series with the correct values
revenue = pd.Series([1000, 900, 1100, 400, 200],\
                    ['Mon','Tue','Wed','Thu','Fri'],\
                     name='Revenue')
#Prints the revenue panda series
print(revenue,'\n')

#Creates the expenses panda series with the correct values
expenses = pd.Series([900, 900, 900, 900, 900],\
                    ['Mon','Tue','Wed','Thu','Fri'],\
                     name='Expenses')
#Prints the expenses panda series
print(expenses,'\n')

#Prints the revenue value on Wednesday using slicing
print('Wednesday Revenue:', revenue['Wed'],'\n')

#Prints the expenses value from Tuesday to Thursday using slicing
print('Expenses on Tuesday, Wednesday, and Thursday:')
print(expenses['Tue':'Thu'],'\n')

#Net_profit using the formula in the slides
net_profit = (revenue - expenses)
#Prints the results
print(net_profit, '\n')

#Find the average of the series using the .mean() function
print('Average: ',net_profit.mean(),'\n')