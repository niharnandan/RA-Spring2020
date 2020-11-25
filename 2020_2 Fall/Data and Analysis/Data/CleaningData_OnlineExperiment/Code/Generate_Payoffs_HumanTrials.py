## IMPORT PACKAGES
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')


## PATH
oloc = open("../Output_Location.txt", "r").read()
#files.remove('.DS_Store')


## CREATE FILE

df = pd.read_csv(oloc+'Task1_step4.csv')
players = list(set(df['participant_ID'].to_list()))

t1 = np.array([[int(i),0] for i in players])
for key,value in df.iterrows():
    if value[7] == 1:
        if value[-2] == value[-3]:
            t1[list(t1[:,0]).index(value[0]),1] += 1000


temp2 = pd.read_csv(oloc+'Task2_step4.csv')
players = list(set(temp2['participant_ID'].to_list()))

t2 = np.array([[int(i),0] for i in players])
for key,value in temp2.iterrows():
    if value[8] == 1:
        # suspect_accused == true_guilty_suspect
        if value[-2] == value[-3]:
            # 1000 - setup_cost_red*count_red_samples - setup_cost_blue*count_blue_samples
            t2[list(t2[:,0]).index(value[0]),1] += 1500 - value[4]*value[10] - value[5]*value[11]
        else:
            t2[list(t2[:,0]).index(value[0]),1] += 500 - value[4]*value[10] - value[5]*value[11]

            
temp3 = pd.read_csv(oloc+'Task3_step4.csv')
players = list(set(temp3['participant_ID'].to_list()))

t3 = np.array([[int(i),0] for i in players])
for key,value in temp3.iterrows():
    if value[8] == 1:
        if value[-2] == value[-3]:
            t3[list(t3[:,0]).index(value[0]),1] += 1500 - value[4]*value[10] - value[5]*value[11]
        else:
            t3[list(t3[:,0]).index(value[0]),1] += 500 - value[4]*value[10] - value[5]*value[11]

df = pd.DataFrame(t3, columns=['participant_ID', 'task_3'])
df['task_2'] = t2[:,1]
df['task_1'] = t1[:,1]

## SAVE FILE
df.to_csv(oloc+'payoff.csv', index=False)





