#???? -> shift + option + A
""" from sklearn.datasets import load_iris
import pandas as pd 
import numpy as np

iris_dataset = load_iris()
keys = iris_dataset.keys()
print(keys)
"""

import csv

#open the csv file 
with open ('NUSW-1000.csv', newline='') as csvfile:

    packets = pd.read_csv(csvfile)


#save label and attack_cat in an array (for comparison) 
label = packets['Label'].to_numpy()
attack_cat = packets['attack_cat'].to_numpy()
del packets['Label']
del packets['attack_cat']




