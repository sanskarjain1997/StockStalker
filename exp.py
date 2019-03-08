from get_pure_data import Data
from model import build_model

tcs_data = Data('TCS')
tcs_data.preprocess()
x_train, y_train, x_test, y_test = tcs_data.split_data(window=25)

#Preprocessing
window = 45 #
model = build_model()
#Splitting the Data
x_train, y_train, x_test, y_test = split_data(data)
#Predicting
#Trading
#Plotting and printing results
