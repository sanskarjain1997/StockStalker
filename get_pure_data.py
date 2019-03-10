import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Data:
    def __init__(self, symbol='TCS'):
        self.scaler = MinMaxScaler(feature_range=(0,1))
        self.data = [i for _,i in pd.read_csv('Processed-'+symbol+'.csv').groupby('date')]
        self.data = [np.array(d) for d in self.data]
        self.data = np.array(self.data)
        print('Shape of data loaded : ',self.data.shape) #(591 days, 375 instances per day, 7 features per instance)

    def split_data(self, window=25, train_percent=0.9):
        #Randomizing all samples
        total_samples = self.data.shape[0]
        indices = np.arange(total_samples)
        np.random.shuffle(indices)
        self.data = self.data[indices]

        #Splitting into training and testing data
        training_samples = int(train_percent * total_samples)
        testing_samples = total_samples - training_samples
        train = self.data[:training_samples]
        test = self.data[training_samples:]

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
            for i in range(window, len(day)):
                x_test.append(day[(i-window):i])
                y_test.append(day[i])

        x_train, y_train, x_test, y_test = np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

        return x_train, y_train, x_test, y_test

    def preprocess(self):
        self.data = [self.scaler.fit_transform(day[:,2].reshape([-1,1])) for day in self.data]
        self.data = np.array(self.data)
        print('Shape of data after preprocessing : ', self.data.shape) #(591 days, 375 instances per day, 1 features per instance)
        return self.data

    def inverse_transform(self,data):
        return self.scaler.inverse_transform(data)
