from get_pure_data import Data
from model import build_model

window = 25

tcs_data = Data('TCS')
tcs_data.preprocess()
x_train, y_train, x_test, y_test = tcs_data.split_data(window=window)

model = build_model([x_train.shape[2], window, 100, 1])
model.fit(x_train, y_train, batch_size= , epochs= , verbose= )
#Predicting
predictions = model.predict(x_test)
#Trading
#Plotting and printing results
