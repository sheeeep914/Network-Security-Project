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
import method_dbscan as method_db
import method_isolationForest as method_iF

"""
reduce dimension/visualized
"""
import reduce_dimension as reduce_d


def init(file):
    packets = rd.read(file)
    
    packets = prep.proto_to_value(packets)
    packets = prep.state_to_value(packets)
    packets = prep.service_to_value(packets)

    pkt = packets.copy()

    packets = prep.ip_to_value(packets)

    label, att_cat = prep.seperate_att_label(packets)

    return packets, label, att_cat, pkt


def init_http(file):
    packets = rd.read(file)

    packets = prep.get_http(packets)

    #packets = prep.state_to_value(packets)
    packets = prep.proto_to_value(packets)
    pkt = packets.copy()

    packets = prep.ip_to_value(packets)

    label, att_cat = prep.seperate_att_label(packets)

    #del packets['service']

    return packets, label, att_cat, pkt



def Dbscan_fixed_eps_info(eps, packets):

    """  c_info.packets_in_cluster(db_group_number_list, db_max_label+1)

    for i in range(db_max_label+1):
        c_info.print_cluster(pkt, db_group_number_list, i)

    c_info.print_outlier(pkt, db_group_number_list)
"""
#reduce_d.LDA(packets, db_group_number_list)


"""
Method
"""
#data -> all, imp
#evalu -> e, s
#normalize -> y, n
#delete_tcp_features -> y, n

#normalize_all, normalize_tcp 
normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt',
'is_sm_ips_ports', 'ct_state_ttl', 'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2']

normalize_tcp = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss', 'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz', 'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime', 'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl','ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src', 'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1', 'dstip2', 'swin', 'dwin', 'stcpb', 'dtcpb', 'tcprtt', 'synack', 'ackdat']

normalize_http = ['srcip1', 'srcip1', 'sport', 'dstip1', 'dstip2', 'dsport', 'dur',
'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm']

eps = 0.5


#if this file being run directly by python(__name__ == "__main__") or is it being imported
if __name__ == "__main__": 
    
    # number = input("Input the number of datasets: ")
    #trained by normal packets
    number = 40000
    packets_0, label0, att_cat0, pkt_0 = init('../dataset/NUSW' + str(number) + '-label0.csv')
    #packets_0, label0, att_cat0, pkt_0 = init_http('dataset/NUSW' + str(number) + '-label0-http.csv')

    #mix packets, see outlier as abnormal packets
    number = 20000
    packets, label, att_cat, pkt = init('../dataset/NUSW' + str(number) + '.csv')
    #packets, label, att_cat, pkt = init_http('dataset/NUSW' + str(number) + '-http.csv')
    

    normalize_features = normalize_all
    prep.normalization(packets_0, normalize_features)
    prep.normalization(packets, normalize_features)

    """dbscan, db_max_label, db_group_number_list = method_db.DBscan_fixed_eps(packets_0, eps)
    label_test = method_db.DBscan_predict(packets, eps, dbscan)
    method_db.DBscan_score(label_test, label)"""

    """normalize_features = normalize_http
    prep.normalization(packets_0, normalize_features)
    prep.normalization(packets, normalize_features)

    dbscan, db_max_label, db_group_number_list = method_db.DBscan_fixed_eps(
        packets_0, eps)
    label_test = method_db.DBscan_predict(packets, eps, dbscan)
    method_db.DBscan_score(label_test, label)"""

    for i in range (10):
        forest = method_iF.isolation_forest(packets_0)
        method_iF.outlier_predict(forest, packets, label)




