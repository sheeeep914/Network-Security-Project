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

attack_cat = ['Normal', 'Fuzzers', 'Analysis',
'Backdoors', 'Dos', 'Exploits', 'Generic', 'Reconnaissance', 'Shellcode', 'Worms']

#DNN model
def simpleDNN(feature_dim, units, atv, loss):
    
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=units,
                    activation = atv)) 
    for i in range(10):
        model.add(Dense(units=units-i, activation=atv))

    model.add(Dense(units=10, activation='softmax'))
    opt = Adam(learning_rate=0.01)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model


#DNN model with dropout
def simpleDNN_dropout(feature_dim, units, atv, loss, output_dim):
    model = Sequential()

    model.add(Dense(input_dim=feature_dim, units=units,
        activation = atv)) 

    for i in range(10):
        model.add(Dense(units=units-i, activation=atv))

    model.add(Dropout(0.2, input_shape=(units-i+1,)))
    model.add(Dense(units=output_dim, activation='softmax'))
    opt = Adam(learning_rate=0.01)
    model.compile(loss=loss, optimizer=opt, metrics=['accuracy'])

    return model


def metricsDNN(predict, actual):
    print("=========================")
    confusion_metrics = pd.crosstab(actual, predict, rownames=['label'], colnames=['predict'])
    print(confusion_metrics)
    print("=========================")


def detailAccuracyDNN(predict, actual, method):
    n = len(predict)
    #bad_index_list = []
    total = [0 for i in range(10)]
    x = [0 for i in range(10)]


    for i, value in enumerate (actual):
        total[value] = total[value]+1

    for i, value in enumerate(predict):
        if(predict[i] == actual[i]):
            x[value] = x[value]+1

    if(method == 'attack_cat'):
        for index in range(10):
            print("==========================")
            print(index, attack_cat[index], ': ','predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)
    elif(method == 'label'):
        for index in range(2):
            print("==========================")
            print(index, ': ', 'predict: ', x[index], 'total: ', total[index])
            try:
                print("acc: ", x[index]/total[index])
            except ZeroDivisionError:
                print("acc: ", 0.0)

    ("==========================")
    

    """B_G, G_G, G_B, B_B = 0, 0, 0, 0
    n = len(predict)
    bad_index_list = []

    for i in range(len(predict)):
        if (actual[i] == 0) & (predict[i] == 0):
            G_G = G_G+1

        elif (actual[i] == 0) & (predict[i] == 1):
            G_B = G_B+1

        elif (actual[i] == 1) & (predict[i] == 0):
            B_G = B_G+1

        elif (actual[i] == 1) & (predict[i] == 1):
            B_B = B_B+1
            #must return its index for the usage in iptable
            bad_index_list.append(i)

    print("===========================")
    print("predict right:")
    print("Good to Good: ", G_G/n)
    print("Bad to Bad: ", B_B/n)
    print("===========================")
    print("predict wrong:")
    print("Good to Bad: ", G_B/n)
    print("Bad to Good: ", B_G/n)
"""
    #return bad_index_list
