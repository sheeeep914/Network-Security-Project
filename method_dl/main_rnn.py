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
import method_rnn as rnn

""" 
normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']
"""

def init(packets):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    #one hard encoding
    packets = prep.proto_to_value(packets)
    packets = prep.state_to_value(packets)
    packets = prep.service_to_value(packets)
    packets = prep.ip_to_value(packets)

    #seperate attack category and label (in case of future comparing, don't return)
    attack_cat, label, packets = prep.seperate_att_lab(packets, 'rnn')

    #if we want to do get only non-flow features
    packets = prep.get_imp(packets)

    return packets

#create np array for label
def label_to_nparr(label_list):

    label_np = []
    for i in range(label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0])
        elif(label_list[i] == 1):
            label_np.append([0, 1])

    return label_np


if __name__ == "__main__":

    train_df = pd.read_csv(
        "../dataset/NUSW-1-20000-100000_80000_mix_time.csv", low_memory=False)
    test_df = pd.read_csv(
        "../dataset/NUSW10000.csv", low_memory=False)
    
    
    train_df = init(train_df)
    test_df = init(test_df)

    """ print("train_df key:\n")
    print(train_df.keys()) """
    train_np, test_np, trainlabel_list, testlabel_list = rnn.defRNN(train_df, test_df)

    """ #transforming datatype (object -> normal datatype)
    packets = prep.trans_datatype(packets) """

    """ #scaling
    train_np = prep.feature_scaling(train_np)
    test_np = prep.feature_scaling(test_np) """

    """ pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None) """

    #create an one-hot list for label list
    trainlabel_list_oneHot = label_to_nparr(trainlabel_list)
    testlabel_list_oneHot = label_to_nparr(testlabel_list)

    #turn dataframe and list to np array
    trainlabel_np = np.array(trainlabel_list_oneHot)
    testlabel_np = np.array(testlabel_list_oneHot)

    train_np = prep.np_fillna(train_np)
    test_np = prep.np_fillna(test_np)


    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np[0].shape   # input dimention


    # simpleRNN(feature_dim, atv, loss)
    model = rnn.simpleRNN(feature_dim, 'relu', 'mse')

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

    predictLabel = model.predict_classes(test_np)
    rnn.detailAccuracyRNN(predictLabel, testlabel_list)
