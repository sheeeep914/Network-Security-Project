"""
1. time based
2. feature based with no weight
3. feature based with important features
4. feature based with time weight
5. time slot + feature based
"""
from IPython.display import Math

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
    #packets['Ltime'] = (packets['Ltime'] - packets['Ltime'].min()) /\
    #    (packets['Ltime'].max() - packets['Ltime'].min())
    #print(packets['Stime'].head())


def load_normalization():
    packets['Sload'] = (packets['Sload'] - packets['Sload'].min()) /\
        (packets['Sload'].max() - packets['Sload'].min())
    packets['Dload'] = (packets['Dload'] - packets['Dload'].min()) /\
        (packets['Dload'].max() - packets['Dload'].min())

"""
def time_standardization():
    #Math(r'x^{(i)}_{norm}=\frac{x^{(i)}-x_{min}}{x_{max}-x_{min}}')
    packets['Stime'] = (packets['Stime'] - packets['Stime'].mean()) /\
        (packets['Stime'].std())
    packets['Ltime'] = (packets['Ltime'] - packets['Ltime'].mean()) /\
        (packets['Ltime'].std())
    print(packets['Stime'].head())
"""




imp_features = ['srcip','sport','dstip','dsport','proto','state','dur','sbytes','Stime']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN','CON']
service = ['http','dns','ftp-data']



import csv
import pandas as pd
import numpy as np

with open('NUSW10000.csv',  newline='') as csvfile:

    packets = pd.read_csv(csvfile)

label = packets['Label'].to_numpy()
attack_cat = packets['attack_cat'].to_numpy()
del packets['Label']
del packets['attack_cat']


packets = get_imp()

#del_tcp_features()
ip_to_value()
proto_to_value()
state_to_value()
service_to_value()
time_normalization()
#time_standardization()
#load_normalization()

#print(packets.keys())


""" for rows in packets: 
    for object in rows:
        int(object, base = 10)

for x in packets.head(1):
    print(type(x)) """


#print(packets.dtypes)


#print(type(packets.keys()))

"""
preprossing done

"""

#from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.pyplot as plt
#scaler = MinMaxScaler()
#data_transform = scaler.fit_transform(packets)

"""
#Kmeans Algorithm - elbow
sum_of_squared_dis = []
K = range(1, 10)
for k in K:
    model = KMeans(n_clusters = k)
    km = model.fit(packets)
    sum_of_squared_dis.append(km.inertia_)     #SSE

# Plot the elbow
plt.plot(K, sum_of_squared_dis, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()  

"""

#Kmeans Algorithm - silhouette
silhouette_avg = []
K2 = range(2, 20)
for k in K2:
    model = KMeans(n_clusters = k)
    km = model.fit(packets)
    silhouette_avg.append(silhouette_score(packets, km.labels_))

plt.plot(range(2, 20), silhouette_avg)
plt.show()


"""
#Kmeans Algorithm - silhouette for k = 6
group_number = []
#K2 = range(2, 10)
#for k in K2:
model = KMeans(n_clusters=5)
km = model.fit(packets)

group_number = km.labels_
print(group_number[:1000])
print(group_number[1000:2000])
print(group_number[2000:3000])
#print(group_number[100 :200])


#plt.plot(range(2, 10), silhouette_avg)
#plt.show()

"""
