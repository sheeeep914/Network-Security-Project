from sklearn.cluster import DBSCAN
import numpy as np
import sys

def DBscan_fixed_eps(packets, eps):
    model = DBSCAN(eps=eps, min_samples=5)
    dbscan = model.fit(packets)
    np.set_printoptions(threshold=sys.maxsize) #???

    group_number_list = dbscan.labels_

    max_label = 0
    for label in group_number_list:
        if label > max_label:
            max_label = label

    #max_label + 1 -> 分幾群
    #print(max_label)

    return max_label, group_number_list

    

