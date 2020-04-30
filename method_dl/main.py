import numpy as np
import pandas as pd
"""
Import the Keras libraries and packages
"""
from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.core import Activation, Dense, Dropout
from keras.optimizers import SGD, Adam  

import preprocessing as prep

#import the training data
def load_data(file):
    #file = "../dataset/NUSW10000.csv"
    dataset_train = pd.read_csv(file)
    
    return dataset_train

def init(packets):
    
    packets = prep.proto_to_value(packets)
    packets = prep.state_to_value(packets)
    packets = prep.service_to_value(packets)
    packets = prep.ip_to_value(packets)
    
    #print("before scaling : ", type(packets))  df

    #packets = prep.feature_scaling(packets)  # normalize
    #print("after scaling : ", type(packets)) -> np

    return packets


if __name__ == "__main__":

    train_path = '../dataset/NUSW10000.csv'
    test_path = '../dataset/NUSW20000-label1.csv'

    train_packets = init(load_data(train_path))
    test_packets = init(load_data(test_path))

    label_tr, attack_cat_tr, train_packets = prep.seperate_att_label(train_packets)
    label_ts, attack_cat_ts, test_packets = prep.seperate_att_label(test_packets)



    train_packets = prep.feature_scaling(train_packets)
    #train_packet.shape = (10000, 71) -> 10000筆資料 每一筆有71維
    test_packets = prep.feature_scaling(test_packets)

    #create np array for label

    def label_to_nparr(label_list):
        label_np = []
        for i in range(label_list.shape[0]):
            if(label_list[i] == 0):
                label_np.append([1, 0])
            elif(label_list[i] == 1):
                label_np.append([0, 1])
        
        return label_np

    train_labels = label_to_nparr(label_tr)
    test_labels = label_to_nparr(label_ts)

    #print(test_labels)

    train_labels, train_packets = np.array(train_labels), np.array(train_packets)
    test_labels, test_packets = np.array(test_labels), np.array(test_packets)

    dataset_size = train_packets.shape[0]  # 總共幾筆資料
    feature_dim = train_packets.shape[1] #總共幾個features


    #print(input_dim)


    #DNN model
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=500, activation = 'sigmoid'))
    model.add(Dense(units=500, activation='sigmoid'))
    model.add(Dense(units=500, activation='sigmoid'))
    model.add(Dense(units=2, activation='softmax'))

    model.compile(loss='mse', optimizer=SGD(lr = 0.1), metrics = ['accuracy'])
    model.fit(train_packets, train_labels, batch_size=100, epochs=20)

    result = model.evaluate(test_packets,  test_labels)
    print("testing accuracy = ", result[1])
    """ result = model.predict(test_packets)
    print(result)

    predict_label0 = 0
    predict_label1 = 0
    for r in result:
        if(r[0] > r[1]):
            predict_label0 += 1
        elif(r[0] < r[1]):
            predict_label1 += 1
    print(predict_label0, predict_label1) """





