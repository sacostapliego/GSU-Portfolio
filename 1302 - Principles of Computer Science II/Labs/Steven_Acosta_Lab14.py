def computeMSE(observed, predicted):
    #TODO 1: Complete this function
    #Set the squared error to 0
    sq_error = 0
    #Math series loop
    for i in range(len(observed)):
        #Loops squared difference between observed and prediced values (obs - pre)^2
        sq_error += (observed[i] - predicted[i]) ** 2
    #Divide by length of observed (n)
    mse = sq_error / len(observed)
    return mse


def computeRMSE(observed, predicted):
    #TODO 2: Complete this function
    mse = computeMSE(observed, predicted)
    rsme = mse ** 0.5
    return rsme

def computeMAE(observed, predicted):
    # TODO 3: Complete this function
    abs_error = 0
    #Math series loop
    for i in range(len(observed)):
        #Loops absolute difference between obsered and predicted values |obs - pre|
        abs_error += abs(observed[i] - predicted[i])

    #Divide by length of observed (n)
    mae = abs_error / len(observed)
    return mae

'''
TODO 4: Write driver code that calls the above methods and prints
the MSE, RMSE, and MAE for the following input. (Round
off the results to two decimal places)
    observed = 4,5,12,5,7
    predicted = 5,5,11,4,5
'''
#Driver code
#Input
observed = [4, 5, 12, 5, 7]
predicted = [5, 5, 11, 4, 5]

#Functions
mse = computeMSE(observed, predicted)
rmse = computeRMSE(observed, predicted)
mae = computeMAE(observed, predicted)

#Prints...rounded to two decimal places
print(f'MSE  =  {mse:.2f}')
print(f'RSME =  {rmse:.2f}')
print(f'MAE  =  {mae:.2f}')
