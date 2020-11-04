import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

mypath= '../RawData_OnlineExperiment/'
files = [f for f in listdir(mypath)]
oloc = open("../Output_Location.txt", "r").read()

temp = [0]*len(files)
sum = 0
p_count = 0
for i in range(len(files)):
    temp[i] = pd.read_csv(mypath+files[i])
    temp[i] = temp[i].dropna(subset=['block_name'])
    p_count += 1
    temp[i]['participant_ID'] = p_count
    sum += temp[i].count()
for i in range(len(files)-1):
    temp[0] = temp[0].append(temp[i+1], ignore_index=True, sort=False)
temp1 = temp[0].copy(deep = True)
temp1['part'] = 0
temp1['treatment'] = 0
cols = ['treatment']
[temp1.columns.get_loc(c) for c in cols if c in temp1]
for key,value in temp1.iterrows():
    if 'part1' in value[1]: temp1['part'][key] = 1
    elif 'part2' in value[1]: temp1['part'][key] = 2
    else: temp1['part'][key] = 3
    if 'guilty' in value[1]: temp1['treatment'][key] = 1
    else: temp1['treatment'][key] = 0
temp1 = temp1.drop(columns=['block_name'])
for i in range(1,4):
    cols = temp1.columns.tolist()
    cols.remove('participant_ID')
    cols = ['participant_ID'] + cols
    temp1 = temp1[cols]
    temp2 = temp1.loc[temp1['part'] == i]
    temp2.to_csv(oloc+'Task'+str(i)+'.csv', index=False)