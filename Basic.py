"""
1. time based
2. feature based with no weight
3. feature based with important features
4. feature based with time weight
5. time slot + feature based
"""

imp_features = ['srcip','sport','dstip','dsport','proto','state','dur','sbytes']

import csv
import pandas as pd

with open('UNSW-1000.csv',  newline='') as csvfile:

    packets = pd.read_csv(csvfile)

label = packets['Label'].to_numpy()
attack_cat = packets['attack_cat'].to_numpy()
del packets['Label']
del packets['attack_cat']


#important features
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


#packets_time[0] = packets.copy()
#total number of packet
n = len(packets['srcip'])
base_t = packet.loc[[0]]['Ltime']
len_t = 5

for i in range n:
    if( packet.loc[[i]]['Ltime'] - base_t >= 5):
        #new time slot -> create new dataframe
        base_t = packet.loc[[i]]['Ltime']

    else:
        #same time slot -> append this packet to the same dataframe

print(packets.loc[[0]])



