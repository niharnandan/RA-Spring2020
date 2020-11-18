import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from tqdm import tqdm
sns.set_style("darkgrid")
warnings.filterwarnings('ignore')
oloc = open("../Output_Location.txt", "r").read()
folder = ''
df_task1 = pd.read_csv(oloc+'Task1_step2.csv')
df_task2 = pd.read_csv(oloc+'Task2_step2.csv')
df_task3 = pd.read_csv(oloc+'Task3_step2.csv')

print('Running Task 1 :')

for key,value in tqdm(df_task1.iterrows()):
    if value[1] == 1:
        temp = df_task1.iloc[key, 8:17].to_list()
        df_task1.iloc[key, 8:17] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
df_task1.to_csv(oloc+'Task1_step3.csv', index=False)

print('Running Task 2 :')

for key,value in tqdm(df_task2.iterrows()):
    if value[1] == 1:
        temp = df_task2.iloc[key, 9:69].to_list()
        df_task2.iloc[key, 9:69] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
df_task2.to_csv(oloc+'Task2_step3.csv', index=False)

print('Running Task 3 :')

for key,value in tqdm(df_task3.iterrows()):
    if value[1] == 1:
        temp = df_task3.iloc[key, 9:69].to_list()
        df_task3.iloc[key, 9:69] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
df_task3.to_csv(oloc+'Task3_step3.csv', index=False)