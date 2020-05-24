import scapy.all as sp
import copy
import numpy as np

def get_packet_layers(packet):
    counter = 0
    while True:
        layer = packet.getlayer(counter)
        if layer is None:
            break

        yield layer
        counter += 1

def exception_handler(header, layers):

    flow = []

    if layers[1] == 'ARP':
        arp = header.getlayer('ARP')
        flow = [arp.psrc, arp.pdst, 0, 0, 'arp']

    elif layers[2] == 'ICMP':
        ip = header.getlayer('IP')
        flow = [ip.src, ip.dst, 0, 0, 'icmp']

    else:
        flow = ['0.0.0.0', '0.0.0.0', 0, 0, '-']

    return flow


def create_flow(pcaps):
    n = len(pcaps)
    layers = []
    flows = []

    for i, header in enumerate(pcaps):
        
        layers = []
        flow = []

        for layer in get_packet_layers(header):
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
        
def get_flow_index(flows, pcaps):

    index = np.empty((len(flows), 0)).tolist()

    for i, flow in enumerate(flows):
        for j, pcap in enumerate(pcaps):
            if flow == pcap:
                index[i].append(j)

    return index

def merge_flow(flows, index):
    for i, flow in enumerate(flows):
        print(i,flow)
    
    n = len(flows)
    del_list=[]
    mark = [0]*n

    for i, header_i in enumerate(flows):

        if mark[i] == 1:
            continue
        
        src_i, dst_i, sport_i, dport_i, proto_i = header_i[0], header_i[1], header_i[2], header_i[3], header_i[4] 

        for j, header_j in enumerate(flows[i+1:n]):
            
            if j <= i: continue 
            if mark[j] == 1: continue
            
            src_j, dst_j, sport_j, dport_j, proto_j = header_j[0], header_j[1], header_j[2], header_j[3], header_j[4] 
            
            #bidirectional connection with src and dst switch
            if (src_i==dst_j) & (dst_i==src_j) & (sport_i==dport_j) & (dport_i==sport_j) & (proto_i==proto_j):
                
                index[i].extend(index[j])
                del_list.append(j)
                mark[j] = 1

    for item in del_list:
        del index[item]
        del flows[item]

    print(del_list)
    """print("==================================")
    for flow in flows:
        print((flow))
    print("======================")
    for i in index:
        print(i)"""
                

if __name__ == '__main__':
    pcaps = sp.rdpcap('test.pcap')
    n = len(pcaps)

    #print(type(pcaps[230].getlayer('IP').id))

    #create flows with same src ip/ dst ip/ src port/ dst port/ proto
    flows, pcap_list = create_flow(pcaps)

    #in each flow, get the index of the original packets
    index = get_flow_index(flows, pcap_list)

    #if srcip, srcport and dstip, dstport is swap, see as the same bidirectional connection
    merge_flow(flows, index)

