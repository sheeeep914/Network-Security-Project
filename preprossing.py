"""
1. time based
2. feature based with no weight
3. feature based with important features
4. feature based with time weight
5. time slot + feature based
"""
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
    print(type(packets.loc[1]['srcip']))

    n = len(packets)

    srcip = packets['srcip']
    dstip = packets['dstip']
    
    srcip1, srcip2, dstip1, dstip2 = [], [], [], []

    for i in range (n):
        srcip_split = srcip[i].split(".")
        dstip_split = dstip[i].split(".")

        srcip1.append(srcip_split[0])
        srcip2.append(srcip_split[1])

        dstip1.append(dstip_split[0])
        dstip2.append(dstip_split[1])


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

    print(packets.keys())


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
    


imp_features = ['srcip','sport','dstip','dsport','proto','state','dur','sbytes']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN','CON']
service = ['http','dns','ftp-data']



import csv
import pandas as pd

with open('NUSW-1000.csv',  newline='') as csvfile:

    packets = pd.read_csv(csvfile)

label = packets['Label'].to_numpy()
attack_cat = packets['attack_cat'].to_numpy()
del packets['Label']
del packets['attack_cat']


packets_imp = get_imp()

ip_to_value()
proto_to_value()
state_to_value()
service_to_value()

print(packets.keys())

"""
preprossing done

"""