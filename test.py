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

    #read the content
    rows = csv.reader(csvfile)

    #print out each row using a loop
    for row in rows:
        print(row)



