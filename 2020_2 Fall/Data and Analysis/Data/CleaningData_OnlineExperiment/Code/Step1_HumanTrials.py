## IMPORT PACKAGES
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


## SET THE PATH
mypath= '../RawData_OnlineExperiment/'
files = [f for f in listdir(mypath)]
oloc = open("../Output_Location.txt", "r").read()
files.remove('.DS_Store')
## SHOW THE LIST OF FILES IN THE FOLDER (FOR DEBUGGING) 
# print(files)


## LOOP OVER THE SUBJECT FILES TO GENERATE A SINGLE WIDE DATASET
temp = [0]*len(files)
sum = 0
p_count = 0
for i in range(len(files)):
    temp[i] = pd.read_csv(mypath+files[i])
    temp[i] = temp[i].dropna(subset=['block_name'])
    p_count += 1
    temp[i]['participant_ID'] = p_count
    sum += temp[i].count()

#Iterate over every file and add to 1 master dataframe
for i in range(len(files)-1):
    temp[0] = temp[0].append(temp[i+1], ignore_index=True, sort=False)
df = temp[0].copy(deep = True)
#Create part and treatment columns with initial value as 0
df['part'] = 0
df['treatment'] = 0
cols = ['treatment']
[df.columns.get_loc(c) for c in cols if c in df]

#Iterate over dataframe and split into parts 1,2,3 and guilty treatment
for key,value in df.iterrows():
    if 'part1' in value[1]: df['part'][key] = 1
    elif 'part2' in value[1]: df['part'][key] = 2
    else: df['part'][key] = 3
    if 'guilty' in value[1]: df['treatment'][key] = 1
    else: df['treatment'][key] = 0
df = df.drop(columns=['block_name'])

#Create output dataframe as step 1 for each task
for i in range(1,4):
    cols = df.columns.tolist()
    cols.remove('participant_ID')
    cols = ['participant_ID'] + cols
    df = df[cols]
    temp2 = df.loc[df['part'] == i]
    temp2.to_csv(oloc+'Task'+str(i)+'.csv', index=False)