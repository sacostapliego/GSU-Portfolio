import pandas as pd
import matplotlib.pyplot as plt

#Reads the csv file into a Pandas Dataframe
data = pd.read_csv('atlanta_weather.csv')

#Creates the plot itself
plt.plot()

#Adds the title, month, and temperature along with their respective font size,
plt.title('Atlanta - Monthly Temperature', fontsize=20)
plt.xlabel('Month',fontsize=16)
plt.ylabel('Temperature (Fahrenheit)',fontsize=16)

#Plot the data using month as x and high values as y
# b=blue o=circle marker --=dashed
plt.plot(data['Month'], data['High'], 'bo--' ,label='High')

#Plot the data using month as y and high values as x
# g = greeb -.=dashed-dot line ^=triangle
plt.plot(data['Month'], data['Low'], 'g-.^' ,label='Low')

#Annotates the highest temperature using dict
plt.annotate('Highest Temperature\nof the Year',\
            arrowprops=dict(facecolor='red'),\
            xy=('Jul',89),\
            xytext=('Jun',80))

#Creates the legend
plt.legend(fontsize=16)

plt.show()