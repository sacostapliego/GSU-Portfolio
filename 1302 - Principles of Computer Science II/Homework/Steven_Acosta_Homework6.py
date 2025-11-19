import pandas as pd
import matplotlib.pyplot as plt

#Reads the csv file into Pandas DataFrame object.
car_data = pd.read_csv('car_data.csv')

#Shape of the data frame.
print(f"1. Shape of the dataframe: {car_data.shape}\n")

#Prints the names of Japanese cars having v6 engines.
#Use of & logical operator between two comparison operators ==
japan_v6 = car_data[(car_data['origin'] == 'japan') & (car_data['cylinders'] == 6)]['name']
print(f"2. Japanese v6 cars: {list(japan_v6)}\n")

#Prints the car names for which the the horsepower data is missing
missing_horse = car_data[car_data['horsepower'].isnull()]['name']
#Using list function to show the same format as the document
print(f"3. Cars with missing horsepower data: {list(missing_horse)}\n")

#Prints the number of cars having mpg >= 20
mpg_20 = car_data[car_data['mpg'] >= 20]
print(f"4. Number of cars having mpg >= 20: {mpg_20.shape[0]}\n")

#Print the name of the car which have the higest mpg.
high_mpg = car_data[car_data['mpg'] == car_data['mpg'].max()]['name']
#Using list function to show the same format as the document
print(f"5. Most fuel efficent car: {list(high_mpg)}\n")

#Print the max, min, and average of the car weights.
max_weight = car_data['weight'].max()
min_weight = car_data['weight'].min()
avg_weight = car_data['weight'].mean()
print(f'6. minimum weight: {min_weight}, maximum weight: {max_weight}, average weight: {avg_weight:.2f}\n')

#Drop the rows from the datagram which have any missing value...
new_data = car_data.dropna()

#..Prints the shape of the resulting dataframe
print(f"7. Shape after removing the missing values: {new_data.shape}\n")

#Creates a plot with two subplots...
#mpg vs weight
#Creates sub plot
plt.subplot(2,1,1)
plt.scatter(car_data['mpg'], car_data['weight'], label = 'Weight')
plt.ylabel('Weight')

#mpg vs displacement
#Creates sub plot
plt.subplot(2,1,2)
plt.scatter(car_data['mpg'], car_data['displacement'], label = 'Displacement')
plt.xlabel('MPG')
plt.ylabel('Displacement')

#Show scatter plot map
plt.show()