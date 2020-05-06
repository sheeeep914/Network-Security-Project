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
"""
preprocessing
"""
import preprocessing as prep
import sep_train_test as sep


normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets):
    
    packets = prep.proto_to_value(packets)
    
    packets = prep.state_to_value(packets)
    
    packets = prep.service_to_value(packets)

    packets = prep.ip_to_value(packets)
    
    return packets


if __name__ == "__main__":
    data_path = '../dataset/NUSW_mix.csv'

    """ train_path = '../dataset/NUSW_train.csv'
    test_path = '../dataset/NUSW_test.csv' """
    dataset_train, dataset_test, label_tr, label_ts = sep.seperate(
        sep.load_data(data_path))
    #print(dataset_train['proto'])
    

    train_packets = init(dataset_train)
    test_packets = init(dataset_test)
    """ print(train_packets.shape)
    print(test_packets.shape) """
    
    

    attack_cat_tr, train_packets = prep.seperate_att(train_packets)
    attack_cat_ts, test_packets = prep.seperate_att(test_packets)

    """ #normalize
    normalize_features = normalize_all
    train_packets = prep.normalization(train_packets, normalize_features)
    #train_packet.shape = (10000, 71) -> 10000筆資料 每一筆有71維
    test_packets = prep.normalization(test_packets, normalize_features) """

    #scaling
    train_packets = prep.feature_scaling(train_packets)
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
    #print("train feature = ",train_packets.shape[1], "test feature = ", test_packets.shape[1])

    """
    #DNN model
    model = Sequential()
    model.add(Dense(input_dim=feature_dim, units=100, activation = 'sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=100, activation='sigmoid'))
    model.add(Dense(units=2, activation='softmax'))

    model.compile(loss='mse', optimizer='adam', metrics = ['accuracy'])
    model.fit(train_packets, train_labels, batch_size=100, epochs=10)

    result = model.evaluate(test_packets,  test_labels)
    print("testing accuracy = ", result[1])
    result = model.predict(test_packets)
    print(result)

    predict_label0 = 0
    predict_label1 = 0
    for r in result:
        if(r[0] > r[1]):
            predict_label0 += 1
        elif(r[0] < r[1]):
            predict_label1 += 1
    #print(predict_label0, predict_label1)

    """



