import pandas as pd
import numpy as np

class Preprocess:
    def __init__(self):
        self.data = [i for _,i in pd.read_csv('Processed-TCS.csv').groupby('date')]

    def split_data(self, data, train_percent=0.9):
        total_samples = len(data)
        training_samples = int(train_percent * total_samples)

        train = data[:training_samples]
        test = data[training_samples:]

        x_train = train[]
        y_train =
        x_test =
        y_test =

        return x_train, y_train, x_test, y_test
