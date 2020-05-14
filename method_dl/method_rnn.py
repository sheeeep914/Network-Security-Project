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
""" 
Scaling
"""
from sklearn.preprocessing import MinMaxScaler
import preprocessing as prep

def defRNN(data_tr, data_ts):

    tempdata_tr = data_tr.copy()
    del tempdata_tr['Label']
    tempdata_ts = data_ts.copy()
    del tempdata_ts['Label']
    #deal with missing
    data_tr.fillna(value=0, inplace=True)  # fill missing with 0
    data_ts.fillna(value=0, inplace=True) 
    X_tr, X_ts, y_tr, y_ts = [], [], [], []
    
    #transforming datatype (object -> normal datatype)
    tempdata_tr = prep.trans_datatype(tempdata_tr) 
    tempdata_ts = prep.trans_datatype(tempdata_ts)

    #scaling
    tempdata_tr = prep.feature_scaling(tempdata_tr)
    tempdata_ts = prep.feature_scaling(tempdata_ts)
    
    n = 10  # 10 packets per group
    for i in range(data_tr.shape[0] - n):
        X_tr.append(tempdata_tr[i:i+n])  # i - i+n-1
        y_tr.append(data_tr['Label'].iloc[i+n-1])  # i+n-1

        #indexes_tr.append(data_tr.index[i+n-1])     #i+n-1

    for i in range(data_ts.shape[0] - n):
        X_ts.append(tempdata_ts[i:i+n])  # i - i+n-1
        y_ts.append(data_ts['Label'].iloc[i+n-1])  # i+n-1
        #indexes_ts.append(data_ts.index[i+n-1])  # i+n-1

    X_tr = np.array(X_tr)
    y_tr = np.array(y_tr)
    X_ts = np.array(X_ts)
    y_ts = np.array(y_ts)



    return X_tr, X_ts, y_tr, y_ts




#RNN model
def simpleRNN(feature_dim, atv, loss):
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=feature_dim))
    model.add(LSTM(100))
    model.add(Dense(8))
    model.add(Dense(units=2, kernel_initializer='uniform', activation=atv))

    adam = Adam(0.00006)

    model.compile(loss=loss, optimizer=adam, metrics=['accuracy'])

    return model


""" data_tr = pd.read_csv("../dataset/NUSW10000.csv", low_memory=False)
data_ts = pd.read_csv("../dataset/NUSW20000.csv", low_memory=False)
defRNN(data_tr, data_ts)
 """

def detailAccuracyRNN(predict, actual):
    B_G, G_G, G_B, B_B = 0, 0, 0, 0
    n = len(predict)

    for i in range(len(predict)):
        if (actual[i] == 0) & (predict[i] == 0):
            G_G = G_G+1

        elif (actual[i] == 0) & (predict[i] == 1):
            G_B = G_B+1

        elif (actual[i] == 1) & (predict[i] == 0):
            B_G = B_G+1

        elif (actual[i] == 1) & (predict[i] == 1):
            B_B = B_B+1

    print("===========================")
    print("predict right:")
    print("Good to Good: ", G_G/n)
    print("Bad to Bad: ", B_B/n)
    print("===========================")
    print("predict wrong:")
    print("Good to Bad: ", G_B/n)
    print("Bad to Good: ", B_G/n)
    
