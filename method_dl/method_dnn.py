"""
Import the Keras libraries and packages
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD, Adam


#DNN model
def simpleDNN(feature_dim, units, atv, loss):
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=units,
                    activation=atv))
    for i in range(10):
        model.add(Dense(units=units, activation=atv))

    model.add(Dense(units=2, activation='softmax'))
    adam = Adam(0.00006)
    model.compile(loss=loss, optimizer=adam, metrics=['accuracy'])

    return model

#RNN model
