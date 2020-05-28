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


"""def create_flow(pcaps):
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

    return flows, pcap_list"""

def id_eq_http(flow, pkt):
    
    if ((flow['srcip'] == pkt['id_orig_h']) & (flow['dstip'] == pkt['id_resp_h']) 
    & (flow['sport'] == pkt['id_orig_p']) & (flow['dsport'] == pkt['id_resp_p'])):
        return True
    
    if  ((flow['dstip'] == pkt['id_orig_h']) & (flow['srcip'] == pkt['id_resp_h']) 
    & (flow['dsport'] == pkt['id_orig_p']) & (flow['sport'] == pkt['id_resp_p'])):
        return True
    
    return False
        
def get_flow_index(zeek, pcaps):

    n = len(zeek.index)
    index = np.empty((n, 0)).tolist()
    direction = [-1 for i in range (len(pcaps))]

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

    srcip_bytes = zeek['orig_ip_bytes'].tolist()
    dstip_bytes = zeek['resp_ip_bytes'].tolist()

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

    return zeek, srcip_bytes, dstip_bytes

def fill_tcp_feature(zeek, pcaps, index, direction):

    swin, dwin, stcpb, dtcpb =[], [], [], []

    #print(index)

    for i, idx in enumerate(index):

        if idx == []:
            swin.append(np.nan)
            dwin.append(0)
            stcpb.append(0)
            dtcpb.append(0)
            continue

        flow = zeek.iloc[i, :]
        swin_avg, dwin_avg = [], []
        flag_s=0
        flag_d=0
        syn=0
        syn_ack=0
        ack=0
        
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

            
            if pcaps[value].getlayer('TCP').flags == 'S':
                syn = 1

        

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

    return zeek
    

def fill_general_feature(zeek, index, srcip_bytes, dstip_bytes):
    
    smeansz, dmeansz, Ltime = [], [], []
    for i, idx in enumerate(index):

        if idx == []:
            smeansz.append(0)
            dmeansz.append(0)
            Ltime.append(0)
            continue

        flow = zeek.iloc[i,:]

        try:
            smeansz.append(int(int(srcip_bytes[i])/int(flow['Spkts'])))
        except ZeroDivisionError:
            smeansz.append(int(srcip_bytes[i]))

        try:
            dmeansz.append(int(int(dstip_bytes[i])/int(flow['Dpkts'])))
        except ZeroDivisionError:
            dmeansz.append(int(dstip_bytes[i]))

    zeek = zeek.assign(smeansz = pd.Series(smeansz).values, dmeansz = pd.Series(dmeansz).values)

    return zeek

def fill_ip_feature(zeek, pcaps, index, direction):

    sttl, dttl = [],[]

    for i, idx in enumerate(index):

        if idx == []:
            sttl.append(0)
            dttl.append(0)
            continue
        
        flag_s = 0
        flag_d = 0

        for value in idx:
            
            if (flag_s == 0) & (direction[value] == 0):
                sttl.append(pcaps[value].getlayer('IP').ttl)
                flag_s = 1
            
            elif (flag_d == 0) & (direction[value] == 1):
                dttl.append(pcaps[value].getlayer('IP').ttl)
                flag_d = 1

            if flag_d & flag_s:
                break

        if flag_d == 0:
            dttl.append(0)

    zeek = zeek.assign(sttl = pd.Series(sttl).values, dttl = pd.Series(dttl).values)

    return zeek

def fill_http_feature(zeek, pcaps, index):
    http = pd.read_csv('./logfile/http.log.csv')
    trans_depth, res_len = [], []

    for i in range (len(zeek.index)):

        flow = zeek.iloc[i,:]
        if flow['service'] != 'http':

            trans_depth.append(0)
            res_len.append(0)
            continue

        len_avg = []
        depth_tmp = 0

        for j in range(len(http.index)):
            
            pkt = http.iloc[j,:]
            if id_eq_http(flow, pkt):
                
                depth_tmp = int(pkt['trans_depth'])
                len_avg.append(int(pkt['response_body_len']))

        
        trans_depth.append(depth_tmp)

        try:
            res_len.append(int(statistics.mean(len_avg)))
        except:
            res_len.append(0)

    zeek = zeek.assign(trans_depth = pd.Series(trans_depth).values, res_len = pd.Series(res_len).values)

    return zeek
                

if __name__ == '__main__':
    pcaps = sp.rdpcap('./logfile/test.pcap')
    n = len(pcaps)

    zeek = pd.read_csv('./logfile/conn.log.csv', low_memory=False)
    zeek, srcip_bytes, dstip_bytes = preprossing(zeek)

    #print(zeek.keys())
    #print(type(pcaps[230].getlayer('IP').id))
    #print(pcaps[31].getlayer('TCP').options[2])

    #in each flow, get the index of the original packets
    index, direction = get_flow_index(zeek, pcaps)

    print(index)
    
    zeek = fill_http_feature(zeek, pcaps, index)
    zeek = fill_general_feature(zeek, index, srcip_bytes, dstip_bytes)
    zeek = fill_tcp_feature(zeek, pcaps, index, direction)
    zeek = fill_ip_feature(zeek, pcaps, index, direction)
    
    


