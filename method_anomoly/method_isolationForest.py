from sklearn.ensemble import IsolationForest
import numpy as np

def isolation_forest(packets):
    model = IsolationForest()
    forest = model.fit(packets)
    return forest

def outlier_predict(forest, packets_test, label):
    output = forest.predict(packets_test)
    score=[]
    right = 0

    for i in range (len(label)):


        lab0 = label[i]
        lab1 = output[i]

        #malicious packets and outlier ( predict as malicious)
        if (lab0 == 1) & (lab1 == -1):
            score.append(1)
            right =right+1

        #malicious packets and inlier ( predict as normal)
        elif (lab0 == 1) & (lab1 == 1):
            score.append(0)

        #normal packets and dbscan outlier ( predict as malicious)
        elif (lab0 == 0) & (lab1 == -1):
            score.append(0)

        #normal packets and dbscan inlier ( predict as normal)
        elif (lab0 == 0) & (lab1 == 1):
            score.append(1)
            right = right+1

    #print(score)
    print(right/len(label))


