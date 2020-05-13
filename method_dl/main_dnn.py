import numpy as np
import pandas as pd

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
"""
Keras Method
"""
from keras.models import Sequential
import method_dnn as dnn 

normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets):

    packets = prep.proto_to_value(packets)    
    packets = prep.state_to_value(packets)    
    packets = prep.service_to_value(packets)
    packets = prep.ip_to_value(packets)
    
    attack_cat, label, packets = prep.seperate_att(packets)

    #if we want to do get only non-flow features
    #packets = prep.get_imp(packets)
    
    return packets, label, attack_cat

#create np array for label
def label_to_nparr(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0])
        elif(label_list[i] == 1):
            label_np.append([0, 1])
        
    return label_np

if __name__ == "__main__":


    train_df = pd.read_csv("../dataset/NUSW_mix_4.csv", low_memory=False)
    test_df = pd.read_csv("../dataset/NUSW_mix.csv", low_memory=False)

    train_df, trainlabel_list, train_att_cat = init(train_df)
    test_df, testlabel_list, test_att_cat = init(test_df)


    """ pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None) """
    
    #transforming datatype
    train_df = prep.trans_datatype(train_df)
    test_df = prep.trans_datatype(test_df)

    """ #normalize
    normalize_features = normalize_all
    train_packets = prep.normalization(train_packets, normalize_features)
    #train_packet.shape = (10000, 71) -> 10000筆資料 每一筆有71維
    test_packets = prep.normalization(test_packets, normalize_features)  """
    
    #scaling
    train_df = prep.feature_scaling(train_df)
    test_df = prep.feature_scaling(test_df)

    #create an one-hot list for label list

    trainlabel_list = label_to_nparr(trainlabel_list)
    testlabel_list = label_to_nparr(testlabel_list)

    #turn dataframe and list to np array
    trainlabel_np, train_np = np.array(trainlabel_list), np.array(train_df)
    testlabel_np, test_np = np.array(testlabel_list), np.array(test_df)

    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np.shape[1] # how mant features

    # simpleDNN(feature_dim, units, atv, loss, opt)
    model = dnn.simpleDNN(feature_dim, 10, 'relu', 'mse')

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
    model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, callbacks=[earlystopping, checkpoint, csv_logger])

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])


