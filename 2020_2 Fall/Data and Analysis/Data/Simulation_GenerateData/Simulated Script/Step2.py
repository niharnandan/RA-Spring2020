# import packages
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')


## DESCRIPTION OF THE SCRIPT
# Input:        TBA
# Output:       TBA
# Processing:   TBA


## INITIALIZE
print('Currently running STEP 2')
mypath= '../../../Data/RawData_OnlineExperiment/'
oloc = open("../Output_Location (Simulated).txt", "r").read()
f = open("values.txt").read().split('\n')
no_files = int(f[8])


## REPEAT FOR EVERY FILE IN THE FOLDER
for name in range(65,65+no_files):
    
    # Read file
    print('Running Step 2 for File', chr(name))
    temp1 = pd.read_csv('../Simulated_Data/simulation results '+chr(name)+'.csv', error_bad_lines=False)
    
    # Replace values (convert strings to numerical variables)
    temp1 = temp1.replace('red', 0)
    temp1 = temp1.replace('blue', 1)
    temp1 = temp1.rename(columns={"setup_cost": "rounds",})
    temp1 = temp1.rename(columns={"guilty_suspect_chosen": "true_guilty_suspect",})
    for i in range(1,63,1):
        temp1.insert(len(temp1.columns), 'outcome_'+str(i), np.nan)
    temp1['evidence_round'] = 0
    temp1['correct_suspect_accused'] = 0
    temp1['participant_ID'] = 0
    temp1['treatment'] = 0
    temp1['part'] = 2
    temp1['suspect_accused'] = 0
    for i in range(1,63): 
        temp1['timing_choice_'+str(i)] = 0
        
    # ??? Is this ever used?
    c = ['choice_' + str(i) for i in range(1,12)]

    # ??? ASK NIHAR
    temp = ['investigate_red','investigate_blue','accuse_red','accuse_blue','advance_to_next_trial', 'evidence_shown']

    # ??? ASK NIHAR
    for i in temp:
        temp1 = temp1.replace(i, temp.index(i))
    temp1.head()
    for key,value in temp1.iterrows():
        temp = temp1.iloc[key, 7:69].to_list()
        outcome = [x for x in temp if x != np.nan and (x == 5) or (x == 1) or (x == 0)]
        outcome = [1 if i == 5 else 0 for i in outcome]
        for i in range(1,len(outcome)+1):
            temp1['outcome_'+str(i)][key] = outcome[i-1]

    # ??? ASK NIHAR
        if (2 in temp and value[4] == 0) or (3 in temp and value[4] == 1): 
            temp1['correct_suspect_accused'][key] = 1 
        if 2 in temp: 
            temp1['suspect_accused'] == 0
        elif 3 in temp: 
            temp1['suspect_accused'] == 1

    # ??? ASK NIHAR
        if 5 in temp:
            temp1['evidence_round'][key] = temp.index(5)+1
            temp.remove(5)
            temp.append(np.nan)
        else: temp1['evidence_round'][key] = 0
        temp = [x if x == 1 or x == 0 else np.nan for x in temp]
        temp1.iloc[key, 7:69] = temp

    d3 = ['choice_'+str(i) for i in range(1,61)]
    d4 = ['outcome_'+str(i) for i in range(1,61)]
    d5 = ['timing_choice_'+str(i) for i in range(1,63)]
    temp1 = temp1.rename(columns={"rounds": "setup_cost_red",})
    temp1["setup_cost_blue"] =  temp1["setup_cost_red"]
    cols = ['participant_ID', 'treatment', 'part', 'trial_no', 
             'setup_cost_red', 'setup_cost_blue', 'red_prior_prob',
            'true_guilty_suspect', 'suspect_accused']+d3+d4+d5+['correct_suspect_accused', 'evidence_round']
    temp1 = temp1[cols]

    # Save output file
    temp1.to_csv(oloc+'Step2_'+chr(name)+'.csv', index=False)
    
    