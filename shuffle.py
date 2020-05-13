import pandas as pd
from sklearn.utils import shuffle


file = './dataset/NUSW_mix_4(unshuffle).csv'
dataset_raw = pd.read_csv(file, low_memory=False)

dataset_raw = dataset_raw.sample(frac=1).reset_index(drop=True)

dataset_raw.to_csv('./dataset/NUSW_mix_4.csv')