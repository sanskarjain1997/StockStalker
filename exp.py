from get_pure_data import Data
from model import build_model
from keras.models import load_model
from keras.callbacks import TensorBoard
from time import time
import sys
import matplotlib.pyplot as plt
import numpy as np

program_name = sys.argv[0]
arguments = sys.argv[1:]
argc = len(arguments)

model_file = 'Model.hd5'
stock_symbol = 'TCS'

tensorboard = TensorBoard(log_dir='logs/{}'.format(time()))

window = 60
output_features = 1

if argc==2: stock_symbol=arguments[1]

tcs_data = Data(symbol=stock_symbol)
tcs_data.minmaxscaling()


if argc >= 1:
	if arguments[0] == 'train':
		#training
		x_train, y_train, _, _ = tcs_data.split_data(window=window, randomize=True)
		print('Shape of x_train : ', x_train.shape)
		print('Shape of y_train : ', y_train.shape)
		model = build_model([x_train.shape[2], window, 100, output_features])
		model.fit(x_train, y_train, batch_size=350 , epochs=6 , verbose=1, callbacks=[tensorboard] )
		#Saving Mode
		model.save(model_file)
		print('Trained Model saved as ', model_file)

	if arguments[0] == 'predict':
		_, _, x_test, y_test = tcs_data.split_data(window=window, randomize=False)
		print('Shape of x_test : ', x_test.shape) #(days, instances, window, features)
		print('Shape of y_test : ', y_test.shape) #(days, instances, features)

		#Load Model file
		model = load_model(model_file)

		#Predicting with all sequences
		predictions = np.array([model.predict(x, verbose=1) for x in x_test])

		#predicting with only first sequence and one model
		'''seq=x_test[-1][0]
		l=len(seq)
		for i in range(0,len(x_test[-1])):
			pred = model.predict(seq[i:].reshape([1,window,1]), verbose=1)
			seq = np.concatenate([seq , pred])

		print('\n\n len(seq) : ',len(seq))'''

		#predicting with only first sequence and many models
		'''windows = range(25,50)
		seq = x_test[-1][0]
		l = len(seq)
		for window in windows:
			model = load_model('Model-w'+str(window)+'.hd5')
			pred = model.predict(seq.reshape([1,window,output_features]), verbose=1)
			seq = np.concatenate([seq, pred])'''

		#Appending starting data of 25 minutes
		'''test = np.array([np.concatenate([x[0],y]) for x,y in zip(x_test, y_test)] )
		predictions = np.array([np.concatenate([x[0],y]) for x,y in zip(x_test, predictions)])'''

		#scaling back the results
		'''test = tcs_data.postprocess(test)
		predictions = tcs_data.postprocess(predictions)'''

		#Plotting and printing results
		plt.plot(y_test[-1], color = 'blue', label = 'Real TCS Stock price')
		plt.plot(predictions[-1], color = 'orange', label = 'Predicted TCS Stock Price')
		plt.title('TCS Stock Price Prediction')
		plt.xlabel('Time')
		plt.ylabel('TCS Stock Price')
		plt.legend()
		plt.show()
