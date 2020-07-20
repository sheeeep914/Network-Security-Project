import pandas as pd

csv_file_1 = ['UNSW-NB15_3.csv']
csv_file = ['UNSW-NB15_1.csv', 'UNSW-NB15_2.csv', 'UNSW-NB15_3.csv', 'UNSW-NB15_4.csv']

df_ref = pd.read_csv('UNSW-NB15_1.csv')
df = pd.DataFrame(columns = df_ref.keys())
cnt = 0

"""for file in csv_file:
    df_ref = pd.read_csv(file, low_memory=False)
    attack_cat = df_ref['attack_cat']

    for i, ele in enumerate(attack_cat):
        if ele == 'Worms':
            df = df.append(df_ref.iloc[i], ignore_index=True)

        elif ele == 'Reconnaissance':
            cnt  = cnt+1
            if cnt > 200:
                continue
            df = df.append(df_ref.iloc[i], ignore_index=True)"""

for file in csv_file_1:
    df_ref = pd.read_csv(file, low_memory=False)
    attack_cat = df_ref['attack_cat']

    for i, ele in enumerate(attack_cat):

        if ele == 'Reconnaissance':
            cnt  = cnt+1
            if cnt > 200:
                break
            df = df.append(df_ref.iloc[i], ignore_index=True)

        
            
    #print(df_based)

df.to_csv('label7.csv')