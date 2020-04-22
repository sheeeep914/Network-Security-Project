"""
1. time based
2. feature based with no weight
3. feature based with important features
4. feature based with time weight
5. time slot + feature based
"""
import read_data as rd 
import preprocessing_1 as prep

""" #important features
def get_imp():
    imp_features_n = len(imp_features)
    cnt = 0

    packets_imp = packets.copy()
    for col in (packets_imp.columns):
        for i in range (imp_features_n):

            #important features, check the next column
            if (col == imp_features[i]):
                break

            #no important features match, and last feature has been checked 
            elif ((col != imp_features[i]) & (i == imp_features_n-1)):
                del packets_imp[col]

    return packets_imp


def ip_to_value():
    #ip is stored as string
    #print(type(packets.loc[1]['srcip']))

    n = len(packets)

    srcip = packets['srcip']
    dstip = packets['dstip']
    
    srcip1, srcip2, dstip1, dstip2 = [], [], [], []

    for i in range (n):
        srcip_split = srcip[i].split(".")
        dstip_split = dstip[i].split(".")

        srcip1.append(int(srcip_split[0], base = 10))
        srcip2.append(int(srcip_split[1], base = 10))

        dstip1.append(int(dstip_split[0], base = 10))
        dstip2.append(int(dstip_split[1], base = 10))


    packets['srcip1'], packets['srcip2'] = srcip1, srcip2
    packets['dstip1'], packets['dstip2'] = dstip1, dstip2

    del packets['srcip'], packets['dstip']
    #print(packets.keys())
    
def proto_to_value():
    index = 0
    for element in proto:
        proto_list = []
        for protocol in packets['proto']:

            if(protocol == element):
                proto_list.append(1)
            else:
                proto_list.append(0)

        
        packets[element] = proto_list
        
    del packets['proto']

    #print(packets.keys())

def state_to_value():

    for element in states:
        state_list = []
        for state in packets['state']:

            if(state == element):
                state_list.append(1)
            else:
                state_list.append(0)

        
        packets[element] = state_list
        
    del packets['state']

    #print(packets.keys())


def service_to_value():
    
    for element in service:
        service_list = []
        for serv in packets['service']:

            if(serv == element):
                service_list.append(1)
            else:
                service_list.append(0)

        
        packets[element] = service_list
        
    del packets['service']

    #print(packets.keys())
    

def del_tcp_features():
    del packets['swin']
    del packets['dwin']
    del packets['stcpb']
    del packets['dtcpb']
    del packets['tcprtt']
    del packets['synack']
    del packets['ackdat']


#Standardization -> mean = 0, var = 1
#Normalization -> min = 0, max = 1 
def time_normalization():
    #Math(r'x^{(i)}_{norm}=\frac{x^{(i)}-x_{min}}{x_{max}-x_{min}}')
    packets['Stime'] = (packets['Stime'] - packets['Stime'].min())/\
        (packets['Stime'].max() - packets['Stime'].min())
    packets['Ltime'] = (packets['Ltime'] - packets['Ltime'].min()) /\
        (packets['Ltime'].max() - packets['Ltime'].min())
    #print(packets['Stime'].head())


def load_normalization():
    packets['Sload'] = (packets['Sload'] - packets['Sload'].min()) /\
        (packets['Sload'].max() - packets['Sload'].min())
    packets['Dload'] = (packets['Dload'] - packets['Dload'].min()) /\
        (packets['Dload'].max() - packets['Dload'].min()) 

def normalization(features):
    for f in features:
        packets[f] = (packets[f] - packets[f].min()) /\
            (packets[f].max() - packets[f].min())


def time_standardization():
    #Math(r'x^{(i)}_{norm}=\frac{x^{(i)}-x_{min}}{x_{max}-x_{min}}')
    packets['Stime'] = (packets['Stime'] - packets['Stime'].mean()) /\
        (packets['Stime'].std())
    packets['Ltime'] = (packets['Ltime'] - packets['Ltime'].mean()) /\
        (packets['Ltime'].std())
    print(packets['Stime'].head())


imp_features = ['srcip','sport','dstip','dsport','proto','state','dur','sbytes','Stime', 'Ltime', 'service']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN','CON']
service = ['http','dns','ftp-data']

normalize_all = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss',
    'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz',
    'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime',
    'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl',
    'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src',
    'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm',
    'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1',
    'dstip2']

normalize_tcp = ['sport', 'dsport', 'dur', 'sbytes', 'dbytes', 'sttl', 'dttl', 'sloss',
    'dloss', 'Sload', 'Dload', 'Spkts', 'Dpkts', 'smeansz', 'dmeansz',
    'trans_depth', 'res_bdy_len', 'Sjit', 'Djit', 'Stime', 'Ltime',
    'Sintpkt', 'Dintpkt', 'is_sm_ips_ports', 'ct_state_ttl',
    'ct_flw_http_mthd', 'is_ftp_login', 'ct_ftp_cmd', 'ct_srv_src',
    'ct_srv_dst', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm',
    'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'srcip1', 'srcip2', 'dstip1',
    'dstip2', 'swin', 'dwin', 'stcpb', 'dtcpb', 'tcprtt', 'synack', 'ackdat']
"""
import numpy as np
import sys

def init(file):
    """ with open(file,  newline='') as csvfile:

        global packets, pkt
        packets = pd.read_csv(csvfile)
        #print(type(packets)) """
    
    packets = rd.read(file)
    global label, attack_cat 


    prep.proto_to_value(packets)
    prep.state_to_value(packets)
    prep.service_to_value(packets)

    pkt = packets.copy()

    prep.ip_to_value(packets)

    label = packets['Label'].to_numpy()
    attack_cat = packets['attack_cat'].to_numpy()
    del packets['Label']
    del packets['attack_cat']


#number = input("Input the number of datasets: ")
number = 20000
init('NUSW' + str(number) + '.csv')

""" def cal_accuracy(data_index):
    if(data_index == 1):
    """



def packets_in_cluster(labels, n):

    packets_num=[0]*n
    for label in labels:
        if (label != -1):
            packets_num[label] = packets_num[label] +1
    print('number of packets in each cluster: ', packets_num)


def print_cluster(labels, cluster_index):
    print_list = []
    label_list = []
    att_cat_list = []
    timestamp_list = []
    index_list = []
    
    num = 0

    #cal accuracy ratio
    sum_label_0 = 0
    sum_label_1 = 0
    for i in range(len(labels)):
        label = labels[i]
        
        if label == cluster_index:
            print_list.append(list(pkt.iloc[i,:]))
            label_list.append(pkt['Label'].loc[i])

            if(pkt['Label'].loc[i] == 0):
                sum_label_0 += 1
            elif(pkt['Label'].loc[i] == 1):
                sum_label_1 += 1

            att_cat_list.append(pkt['attack_cat'].loc[i])
            timestamp_list.append(pkt['Stime'].loc[i])
            index_list.append(i)
            num = num+1

    ratio0 = (sum_label_0) / (sum_label_0 + sum_label_1)
    ratio1 = (sum_label_1) / (sum_label_0 + sum_label_1)
    print_df = pd.DataFrame(print_list, columns=pkt.keys())
    print_df['index'] = index_list
    print(cluster_index, ':')
    print(index_list)
    print(label_list)
    print(att_cat_list)
    print('ratio0: ', ratio0, ' ratio1: ', ratio1)
    #print(timestamp_list)
    pd.set_option('display.max_rows', None)

    #print(print_df)


"""
preprossing done

"""

#from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt

#from clustering_method import DBSCAN

#scaler = MinMaxScaler()
#data_transform = scaler.fit_transform(packets)
"""
def Kmeans_elbow():   
    sum_of_squared_dis = []
    K = range(1, 10)  # origin -> 1, 10
    for k in K:
        model = KMeans(n_clusters=k)
        km = model.fit(packets)
        sum_of_squared_dis.append(km.inertia_)  # SSE

    # Plot the elbow
    plt.plot(K, sum_of_squared_dis, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Distortion')
    plt.title('The Elbow Method showing the optimal k')
    plt.show()

def Kmeans_silh():
    silhouette_avg = []
    K = range(2, 20)   
    for k in K:
        model = KMeans(n_clusters=k)
        km = model.fit(packets)
        silhouette_avg.append(silhouette_score(packets, km.labels_))

    #Plot
    plt.plot(range(2, 20), silhouette_avg)
    plt.show()

    #return max(silhouette_avg)  # parameter(k) of Kmeans_silh_fixed_size(k)


def Kmeans_silh_fixed_size(k):
    global group_number 
    model = KMeans(n_clusters=k)
    km = model.fit(packets)

    #group_number = km.labels_

    max_label = 0
    for label in km.labels_:
        if label > max_label:
            max_label = label

    packets_in_cluster(km.labels_, max_label+1)
    for i in range(max_label+1):
        c_info.print_cluster(pkt, km.labels_, i)

    


def dbscan_fixed_eps(eps):
    model = DBSCAN(eps = eps, min_samples = 5)
    dbscan = model.fit(packets)
    np.set_printoptions(threshold=sys.maxsize)
    
    max_label = 0
    for label in dbscan.labels_:
        if label > max_label:
            max_label = label

    #max_label + 1 -> 分幾群
    #print(max_label)
    packets_in_cluster(dbscan.labels_, max_label+1)

    for i in range (max_label+1):
        print_cluster(dbscan.labels_, i)
    



def PCA():
    #PCA
    from sklearn.decomposition import PCA
    import matplotlib.pyplot as plt
    pca = PCA(n_components=48).fit(packets)
    print(pca.explained_variance_ratio_)

    fig, ax = plt.subplots(1,2,figsize=(12,6))

    ax[0].scatter(pca[:,0], pca[:,1],c=group_number)
    ax[0].set_title("PCA")


    plt.show() 


"""
Method
"""
#data -> all, imp
#evalu -> e, s
#normalize -> y, n
#delete_tcp_features -> y, n


def raw_data(evalu, del_tcp, normalize):
    if(evalu == 'e'):
        Kmeans_elbow()
    elif(evalu == 's'):
        if(del_tcp == 'y'):
            prep.del_tcp_features(packets)
            if(normalize == 'y'):
                normalize_features = ['Stime', 'Ltime', 'Sload', 'Dload']
                prep.normalization(packets, normalize_features)

        Kmeans_silh()

    elif(evalu == 'db'):
        if(del_tcp == 'y'):
            prep.del_tcp_features(packets)
            if(normalize == 'y'):
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
        dbscan_fixed_eps(0.5)


def imp_data(normalize):
    packets = get_imp()
    if(normalize == 'y'):
        normalize_features = ['srcip1', 'srcip1', 'sport', 'dstip1', 'dstip2', 'dsport',
        'dur', 'sbytes', 'Stime', 'Ltime']
        prep.normalization(packets, normalize_features)
    
    dbscan_fixed_eps(0.5)
    #Kmeans_silh()


""" 
def write_data(evalu, del_tcp, normalize):
    method = []
    method.append(evalu)
    method.append(del_tcp)
    method.append(normalize)

    file_name = ''

    if(method[0] == db)
        
        file_name += 'db'
        file = open()  """
    

#imp_data('y')
raw_data('db', 'n', 'y')
""" del_tcp_features()
Kmeans_silh_fixed_size(6) """




