"""
useful lib
"""
import pandas as pd

"""
function
"""
import read_data as rd
import preprocessing as prep
import cluster_info as c_info

"""
method
"""
import method_kmeans as method_km
import method_dbscan as method_db

"""
feature selection 
"""
import feature_sel_pca as f_sel_pac

"""
reduce dimension/visualized
"""
import reduce_dimension as reduce_d


def init(file):
    #global packets, pkt, label, attack_cat

    packets = rd.read(file)

    prep.proto_to_value(packets)
    prep.state_to_value(packets)
    prep.service_to_value(packets)

    pkt = packets.copy()

    prep.ip_to_value(packets)

    label, attack_cat = prep.seperate_att_label(packets)
    return packets, pkt, label, attack_cat


# number = input("Input the number of datasets: ")
number_train = 10000
number_test = 20000
packets_train, pkt_train, label_train, attack_cat_train = init(
    'dataset/NUSW' + str(number_train) + '.csv')
packets_test, pkt_test, label_test, attack_cat_test = init(
    'dataset/NUSW' + str(number_test) + '.csv')

#print(packets_train.shape[1])

""" pd.set_option('display.max_columns', None)
print(packets.head()) """
#print(type(packets.keys()) == int)


# method_k.Elbow(packets_train, pkt_train)     -> plot result for elbow
# method_k.Silh(packets_train, pkt_train)      -> plot result for silh

def Kmeans_fixed_k_info(packets, pkt):
    km_max_label, km_group_number_list = method_km.Silh_fixed_size(packets, 6) 
    #6是從silh的圖中看出來的

    c_info.packets_in_cluster(km_group_number_list, km_max_label+1)

    for i in range(km_max_label+1):
        c_info.print_cluster(pkt, km_group_number_list, i)

def Dbscan_fixed_eps_info(eps, packets_tr, packets_t, pkt_tr, pkt_t):
    db_model_train, db_max_label, db_group_number_list = method_db.DBscan_fixed_eps(
        packets_tr, eps)
    
    t_db_max_label, t_db_group_number_list = method_db.DBscan_predict(
        db_model_train, packets_t)

    c_info.packets_in_cluster(db_group_number_list, db_max_label+1)
    c_info.packets_in_cluster(t_db_group_number_list, t_db_max_label+1)

    print("db train data")
    for i in range(db_max_label+1):
        c_info.print_cluster(pkt_tr, db_group_number_list, i)
    print("__________________")

    print("db test data")
    for i in range(t_db_max_label+1):
        c_info.print_cluster(pkt_t, t_db_group_number_list, i)


    #c_info.print_outlier(pkt_tr, db_group_number_list)

#reduce_d.LDA(packets, db_group_number_list)


"""
Method
"""
#data -> all, imp
#evalu -> e, s
#normalize -> y, n
#delete_tcp_features -> y, n

#normalize_all, normalize_tcp 要改
normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt',
'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']

normalize_tcp = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl','ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2', 'swin', 'dwin', 'stcpb', 'dtcpb', 'tcprtt', 'synack', 'ackdat']

def raw_data(packets, evalu, del_tcp, normalize):
    if(evalu == 'km_e'):
        method_km.Elbow(packets)
    elif(evalu == 'km_s'):
        if(del_tcp == 'y'):
            prep.del_tcp_features(packets)
            if(normalize == 'y'):
                normalize_features = ['Stime', 'Ltime', 'Sload', 'Dload']
                prep.normalization(packets, normalize_features)

        #Kmeans_fixed_k_info()

    elif(evalu == 'db'):
        if(del_tcp == 'y'):
            prep.del_tcp_features(packets)
            if(normalize == 'y'):
                #要抓所有key出來當normalize_all

                normalize_features = normalize_all
                prep.normalization(packets, normalize_features)
        elif(del_tcp == 'n'):
            if(normalize == 'y'):
                normalize_features = normalize_tcp
                prep.normalization(packets, normalize_features)
                """ del packets['Ltime']
                del packets['Stime']
                del packets['Sintpkt']
                del packets['Dintpkt']
                del packets['Sjit']
                del packets['Djit'] """
                #print(packets.loc[0])

        #Dbscan_fixed_eps_info(0.5)
    return packets
        


data_train = raw_data(packets_train, 'db', 'n', 'y')
data_test = raw_data(packets_test, 'db', 'n', 'y')


def db_train_and_predict(data_tr, data_t):
    Dbscan_fixed_eps_info(0.5, data_tr, data_t, pkt_train, pkt_test)


db_train_and_predict(data_train, data_test)
""" 
def imp_data(normalize):
    imp_packets = prep.get_imp(packets)
    if(normalize == 'y'):
        normalize_features = ['srcip1', 'srcip1', 'sport', 'dstip1', 'dstip2', 'dsport','dur', 'sbytes', 'Stime', 'Ltime']
        prep.normalization(imp_packets, normalize_features)

    Dbscan_fixed_eps_info(0.5)
    #Kmeans_silh() """


#raw_data('db', 'n', 'y')

