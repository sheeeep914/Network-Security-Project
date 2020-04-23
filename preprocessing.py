imp_features = ['srcip', 'sport', 'dstip', 'dsport', 'proto', 'state', 'dur', 'sbytes', 'Stime', 'Ltime', 'service']
proto = ['tcp', 'udp', 'arp', 'ospf']
states = ['FIN', 'CON', 'REQ', 'URH', 'ACC', 'CLO',  'ECO', 'ECR', 'INT', 'MAS', 'PAR',  'RST', 'TST', 'TXD',  'URN']
service = ['http', 'dns', 'ftp-data', 'smtp', 'ssh', 'irc']


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

#Standardization -> mean = 0, var = 1
#Normalization -> min = 0, max = 1
""" def time_normalization():
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
        (packets['Dload'].max() - packets['Dload'].min()) """


def normalization(packets, features):
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
