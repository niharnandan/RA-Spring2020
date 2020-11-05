import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')
mypath= '../../../Data/RawData_OnlineExperiment/'
oloc = open("../Output_Location.txt", "r").read()

temp1 = pd.read_csv(oloc+'Task1.csv')

d_columns = ['choice_'+str(i) for i in range(12,63)]
d_columns += ['timing_choice_'+str(i) for i in range(12,63)]
d_columns += ['evidence_red_'+str(i) for i in range(10,31)]
d_columns += ['evidence_blue_'+str(i) for i in range(10,31)]
d_columns += ['num_evidences_total', 'final_evidence', 'bonus_earned', 
        'trial_chosen_for_bonus', 'total_bonus_paid_cents', 'setup_cost_investigate_red',
              'setup_cost_investigate_blue', 'timing_valid', 'timing_error', 
             'choice_10', 'choice_11']
temp1 = temp1.drop(columns = d_columns)
temp1 = temp1.replace('red', 0)
temp1 = temp1.replace('blue', 1)
temp1 = temp1.rename(columns={"setup_cost": "rounds",})# 'guilty_suspect_chosen': 'true_guilty_suspect'})
temp1['true_guilty_suspect'] = 0
temp1['evidence_round'] = 0
for i in range(9,0,-1):
    temp1.insert(48, 'outcome_'+str(i), np.nan)
temp1.correct_suspect_accused = temp1.correct_suspect_accused.astype(int)

c = ['choice_' + str(i) for i in range(1,12)]
temp = ['investigate_red','investigate_blue','accuse_red','accuse_blue','advance_to_next_trial']

for i in temp:
    temp1 = temp1.replace(i, temp.index(i))
    
evr_col = temp1.columns.to_list().index('evidence_red_1')
evb_col = temp1.columns.to_list().index('evidence_blue_1')
out_col = temp1.columns.to_list().index('outcome_1')
choice_col = temp1.columns.to_list().index('choice_1')
for key,value in tqdm(temp1.iterrows()):
    temp1['true_guilty_suspect'][key] = temp1['suspect_accused'][key] ^ 1 if temp1['correct_suspect_accused'][key] == 0 else temp1['suspect_accused'][key]
    temp = []
    counter_r = 0
    counter_b = 0
    for i in range(9):
        if value[i+5] == 0:
            temp.append(1) if value[evr_col+counter_r] == 1 else temp.append(0)
            counter_r += 1
        elif value[i+5] == 1:
            temp.append(1) if value[evb_col+counter_b] == 1 else temp.append(0)
            counter_b += 1
    for i in range(1,len(temp)+1):
        temp1['outcome_'+str(i)][key] = temp[i-1]
    
    temp = temp1.iloc[key, out_col:].to_list()
    temp1['evidence_round'][key] = temp.index(1.0)+1 if 1 in temp else 0
    
    temp = temp1.iloc[key, choice_col:choice_col+9].to_list()
    temp = [x if x == 1 or x == 0 else np.nan for x in temp]
    temp1.iloc[key, choice_col:choice_col+9] = temp

d_columns = ['evidence_red_1', 'evidence_red_2', 'evidence_red_3', 
        'evidence_red_4', 'evidence_red_5', 'evidence_red_6', 
        'evidence_red_7', 'evidence_red_8', 'evidence_red_9', 
        'evidence_blue_1', 'evidence_blue_2', 'evidence_blue_3', 
        'evidence_blue_4', 'evidence_blue_5', 'evidence_blue_6', 
        'evidence_blue_7', 'evidence_blue_8', 'evidence_blue_9']
temp1 = temp1.drop(columns = d_columns)

cols = ['participant_ID', 'treatment', 'part', 'trial_no', 
         'rounds', 'red_prior_prob',
        'true_guilty_suspect', 'suspect_accused',  
        'choice_1', 'choice_2', 'choice_3', 'choice_4', 'choice_5', 
        'choice_6', 'choice_7', 'choice_8', 'choice_9', 'outcome_1', 'outcome_2',
        'outcome_3', 'outcome_4', 'outcome_5', 'outcome_6', 'outcome_7', 'outcome_8', 'outcome_9',
        'timing_choice_1', 'timing_choice_2', 
        'timing_choice_3', 'timing_choice_4', 'timing_choice_5', 
        'timing_choice_6', 'timing_choice_7', 'timing_choice_8', 
        'timing_choice_9', 'timing_choice_10', 'timing_choice_11', 
        
        'correct_suspect_accused', 'evidence_round']
temp1 = temp1[cols]
temp1.to_csv(oloc+'Task1_step2.csv', index=False)

folder = ''
temp1 = pd.read_csv(oloc+'Task2.csv')
drop_columns = ['num_evidences_total', 'final_evidence', 'bonus_earned', 
        'trial_chosen_for_bonus', 'total_bonus_paid_cents', 'timing_valid', 'timing_error']
num_rounds = 60
temp1 = temp1.drop(columns = drop_columns)
temp1 = temp1.replace('red', 0)
temp1 = temp1.replace('blue', 1)
temp1['true_guilty_suspect'] = 0
temp1['evidence_round'] = 0

for i in range(num_rounds,0,-1):
    temp1.insert(68, 'outcome_'+str(i), np.nan)
temp1.correct_suspect_accused = temp1.correct_suspect_accused.astype(int)

temp = ['investigate_red','investigate_blue','accuse_red','accuse_blue','advance_to_next_trial']

for i in temp:
    temp1 = temp1.replace(i, temp.index(i))
temp1.astype({'suspect_accused': 'int'}).dtypes
temp1.astype({'correct_suspect_accused': 'int'}).dtypes
p_count = 0
for key,value in tqdm(temp1.iterrows()):
    temp1['true_guilty_suspect'][key] = int(temp1['suspect_accused'][key]) ^ 1 if temp1['correct_suspect_accused'][key] == 0 else temp1['suspect_accused'][key]
    temp = []
    counter_r = 0
    counter_b = 0
    for i in range(num_rounds):
        if value[i+7] == 0:
            temp.append(1) if value[191+counter_r] == 1 else temp.append(0)
            counter_r += 1
        elif value[i+7] == 1:
            temp.append(1) if value[221+counter_b] == 1 else temp.append(0)
            counter_b += 1
    for i in range(1,len(temp)+1):
        temp1['outcome_'+str(i)][key] = temp[i-1]
    
    temp = temp1.iloc[key, 68:130].to_list()
    temp1['evidence_round'][key] = temp.index(1.0)+1 if 1 in temp else 0
    
    
    temp = temp1.iloc[key, 7:67].to_list()
    temp = [x if x == 1 or x == 0 else np.nan for x in temp]
    temp1.iloc[key, 7:67] = temp

d1 = ['evidence_red_'+str(i) for i in range(1,31)]
d2 = ['evidence_blue_'+str(i) for i in range(1,31)]
d3 = ['choice_'+str(i) for i in range(1,61)]
d4 = ['outcome_'+str(i) for i in range(1,61)]
d5 = ['timing_choice_'+str(i) for i in range(1,63)]
d_columns = d1+d2
temp1 = temp1.drop(columns = d_columns)
temp1['setup_cost_blue'] = temp1['setup_cost']
temp1 = temp1.rename(columns={"setup_cost": "setup_cost_red",})# 'guilty_suspect_chosen': 'true_guilty_suspect'})
cols = ['participant_ID', 'treatment', 'part', 'trial_no', 
         'setup_cost_red', 'setup_cost_blue', 'red_prior_prob',
        'true_guilty_suspect', 'suspect_accused']+d3+d4+d5+['correct_suspect_accused', 'evidence_round']
temp1 = temp1[cols]
temp1.to_csv(oloc+'Task2_step2.csv', index=False)

folder = ''
temp1 = pd.read_csv(oloc+'Task3.csv')
drop_columns = ['num_evidences_total', 'final_evidence', 'bonus_earned', 
        'trial_chosen_for_bonus', 'total_bonus_paid_cents', 'timing_valid', 'timing_error']
num_rounds = 60
temp1 = temp1.drop(columns = drop_columns)
temp1 = temp1.replace('red', 0)
temp1 = temp1.replace('blue', 1)
temp1['true_guilty_suspect'] = 0
temp1['evidence_round'] = 0

for i in range(num_rounds,0,-1):
    temp1.insert(68, 'outcome_'+str(i), np.nan)
temp1.correct_suspect_accused = temp1.correct_suspect_accused.astype(int)

temp = ['investigate_red','investigate_blue','accuse_red','accuse_blue','advance_to_next_trial']

for i in temp:
    temp1 = temp1.replace(i, temp.index(i))
temp1.astype({'suspect_accused': 'int'}).dtypes
temp1.astype({'correct_suspect_accused': 'int'}).dtypes
p_count = 0
for key,value in tqdm(temp1.iterrows()):
    temp1['true_guilty_suspect'][key] = int(temp1['suspect_accused'][key]) ^ 1 if temp1['correct_suspect_accused'][key] == 0 else temp1['suspect_accused'][key]
    temp = []
    counter_r = 0
    counter_b = 0
    for i in range(num_rounds):
        if value[i+7] == 0:
            temp.append(1) if value[191+counter_r] == 1 else temp.append(0)
            counter_r += 1
        elif value[i+7] == 1:
            temp.append(1) if value[221+counter_b] == 1 else temp.append(0)
            counter_b += 1
    for i in range(1,len(temp)+1):
        temp1['outcome_'+str(i)][key] = temp[i-1]
    
    temp = temp1.iloc[key, 68:130].to_list()
    temp1['evidence_round'][key] = temp.index(1.0)+1 if 1 in temp else 0
    
    
    temp = temp1.iloc[key, 7:67].to_list()
    temp = [x if x == 1 or x == 0 else np.nan for x in temp]
    temp1.iloc[key, 7:67] = temp

d1 = ['evidence_red_'+str(i) for i in range(1,31)]
d2 = ['evidence_blue_'+str(i) for i in range(1,31)]
d3 = ['choice_'+str(i) for i in range(1,61)]
d4 = ['outcome_'+str(i) for i in range(1,61)]
d5 = ['timing_choice_'+str(i) for i in range(1,63)]
d_columns = d1+d2
temp1 = temp1.drop(columns = d_columns)
temp1 = temp1.rename(columns={"setup_cost_investigate_red": "setup_cost_red",
                             "setup_cost_investigate_blue": "setup_cost_blue"})# 'guilty_suspect_chosen': 'true_guilty_suspect'})
cols = ['participant_ID', 'treatment', 'part', 'trial_no', 
         'setup_cost_red', 'setup_cost_blue', 'red_prior_prob',
        'true_guilty_suspect', 'suspect_accused']+d3+d4+d5+['correct_suspect_accused', 'evidence_round']
temp1 = temp1[cols]
temp1.to_csv(oloc+'Task3_step2.csv', index=False)