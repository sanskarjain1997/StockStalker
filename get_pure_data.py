import pandas as pd

data = pd.read_csv('Processed-TCS.csv')
hist = [i for _,i in data.groupby('date')]
