import scapy.all as sp
import copy
import numpy as np
import pandas as pd
import statistics

def get_pcap_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1


def create_flow(pcaps):
    n = len(pcaps)
    layers = []
    flows = []

    for i, header in enumerate(pcaps):
        
        layers = []
        flow = []

        for layer in get_pcap_layers(header):
            layers.append(layer.name)

        try :
            ip = layers[1]
            port = layers[2]

            flow.append(header.getlayer(ip).src)
            flow.append(header.getlayer(ip).dst)
            flow.append(header.getlayer(port).sport)
            flow.append(header.getlayer(port).dport)
            flow.append(port.lower())

        #protocols without port or ip
        except:
            flow = exception_handler(header, layers)

        flows.append(flow)

    pcap_list = copy.deepcopy(flows)

    #merge duplicated (merge the same ip/port/proto for the same flow)
    s = set(tuple(l) for l in flows)
    flows = [list(t) for t in s]

    return flows, pcap_list
        
def get_flow_index(zeek, pcaps):

    n = len(zeek.index)
    index = np.empty((n, 0)).tolist()
    direction = [0 for i in range (len(pcaps))]

    for i in range(n):
        row = zeek.iloc[i, :]
        srcip, dstip, sport, dsport = row['srcip'], row['dstip'], row['sport'], row['dsport']

        for j, pcap in enumerate(pcaps):

            layers = []
            for layer in get_pcap_layers(pcap):
                layers.append(layer.name)

            try:
                ip = layers[1]
                trans = layers[2]

                #packets from src to dst
                if ((srcip == pcap.getlayer(ip).src) & (dstip == pcap.getlayer(ip).dst) & 
                    (sport == pcap.getlayer(trans).sport) & (dsport == pcap.getlayer(trans).dport)):
                    index[i].append(j)
                    direction[j] = 0

                #packets from dst to src
                elif ((srcip == pcap.getlayer(ip).dst) & (dstip == pcap.getlayer(ip).src) & 
                    (sport == pcap.getlayer(trans).dport) & (dsport == pcap.getlayer(trans).sport)):
                    index[i].append(j)
                    direction[j] = 1

            except:continue

    return index, direction


def preprossing(zeek):

    #if the log file hasn't been filtered in linux
    del zeek['uid']
    del zeek['local_orig']
    del zeek['local_resp']
    del zeek['missed_bytes']
    del zeek['history']
    del zeek['orig_ip_bytes']
    del zeek['resp_ip_bytes']
    del zeek['tunnel_parents']

    #change the key name to the same as NUSW dataset
    zeek.columns = ['Stime', 'srcip', 'sport', 'dstip', 'dsport', 'proto', 'service', 'dur', 'sbytes', 'dbytes', 'state', 'Spkts', 'Dpkts']

    return zeek

def fill_tcp_feature(zeek, pcaps, index, direction):

    swin, dwin, stcpb, dtcpb =[], [], [], []

    print(index)

    for i, idx in enumerate(index):

        if idx == []: 
            swin.append(0)
            dwin.append(0)
            stcpb.append(0)
            dtcpb.append(0)
            continue

        flow = zeek.iloc[i, :]
        swin_avg, dwin_avg = [], []
        flag_s=0
        flag_d=0
        
        first_pck = pcaps[idx[0]]

        if first_pck.haslayer('TCP') == False: 
            swin.append(0)
            dwin.append(0)
            stcpb.append(0)
            dtcpb.append(0)
            continue

        for value in idx:

            #first packet in each direction : can get base sequence number and window size
            if (direction[value] == 0) & (flag_s==0):
                flag_s=1
                stcpb.append(pcaps[value].getlayer('TCP').seq)
                swin_avg.append(pcaps[value].getlayer('TCP').window)

            elif (direction[value] == 1) & (flag_d==0):
                flag_d=1
                dtcpb.append(pcaps[value].getlayer('TCP').seq)
                dwin_avg.append(pcaps[value].getlayer('TCP').window)
                
            elif direction[value] == 0:
                swin_avg.append(pcaps[value].getlayer('TCP').window)
            
            elif direction[value] == 1:
                dwin_avg.append(pcaps[value].getlayer('TCP').window)
        

        if flag_d == 0:
            dtcpb.append(0)
        
        #calculate average window size for each flow
        try:
            swin.append(int(statistics.mean(swin_avg)))
        except:
            swin.append(0)

        try:
            dwin.append(int(statistics.mean(dwin_avg)))
        except:
            dwin.append(0)

            
    zeek = zeek.assign(swin = pd.Series(swin).values, dwin = pd.Series(dwin).values)
    zeek = zeek.assign(stcpb = pd.Series(stcpb).values, dtcpb = pd.Series(dtcpb).values)
    print(zeek)

    return zeek
    
                

if __name__ == '__main__':
    pcaps = sp.rdpcap('./logfile/test.pcap')
    n = len(pcaps)


    zeek = pd.read_csv('./logfile/conn.log.csv', low_memory=False)
    zeek = preprossing(zeek)

    #print(zeek.keys())
    #print(type(pcaps[230].getlayer('IP').id))

    #create flows with same src ip/ dst ip/ src port/ dst port/ proto


    #flows, pcap_list = create_flow(pcaps)

    #in each flow, get the index of the original packets
    index, direction = get_flow_index(zeek, pcaps)

    zeek = fill_tcp_feature(zeek, pcaps, index, direction)



