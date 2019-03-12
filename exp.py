from get_pure_data import Data
from model import build_model
from keras.models import load_model
import sys
import matplotlib.pyplot as plt

program_name = sys.argv[0]
arguments = sys.argv[1:]
argc = len(arguments)
model_file = 'Model.hd5'
stock_symbol = 'TCS'

window = 25
output_features = 1

if argc==2: stock_symbol=arguments[1]

tcs_data = Data(stock_symbol)
tcs_data.preprocess()
x_train, y_train, x_test, y_test = tcs_data.split_data(window=window)

if argc >= 1:
    if arguments[0] == 'train':
        #training
        model = build_model([x_train.shape[2], window, 100, output_features])
        model.fit(x_train, y_train, batch_size=350 , epochs=1 , verbose=1 )
        #Saving Mode
        model.save(model_file)
        print('Trained Model saved as ', model_file)

    if arguments[0] == 'predict':
        #Predicting
        model = load_model('Model.hd5')
        predictions = model.predict(x_test, verbose=1)

        #scaling back the results
        '''y_test = tcs_data.inverse_transform(y_test)[0]
        predictions = tcs_data.inverse_transform(predictions)[0]'''
        #Plotting and printing results

        plt.plot(y_test, color = 'blue', label = 'Real TCS Stock price')
        plt.plot(predictions, color = 'orange', label = 'Predicted TCS Stock Price')
        plt.title('TCS Stock Price Prediction')
        plt.xlabel('Time')
        plt.ylabel('TCS Stock Price')
        plt.legend()
        plt.show()
