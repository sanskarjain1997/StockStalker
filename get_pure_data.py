import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Data:
    def __init__(self, symbol='TCS'):
        self.data = [i for _,i in pd.read_csv('Processed-'+symbol+'.csv').groupby('date')]
        self.data = [np.array(d) for d in self.data]
        self.data = np.array(self.data)
        print('Shape of data loaded : ',self.data.shape) #(days, 375, 7)

    def split_data(self, data, window=25, train_percent=0.9):
        #Randomizing all samples
        total_samples = data.shape[0]
        indices = np.arange(total_samples)
        np.random.shuffle(indices)
        data = data[indices]

        #Splitting into training and testing data
        training_samples = int(train_percent * total_samples)
        testing_samples = total_samples - training_samples
        train = data[:training_samples]
        test = data[training_samples:]

        #Splitting into input and output
        x_train = []
        y_train = []
        x_test = []
        y_test = []

        for i in range(window, training_samples):
            x_train.append(train[:, (i-window):i , 0])
            y_train.append(train[:,i, 0])

        for i in range(window, testing_samples):
            x_test.append(test[:,(i-window):i, 0])
            y_test.append(test[:, i, 0])

        return x_train, y_train, x_test, y_test

    def preprocess(self, data):
        scaler = MinMaxScaler(feature_range=(0,1))
        self.data = [scaler.fit_transform(d[:,2:]) for d in self.data]
