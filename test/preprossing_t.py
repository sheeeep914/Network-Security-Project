"""
1. time based
2. feature based with no weight
3. feature based with important features
4. feature based with time weight
5. time slot + feature based
"""
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, AffinityPropagation
from sklearn.metrics import silhouette_samples, silhouette_score, pairwise_distances
from sklearn.decomposition import PCA
from itertools import cycle
from sklearn import metrics


#important features
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

"""
def time_standardization():
    #Math(r'x^{(i)}_{norm}=\frac{x^{(i)}-x_{min}}{x_{max}-x_{min}}')
    packets['Stime'] = (packets['Stime'] - packets['Stime'].mean()) /\
        (packets['Stime'].std())
    packets['Ltime'] = (packets['Ltime'] - packets['Ltime'].mean()) /\
        (packets['Ltime'].std())
    print(packets['Stime'].head())
"""

imp_features = ['srcip','sport','dstip','dsport','proto','state','dur','sbytes','Stime', 'Ltime', 'service']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN','CON']
service = ['http','dns','ftp-data']

normalize = []



def init(file):
    with open(file,  newline='') as csvfile:

        global packets
        packets = pd.read_csv(csvfile)

    global label, attack_cat 
    label = packets['Label'].to_numpy()
    attack_cat = packets['attack_cat'].to_numpy()
    del packets['Label']
    del packets['attack_cat']

    ip_to_value()
    proto_to_value()
    state_to_value()
    service_to_value()



#number = input("Input the number of datasets: ")
number = 100
init('NUSW' + str(number) + '.csv')



#packets = get_imp()

#del_tcp_features()
#ip_to_value()
#proto_to_value()
#state_to_value()
#service_to_value()
#normalization(normalize)
#time_normalization()
#load_normalization()



"""
preprossing done

"""



#scaler = MinMaxScaler()
#data_transform = scaler.fit_transform(packets)

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

#silhouette ???? ???????????? ???????
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
    group_number = []
    model = KMeans(n_clusters=k)
    km = model.fit(packets)

    group_number = km.labels_
    """ print(group_number[:1000])
    print(group_number[1000:2000])
    print(group_number[2000:3000]) """

#need to fix bug
def Affinite_Pro():

    #parameter setting
    S = -np.square(pairwise_distances(packets))  # Affinity matrix
    prefer = np.mean(S)  # set preference value

    #Affinity Propagation method
    af = AffinityPropagation(preference = prefer).fit(packets)
    cluster_centers_indices = af.cluster_centers_indices_
    n_clusters_ = len(cluster_centers_indices)
    labels = af.labels_

    plt.close('all')
    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        class_members = labels == k
        cluster_center = packets[cluster_centers_indices[k]]
        plt.plot(packets[class_members, 0], packets[class_members, 1], col + '.')
        plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
        for x in packets[class_members]:
            plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()



"""
Method
"""
#data -> all, imp
#evalu -> e, s
#normalize -> y, n
#delete_tcp_features -> y, n

def raw_data(evalu, normalize, del_tcp):
    if(evalu == 'e'):
        Kmeans_elbow()
    elif(evalu == 's'):
        if(del_tcp == 'y'):
            del_tcp_features()
            if(normalize == 'y'):
                normalize_features = ['Stime', 'Ltime', 'Sload', 'Dload']
                normalization(normalize_features)

        Kmeans_silh()


def imp_data(normalize):
    packets = get_imp()
    if(normalize == 'y'):
        normalize_features = ['Stime', 'Ltime']
        normalization(normalize_features)
    
    Kmeans_silh()

#shape = packets.shape[1]
#pca(shape)


Affinite_Pro()


