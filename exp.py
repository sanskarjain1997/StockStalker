from get_pure_data import hist
from model import build_model

data = load_data()
data = preprocess_data(data)

#Preprocessing
window = 45 #
model = build_model()
#Splitting the Data
x_train, y_train, x_test, y_test = split_data(data)
#Predicting
#Trading
#Plotting and printing results
