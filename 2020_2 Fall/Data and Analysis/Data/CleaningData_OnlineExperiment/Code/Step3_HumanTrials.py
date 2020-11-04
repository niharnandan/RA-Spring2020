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
temp1 = pd.read_csv(oloc+'Task1_step2.csv')
temp2 = pd.read_csv(oloc+'Task2.csv')
temp3 = pd.read_csv(oloc+'Task3.csv')

for key,value in tqdm(temp1.iterrows()):
    if value[1] == 0:
        temp = temp1.iloc[key, 8:17].to_list()
        temp1.iloc[key, 8:17] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
temp1.to_csv(oloc+'Task1_step3.csv', index=False)

for key,value in tqdm(temp2.iterrows()):
    if value[1] == 0:
        temp = temp2.iloc[key, 9:69].to_list()
        temp2.iloc[key, 9:69] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
temp2.to_csv(oloc+'Task2_step3.csv', index=False)

for key,value in tqdm(temp3.iterrows()):
    if value[1] == 0:
        temp = temp3.iloc[key, 9:69].to_list()
        temp3.iloc[key, 9:69] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
temp3.to_csv(oloc+'Task3_step3.csv', index=False)