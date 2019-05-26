import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Data:
	def __init__(self, symbol='TCS'):
		#self.ovd = []
		self.scaler = MinMaxScaler(feature_range=(0,1))
		try:
		    self.data = [i for _,i in pd.read_csv('Processed-'+symbol+'.csv').groupby('date')]
		    self.data = [np.array(d) for d in self.data]
		    self.data = np.array(self.data)
		    print('Shape of data loaded : ',self.data.shape) #(591 days, 375 instances per day, 7 features per instance)
		except:
		    print('File reading error! Try different stock symbol.')
		    exit(-1)

	def split_data(self, window=25, train_percent=0.95, randomize=True):
		#Randomizing all samples
		total_samples = self.data.shape[0]
		indices = np.arange(total_samples)
		if randomize : np.random.shuffle(indices)
		self.data = self.data[indices]
		#self.ovd = self.ovd[indices]
		#Splitting into training and testing data
		training_samples = int(train_percent * total_samples)
		testing_samples = total_samples - training_samples
		train = self.data[:training_samples]
		test = self.data[training_samples:]
		#self.ovd = self.ovd[training_samples:] #splitting opening values of each day too
		#Splitting into input and output
		x_train = []
		y_train = []
		x_test = []
		y_test = []

		for day in train:
		    for i in range(window, len(day)):
		        x_train.append(day[(i-window):i])
		        y_train.append(day[i])

		for day in test:
		        x_test.append([ day[(i-window):i] for i in range(window, len(day)) ])
		        y_test.append([ day[i] for i in range(window, len(day)) ])


		x_train, y_train, x_test, y_test = np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

		return x_train, y_train, x_test, y_test

	def percent_change_norm(self):
		#Percentage change format of data
		data = [ ( d[0,2],[0]+[ float((d[i-1,2]-d[i,2])/d[i-1,2])*100 for i in range(1,len(d)) ] ) for d in self.data]
		self.ovd = np.array([o for o,_ in data]) # opening value of each day
		self.data = np.array([np.array(d) for _,d in data])
		self.data = self.data.reshape([self.data.shape[0], self.data.shape[1], 1]) #reshaping to compatible format
		print('\tShape of data after preprocessing : ', self.data.shape) #(591 days, 375 instances per day, 1 features per instance)
		return self.data

	def percent_change_denorm(self, data):
		print('\n Post-Processing \n')
		ovd = self.ovd
		ret=[]
		for i in range(0,len(data)):
			day = data[i]
			if day[0]==0: day[0]=ovd[i]
			else: print(day[0])
			for i in range(1, len(day)):
				day[i]=(day[i-1]*(1+(day[i]/100)))
			ret.append(day)
		return np.array(ret)
		
	def minmaxscaling(self):
		self.data = [self.scaler.fit_transform(day[:,2].reshape([-1,1])) for day in self.data]
		self.data = np.array(self.data)
		print('Shape of data after preprocessing : ', self.data.shape) #(591 days, 375 instances per day, 1 features per instance)
		return self.data

	def preprocess(self):
		data = self.data[:,:,2] #opening prices (days, instances, )

		for i in range(0,len(data)):
			data[i]=np.concatenate([ [0],np.diff(np.log([x for x in data[i]])) ])/0.05

		self.data = data.reshape([data.shape[0], data.shape[1], 1])
		return data

	def get_data(self):
		return self.data
