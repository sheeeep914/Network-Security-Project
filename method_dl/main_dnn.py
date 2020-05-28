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
import temp_iptable as iptable

normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']


def init(packets):
    #deal with missing
    packets.fillna(value=0, inplace=True)  # fill missing with 0

    packets = prep.proto_to_value(packets)    
    packets = prep.state_to_value(packets)    
    packets = prep.service_to_value(packets)
    packets, srcip, dstip = prep.ip_to_value(packets)
    
    attack_cat, label, packets = prep.seperate_att_lab(packets, 'dnn')

    #if we want to do get specfic
    #packets = prep.get_imp(packets)
    
    return packets, label, srcip, dstip

#create np array for label
def label_to_nparr(label_list):

    label_np = []
    for i in range (label_list.shape[0]):
        if(label_list[i] == 0):
            label_np.append([1, 0])
        elif(label_list[i] == 1):
            label_np.append([0, 1])
        
    return label_np

def processed_data(datapath):
    data_df = pd.read_csv(datapath, low_memory=False)

    data_df, datalabel_list, data_srcip, data_dstip = init(data_df)
    #print("1 ", type(data_srcip))

    #transforming datatype
    data_df_transtype = prep.trans_datatype(data_df)
    #print("2 ", type(data_df))

    #scaling (data type changes after scaling, i.e. df -> np)
    data_df_scale = prep.feature_scaling(data_df_transtype)
    #print("3 ", type(data_df))

    #create an one-hot list for label list
    datalabel_list_oneHot = label_to_nparr(datalabel_list)

    #turn dataframe and list to np array
    datalabel_np, data_np = np.array(datalabel_list_oneHot), np.array(data_df_scale)

    #deal with problem of key 'ct_ftp_cmd'
    data_np = prep.np_fillna(data_np)

    return data_np, datalabel_np, datalabel_list, data_srcip, data_dstip

def testing_predict(model, testlabel_list, srcip_list):
    predictLabel = model.predict_classes(test_np)
    #print(predictLabel)
    bad_index_list = dnn.detailAccuracyDNN(predictLabel, testlabel_list)
    #print(bad_index_list)

    bad_srcip_list = []

    for index in bad_index_list:
        bad_srcip_list.append(srcip_list[index])

    return bad_srcip_list


if __name__ == "__main__":
    train_path = "../dataset/2_0w4_1w4_yshf_notime.csv"
    test_path = "../dataset/1_0-1_mix_time.csv"

    train_np, trainlabel_np, trainlabel_list, train_srcip, train_dstip = processed_data(train_path)
    test_np, testlabel_np, testlabel_list, test_srcip, test_dstip = processed_data(test_path)

    """ pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    print(train_df.head()) """

    dataset_size = train_np.shape[0]  # how many data
    feature_dim = train_np.shape[1] # how mant features

    # simpleDNN(feature_dim, units, atv, loss)
    #model = dnn.simpleDNN(feature_dim, 15, 'relu', 'mse')


    """ 
    # simpleDNN_dropout(feature_dim, units, atv, loss)
    model = dnn.simpleDNN_dropout(feature_dim, 15, 'relu', 'mse')

    # Setting callback functions
    csv_logger = CSVLogger('training.log')

    checkpoint = ModelCheckpoint(filepath='dnn_best.h5',
                                verbose=1,
                                save_best_only=True,
                                monitor='accuracy',
                                mode='max')
    earlystopping = EarlyStopping(monitor='accuracy',
                                patience=3,
                                verbose=1,
                                mode='max')

    #training
    model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, callbacks=[
            earlystopping, checkpoint, csv_logger], shuffle=True)
    #model.fit(train_np, trainlabel_np, batch_size=100, epochs=10, shuffle=True)

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])

    #testing_predict(model, testlabel_list, test_srcip) """

    iptable.test()

            
   
