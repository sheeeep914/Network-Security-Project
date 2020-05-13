import numpy as np
import pandas as pd
"""
Import the Keras libraries and packages
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.core import Activation, Dense, Dropout
from keras.layers.recurrent import LSTM
from keras.optimizers import SGD, Adam


def seperateRNN(data_tr, data_ts):
    #deal with missing
    data_tr.fillna(value=0, inplace=True)  # fill missing with 0
    data_ts.fillna(value=0, inplace=True)
    X_tr, X_ts, y_tr, y_ts = [], [], [], []
    #indexes_tr, indexes_ts = [], []

    feature_name = data_tr.keys().tolist()
    feature_name.remove('Label')
    n = 10  # 10 packets per group
    temp_features = [feature_name for _ in range(n)]
    #print(temp_features)

    for i in range(data_tr.shape[0] - n):
        X_tr.append(data_tr.iloc[i:i+n].values)  # i - i+n-1
        y_tr.append(data_tr['Label'].iloc[i+n-1])  # i+n-1

        #indexes_tr.append(data_tr.index[i+n-1])     #i+n-1

    for i in range(data_ts.shape[0] - n):
        X_ts.append(data_ts.iloc[i:i+n].values)  # i - i+n-1
        y_ts.append(data_ts['Label'].iloc[i+n-1])  # i+n-1
        #indexes_ts.append(data_ts.index[i+n-1])  # i+n-1

    X_tr = np.array(X_tr)
    y_tr = np.array(y_tr)
    X_ts = np.array(X_ts)
    y_ts = np.array(y_ts)

    X_tr = np.reshape(X_tr, (X_tr.shape[0], X_tr.shape[1], X_tr.shape[2]))

    #print(X_tr[0].shape)
    #print(y_tr.shape)
    #print(X_tr[0])

    """ X_tr = pd.DataFrame(X_tr, columns=temp_features)
    X_ts = pd.DataFrame(X_ts, columns=temp_features) """

    return X_tr, X_ts, y_tr, y_ts




#RNN model
def simpleRNN(train_packets, atv, loss):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=train_packets.shape))
    model.add(LSTM(100))
    model.add(Dense(8))
    model.add(Dense(units=2, kernel_initializer='uniform', activation=atv))

    adam = Adam(0.00006)

    model.compile(loss=loss, optimizer=adam, metrics=['accuracy'])

    return model


data_tr = load_data("../dataset/NUSW10000.csv")
data_ts = load_data("../dataset/NUSW20000.csv")
seperateRNN(data_tr, data_ts)
