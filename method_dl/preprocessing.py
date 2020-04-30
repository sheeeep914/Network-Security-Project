from sklearn.preprocessing import MinMaxScaler


imp_features = ['srcip', 'sport', 'dstip', 'dsport', 'proto',
                'state', 'dur', 'sbytes', 'Stime', 'Ltime', 'service']
http_features = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'dur', 'ct_dst_ltm', 'ct_src_ ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'Label', 'attack_cat']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN', 'CON', 'REQ', 'URH', 'ACC', 'CLO',  'ECO', 'ECR', 'INT', 'MAS', 'PAR',  'RST', 'TST', 'TXD',  'URN']
service = ['http', 'dns', 'ftp-data', 'smtp', 'ssh', 'irc']


def seperate_att_label(packets):

    label = packets['Label'].to_numpy()
    attack_cat = packets['attack_cat'].to_numpy()
    del packets['Label']
    del packets['attack_cat']
    return label, attack_cat, packets


def proto_to_value(packets):
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

    return packets
    #print(packets.keys())


def state_to_value(packets):

    for element in states:
        state_list = []
        for state in packets['state']:

            if(state == element):
                state_list.append(1)
            else:
                state_list.append(0)

        packets[element] = state_list

    del packets['state']

    return packets
    #print(packets.keys())


def service_to_value(packets):

    for element in service:
        service_list = []
        for serv in packets['service']:

            if(serv == element):
                service_list.append(1)
            else:
                service_list.append(0)

        packets[element] = service_list

    del packets['service']

    return packets
    #print(packets.keys())


def ip_to_value(packets):
    #ip is stored as string
    #print(type(packets.loc[1]['srcip']))

    n = len(packets)

    srcip = packets['srcip']
    dstip = packets['dstip']

    srcip1, srcip2, dstip1, dstip2 = [], [], [], []

    for i in range(n):
        srcip_split = srcip[i].split(".")
        dstip_split = dstip[i].split(".")

        srcip1.append(int(srcip_split[0], base=10))
        srcip2.append(int(srcip_split[1], base=10))

        dstip1.append(int(dstip_split[0], base=10))
        dstip2.append(int(dstip_split[1], base=10))

    packets['srcip1'], packets['srcip2'] = srcip1, srcip2
    packets['dstip1'], packets['dstip2'] = dstip1, dstip2

    del packets['srcip'], packets['dstip']

    return packets
    #print(packets.keys())


#important features
def get_http(packets):
    http_features_n = len(http_features)
    #cnt = 0

    packets_http = packets.copy()
    for col in (packets_http.columns):
        for i in range(http_features_n):

            #important features, check the next column
            if (col == http_features[i]):
                break

            #no important features match, and last feature has been checked
            elif ((col != http_features[i]) & (i == http_features_n-1)):
                del packets_http[col]

    return packets_http

#important http feature


def get_imp(packets):
    imp_features_n = len(imp_features)
    cnt = 0

    packets_imp = packets.copy()
    for col in (packets_imp.columns):
        for i in range(imp_features_n):

            #important features, check the next column
            if (col == imp_features[i]):
                break

            #no important features match, and last feature has been checked
            elif ((col != imp_features[i]) & (i == imp_features_n-1)):
                del packets_imp[col]

    return packets_imp


def del_tcp_features(packets):
    del packets['swin']
    del packets['dwin']
    del packets['stcpb']
    del packets['dtcpb']
    del packets['tcprtt']
    del packets['synack']
    del packets['ackdat']

    return packets

#normalization
def feature_scaling(packets):
    sc = MinMaxScaler(feature_range=(0, 1))
    packets_scaled = sc.fit_transform(packets)

    return packets_scaled


def normalization(packets, features):
    for f in features:
        packets[f] = (packets[f] - packets[f].min()) /\
            (packets[f].max() - packets[f].min())

    return packets

