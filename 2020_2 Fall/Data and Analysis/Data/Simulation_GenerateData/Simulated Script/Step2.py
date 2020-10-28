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
mypath= '../../../Data/RawData_OnlineExperiment/' #Path of data folder that contains simulated data
oloc = open("../Output_Location (Simulated).txt", "r").read() #Path of output folder
f = open("values.txt").read().split('\n') #To check for the number of files
no_files = int(f[8])


## REPEAT FOR EVERY FILE IN THE FOLDER
for name in range(65,65+no_files):
    
    # Read file
    print('Running Step 2 for File', chr(name))
    step2_df = pd.read_csv('../Simulated_Data/simulation results '+chr(name)+'.csv', error_bad_lines=False)
    
    # Replace values (convert strings to numerical variables)
    step2_df = step2_df.replace('red', 0)
    step2_df = step2_df.replace('blue', 1)
    step2_df = step2_df.rename(columns={"setup_cost": "rounds",})
    step2_df = step2_df.rename(columns={"guilty_suspect_chosen": "true_guilty_suspect",})
    for i in range(1,63,1):
        step2_df.insert(len(step2_df.columns), 'outcome_'+str(i), np.nan)
    step2_df['evidence_round'] = 0
    step2_df['correct_suspect_accused'] = 0
    step2_df['participant_ID'] = 0
    step2_df['treatment'] = 0
    step2_df['part'] = 2
    step2_df['suspect_accused'] = 0
    for i in range(1,63): 
        step2_df['timing_choice_'+str(i)] = 0

    # Ennumeration values that is represented by the array index. Example: investigate_red will be stored as 0
    values = ['investigate_red','investigate_blue','accuse_red','accuse_blue','advance_to_next_trial', 'evidence_shown']
    for i in values: step2_df = step2_df.replace(i, values.index(i))
	
	#Iterating over rows in the dataframe. 
    for key,value in step2_df.iterrows():
        temp = step2_df.iloc[key, 7:69].to_list() #Storing the choice columns into array 
        outcome = [x for x in temp if x != np.nan and (x == 5) or (x == 1) or (x == 0)]
        outcome = [1 if i == 5 else 0 for i in outcome]
        for i in range(1,len(outcome)+1):
            step2_df['outcome_'+str(i)][key] = outcome[i-1]
            
    # Storing the values for the suspect accused and whether the right suspect is accused
        if (2 in temp and value[4] == 0) or (3 in temp and value[4] == 1): 
            step2_df['correct_suspect_accused'][key] = 1 
        if 2 in temp: step2_df['suspect_accused'][key] = 0
        elif 3 in temp: step2_df['suspect_accused'][key] = 1

    # Storing the round in which evidence is found. 
        if 5 in temp:
            step2_df['evidence_round'][key] = temp.index(5)+1
            temp.remove(5)
            temp.append(np.nan)
        else: step2_df['evidence_round'][key] = 0 # In case there is no evidence found, evidence round is 0
        temp = [x if x == 1 or x == 0 else np.nan for x in temp] #Store only investigate action
        step2_df.iloc[key, 7:69] = temp #Replace the newly trimmed array into choice columns. 
		
	# Removing unneccesary columns and ordering the required columns for output
    d3 = ['choice_'+str(i) for i in range(1,61)]
    d4 = ['outcome_'+str(i) for i in range(1,61)]
    d5 = ['timing_choice_'+str(i) for i in range(1,63)]
    step2_df = step2_df.rename(columns={"rounds": "setup_cost_red",})
    step2_df["setup_cost_blue"] =  step2_df["setup_cost_red"]
    cols = ['participant_ID', 'treatment', 'part', 'trial_no', 
             'setup_cost_red', 'setup_cost_blue', 'red_prior_prob',
            'true_guilty_suspect', 'suspect_accused']+d3+d4+d5+['correct_suspect_accused', 'evidence_round']
    step2_df = step2_df[cols]

    # Save output file
    step2_df.to_csv(oloc+'Step2_'+chr(name)+'.csv', index=False)
    
    