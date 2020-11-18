import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import warnings
from tqdm import tqdm
import seaborn as sns
sns.set_style("darkgrid")
warnings.filterwarnings('ignore')

folder = ''
oloc = open("../Output_Location.txt", "r").read()
df = pd.read_csv(oloc+'Task1_step3.csv')

print('Running Task 1 :')

df.head()
data = []
for key,value in tqdm(df.iterrows()):
    info_b = value[:6].to_list()
    info_e = value[6:8].to_list()
    rounds = value[8:17].to_list()
    rounds = [x for x in rounds if x == 1.0 or x == 0.0]
    suspect = []
    post = value[5]
    e_f = 0
    e_s = -1
    for i in range(len(rounds)):
        suspect.append(rounds[i])
        pg = 0.75 if suspect[-1] == 0 else 1
        pi = 1 if suspect[-1] == 0 else 0.75
        temp = [i+1, 0, suspect[-1], suspect[:-1].count(1.0), 
               suspect[:-1].count(0.0), e_f, e_s]
        data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+1)][key]])
        post = post*pi/(post*pi + pg*(1-post))
        e_f = int(value[17+i]) if e_f != 1 else 1
        if e_f == 1: 
            e_s = value[7]
        else: e_f = 1 if e_f == 1 and i != 0 else 0
        post = value[7] if e_f == 1 else post
    temp = [i+2, 1, value[7], suspect.count(1.0), suspect.count(0.0), e_f, e_s]
    data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+2)][key]])
cols = ['participant_ID', 'treatment', 'part', 'trial_no', 'rounds',
       'red_prior_prob', 'current_rounds', 'action_type', 'suspect', 
        'count_red_samples', 'count_blue_samples', 'evidence_found',
       'evidence_suspect', 'posterior', 'true_guilty_suspect', 'suspect_accused',
       'time']
df2 = pd.DataFrame(data,columns=cols)
df2.head()
df2.to_csv(oloc+'Task1_step4.csv', index=False)

folder = ''
df = pd.read_csv(oloc+'Task2_step3.csv')

print('Running Task 2 :')

df.head()
data = []
for key,value in tqdm(df.iterrows()):
    info_b = value[:7].to_list()
    info_e = value[7:9].to_list()
    rounds = value[9:69].to_list()
    rounds = [x for x in rounds if x == 1.0 or x == 0.0]
    suspect = []
    post = value[6]
    #if value[3] == 1: print(len(rounds))
    e_f = 0
    e_s = -1
    for i in range(len(rounds)):
        suspect.append(rounds[i])
        pg = 0.75 if suspect[-1] == 0 else 1
        pi = 1 if suspect[-1] == 0 else 0.75
        temp = [i+1, 0, suspect[-1], suspect[:-1].count(0.0), 
               suspect[:-1].count(1.0), e_f, e_s]
        data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+1)][key]])
        post = post*pg/(post*pg + pi*(1-post))
        
        e_f = int(value[69+i]) if e_f != 1 else 1
        if e_f == 1: 
            e_s = value[8]
        else: e_f = 1 if e_f == 1 and i != 0 else 0
        post = value[7] if e_f == 1 else post
    if len(rounds) == 1 or len(rounds) == 0: i = 0
    suspect.append(value[7])
    if len(rounds) == 0: i = -1
    temp = [i+2, 1, suspect[-1], suspect[:-1].count(0.0), suspect[:-1].count(1.0), e_f, e_s]
    data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+2)][key]])
cols = ['participant_ID', 'treatment', 'part', 'trial_no', 'setup_cost_red', 'setup_cost_blue',
       'red_prior_prob', 'current_rounds', 'action_type', 'suspect', 
        'count_red_samples', 'count_blue_samples', 'evidence_found',
       'evidence_suspect', 'posterior', 'true_guilty_suspect', 'suspect_accused',
       'time']
df2 = pd.DataFrame(data,columns=cols)
df2.head()
df2 = df2.fillna(0)
df2.to_csv(oloc+'Task2_step4.csv', index=False)

folder = ''
df = pd.read_csv(oloc+'Task3_step3.csv')

print('Running Task 3 :')

data = []
for key,value in tqdm(df.iterrows()):
    info_b = value[:7].to_list()
    info_e = value[7:9].to_list()
    rounds = value[9:69].to_list()
    rounds = [x for x in rounds if x == 1.0 or x == 0.0]
    suspect = []
    post = value[6]
    
    e_f = 0
    e_s = -1
    for i in range(len(rounds)):
        suspect.append(rounds[i])
        pg = 0.75 if suspect[-1] == 0 else 1
        pi = 1 if suspect[-1] == 0 else 0.75
        temp = [i+1, 0, suspect[-1], suspect[:-1].count(0.0), 
               suspect[:-1].count(1.0), e_f, e_s]
        data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+1)][key]])
        post = post*pg/(post*pg + pi*(1-post))
        
        e_f = int(value[69+i]) if e_f != 1 else 1
        if e_f == 1: 
            e_s = value[8]
        else: e_f = 1 if e_f == 1 and i != 0 else 0
        post = value[7] if e_f == 1 else post
    if len(rounds) == 1 or len(rounds) == 0: i = 0
    suspect.append(value[7])
    if len(rounds) == 0: i = -1
    temp = [i+2, 1, suspect[-1], suspect[:-1].count(0.0), suspect[:-1].count(1.0), e_f, e_s]
    data.append(info_b+temp+[post]+info_e+[df['timing_choice_'+str(i+2)][key]])
cols = ['participant_ID', 'treatment', 'part', 'trial_no', 'setup_cost_red', 'setup_cost_blue',
       'red_prior_prob', 'current_rounds', 'action_type', 'suspect', 
        'count_red_samples', 'count_blue_samples', 'evidence_found',
       'evidence_suspect', 'posterior', 'true_guilty_suspect', 'suspect_accused',
       'time']
df2 = pd.DataFrame(data,columns=cols)
df2.head()
df2 = df2.fillna(0)
df2.to_csv(oloc+'Task3_step4.csv', index=False)