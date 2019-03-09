from get_pure_data import Data
from model import build_model
import matplotlib.pyplot as plt

window = 25

tcs_data = Data('TCS')
tcs_data.preprocess()
x_train, y_train, x_test, y_test = tcs_data.split_data(window=window)

model = build_model([x_train.shape[2], window, 100, 1])
model.fit(x_train, y_train, batch_size=200 , epochs=1 , verbose=1 )
#Predicting
predictions = model.predict(x_test)
predictions = inverse_transform(predictions)
#Plotting and printing results

plt.plot(y_test, color = 'blue', label = 'Real TCS Stock price')
plt.plot(predictions, color = 'orange', label = 'Predicted TCS Stock Price')
plt.title('TCS Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('TCS Stock Price')
plt.legend()
plt.show()
