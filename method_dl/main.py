import numpy as np
import pandas as pd
"""
Import the Keras libraries and packages

from keras.models import Sequential
from keras.utils import np_utils
from keras.layers import SimpleRNN
from keras.layers.core import Activation, Dense, Dropout
from keras.optimizers import SGD, Adam  
"""
"""
callback function
"""
from keras.callbacks import CSVLogger
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
"""
preprocessing
"""
import preprocessing as prep
import sep_train_test as sep
"""
Keras Method
"""
from keras.models import Sequential
import model as models


normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets):
    packets = prep.proto_to_value(packets)    
    packets = prep.state_to_value(packets)    
    packets = prep.service_to_value(packets)
    packets = prep.ip_to_value(packets)

    #if we want to do get only non-flow features
    #packets = prep.get_imp(packets)
    
    return packets


if __name__ == "__main__":
    #data_path = '../dataset/NUSW_mix_4.csv'

    #dataset_train, dataset_test, label_tr, label_ts = sep.seperate(sep.load_data(data_path))

    data_tr = sep.load_data("../dataset/NUSW_mix.csv")
    data_ts = sep.load_data("../dataset/NUSW_mix_4.csv")
    #dataset_train, dataset_test, label_tr, label_ts = sep.seperateRNN(
    #    data_tr, data_ts)

    train_packets = init(data_tr)
    test_packets = init(data_ts)

    attack_cat_tr, label_tr, train_packets = prep.seperate_att(train_packets)
    attack_cat_ts, label_ts, test_packets = prep.seperate_att(test_packets)

    """ pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None) """
    
    #transforming datatype
    train_packets = prep.trans_datatype(train_packets)
    test_packets = prep.trans_datatype(test_packets)

    """ normalize
    normalize_features = normalize_all
    train_packets = prep.normalization(train_packets, normalize_features)
    #train_packet.shape = (10000, 71) -> 10000筆資料 每一筆有71維
    test_packets = prep.normalization(test_packets, normalize_features)  """
    
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


    train_labels, train_packets = np.array(train_labels), np.array(train_packets)
    test_labels, test_packets = np.array(test_labels), np.array(test_packets)

    dataset_size = train_packets.shape[0]  # how many data
    feature_dim = train_packets.shape[1] #how mant features

    

    # simple(feature_dim, units, atv, loss, opt)
    #model = models.simpleDNN(feature_dim, 10, 'relu', 'mse')

    # simpleRNN(train_packets, atv, loss)
    model = models.SimpleRNN(train_packets, 'relu', 'mse')

    # Setting callback functions
    csv_logger = CSVLogger('training.log')
    checkpoint = ModelCheckpoint(filepath='best.h5',
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=3,
                                verbose=1,
                                mode='max')

    #training
    model.fit(train_packets, train_labels, batch_size=100, epochs=10, callbacks=[earlystopping, checkpoint, csv_logger])

    result = model.evaluate(test_packets,  test_labels)
    print("testing accuracy = ", result[1])


"""
    result = model.predict(test_packets)
    print(result)

 
    predict_label0 = 0
    predict_label1 = 0
    for r in result:
        if(r[0] > r[1]):
            predict_label0 += 1
        elif(r[0] < r[1]):
            predict_label1 += 1
    #print(predict_label0, predict_label1) """





