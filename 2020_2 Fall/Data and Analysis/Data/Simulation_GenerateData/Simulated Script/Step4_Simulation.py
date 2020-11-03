# import packages
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


## DESCRIPTION OF THE SCRIPT
# Input:        TBA
# Output:       TBA
# Processing:   TBA


## INITIALIZE
print('Currently running STEP 4')
f = open("values.txt").read().split('\n')
no_files = int(f[8])
oloc = open("../Output_Location (Simulated).txt", "r").read()

## REPEAT FOR EVERY FILE IN THE FOLDER
for name in range(65,65+no_files):

    print('Running Step 4 for File', chr(name))
    # Read file
    step4_df = pd.read_csv(oloc+'Step2_'+chr(name)+'.csv')
    step4_df.head()
    data = []

    #Iterating over rows in the dataframe. 
    for key,value in tqdm(step4_df.iterrows()):
        info_b = value[:7].to_list()
        info_e = value[7:9].to_list()
        rounds = value[9:69].to_list()
        rounds = [x for x in rounds if x == 1.0 or x == 0.0]
        suspect = []
        post = value[6]
        #if value[3] == 1: print(len(rounds))
        e_f = 0 #evidence found variable
        e_s = -1 #evidence suspect
        i = 1

    # Iterate over every action and append new row to dataframe
        for i in range(len(rounds)):
            suspect.append(rounds[i])
            pg = 0.75 if suspect[-1] == 0 else 1
            pi = 1 if suspect[-1] == 0 else 0.75
            temp = [i+1, 0, suspect[-1], suspect[:-1].count(0.0), 
                   suspect[:-1].count(1.0), e_f, e_s]
            data.append(info_b+temp+[post]+info_e+[step4_df['timing_choice_'+str(i+1)][key]])
            post = post*pg/(post*pg + pi*(1-post))

            e_f = int(value[69+i]) if e_f != 1 else 1
            if e_f == 1: 
                e_s = value[8]
            else: e_f = 1 if e_f == 1 and i != 0 else 0
            post = value[7] if e_f == 1 else post

    # Store accuse row. 
        if len(rounds) == 0:
            i = 0
        else:
            i += 1
            e_f = int(value[69+i]) if e_f != 1 else 1
            if e_f == 1: e_s = value[8]
            else: e_f = 1 if e_f == 1 and i != 0 else 0
            post = value[7] if e_f == 1 else post
        suspect.append(value[7])
        temp = [i+1, 1, suspect[-1], suspect[:-1].count(0.0), suspect[:-1].count(1.0), e_f, e_s]
        data.append(info_b+temp+[post]+info_e+[step4_df['timing_choice_'+str(i+2)][key]])
        
    # Columns for the output file
    cols = ['participant_ID', 'treatment', 'part', 'trial_no', 'setup_cost_red', 'setup_cost_blue',
           'red_prior_prob', 'current_rounds', 'action_type', 'suspect', 
            'count_red_samples', 'count_blue_samples', 'evidence_found',
           'evidence_suspect', 'posterior', 'true_guilty_suspect', 'suspect_accused',
           'time']
    df2 = pd.DataFrame(data,columns=cols)
    df2.head()
    df2 = df2.fillna(0)
    
    # Save output file
    df2.to_csv(oloc+'Step4_'+chr(name)+'.csv', index=False)
    
    