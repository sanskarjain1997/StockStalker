from keras.layers import Dense, LSTM, Dropout, Activation
from keras.models import Sequential

hparams = { 'optimizer' : 'RMSprop',
			'loss' : 'mse',
			'activation' : 'linear'
		  }

def build_model(layers):
    model = Sequential()

    # By setting return_sequences to True we are able to stack another LSTM layer
    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.4))

    model.add(LSTM(
        layers[2],
        return_sequences=True))
    model.add(Dropout(0.3))
    
    model.add(LSTM(
    layers[2],
    return_sequences=False))
    model.add(Dropout(0.3))

    model.add(Dense(
        output_dim=layers[3]))
    model.add(Activation(hparams['activation']))

    model.compile(loss=hparams['loss'], optimizer=hparams['optimizer'], metrics=['accuracy'])

    return model
