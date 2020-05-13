import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

#import the training data
def load_data(file):
    #file = "../dataset/NUSW_mix.csv"
    dataset_raw = pd.read_csv(file, low_memory=False)

    return dataset_raw


def seperate(dataset):
    
    #處理缺失值
    dataset.fillna(value=0, inplace=True)  #缺失值全部填成0
    #dataset.isnull().sum() -> 看每一個key是否有null值

    key_len = dataset.shape[1] #總共幾個features
    feature_name = dataset.keys().tolist()
    feature_name.remove('Label')
    
    dataset_temp, label = dataset.iloc[:, : key_len-1].values,  dataset.iloc[:,  key_len-1].values
    dataset_train, dataset_test, label_tr, label_ts = train_test_split(dataset_temp, label, test_size=0.25, random_state=2)  # 隨機選25趴當測試，剩下當訓練
    #print(dataset_train.dtype)
    np.random.shuffle(dataset_train)
    np.random.shuffle(dataset_test)
    dataset_train = pd.DataFrame(dataset_train, columns=feature_name)
    dataset_test = pd.DataFrame(dataset_test, columns=feature_name)
    """ label_tr = pd.DataFrame(label_tr, columns = ['Label'])
    label_ts = pd.DataFrame(label_ts, columns = ['Label']) """
    
    return dataset_train, dataset_test, label_tr, label_ts


def seperateRNN(data_tr, data_ts):
    #處理缺失值
    data_tr.fillna(value=0, inplace=True)  # 缺失值全部填成0
    data_ts.fillna(value=0, inplace=True)  # 缺失值全部填成0
    X_tr, X_ts, y_tr, y_ts = [], [], [], []
    #indexes_tr, indexes_ts = [], []

    feature_name = data_tr.keys().tolist()
    feature_name.remove('Label')
    n = 10  # 10個一組
    temp_features = [feature_name for _ in range(n)]
    #print(temp_features)

    
    for i in range(data_tr.shape[0] - n):
        X_tr.append(data_tr.iloc[i:i+n].values)     #i - i+n-1
        y_tr.append(data_tr['Label'].iloc[i+n-1])   #i+n-1
        #indexes_tr.append(data_tr.index[i+n-1])     #i+n-1

    for i in range(data_ts.shape[0] - n):
        X_ts.append(data_ts.iloc[i:i+n].values)  # i - i+n-1
        y_ts.append(data_ts['Label'].iloc[i+n-1])  # i+n-1
        #indexes_ts.append(data_ts.index[i+n-1])  # i+n-1

    """ X_tr = np.array(X_tr)
    y_tr = np.array(y_tr)
    X_ts = np.array(X_ts)
    y_ts = np.array(y_ts) """

    #print(X_tr[0].shape)
    #print(y_tr.shape) 
    #print(X_tr[0])

    """ X_tr = pd.DataFrame(X_tr, columns=temp_features)
    X_ts = pd.DataFrame(X_ts, columns=temp_features) """

    return X_tr, X_ts, y_tr, y_ts





""" data_tr = load_data("../dataset/NUSW10000.csv")
data_ts = load_data("../dataset/NUSW20000.csv")
seperateRNN(data_tr, data_ts)  
"""
