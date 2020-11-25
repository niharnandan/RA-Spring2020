## IMPORT PACKAGES
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import warnings
warnings.filterwarnings('ignore')


## PATH
mypath= '../RawData_OnlineExperiment/'
files = [f for f in listdir(mypath)]
oloc = open("../Output_Location.txt", "r").read()
files.remove('.DS_Store')


## CREATE FILE
temp = [0]*len(files)
sum = 0
p_count = 0
for i in range(len(files)):
    p_count += 1
    t1 = [p_count]
    t1.append(files[i].strip('Detective_CSV_OnlineTest/'))
    t = pd.read_csv(mypath+files[i])
    t1.append(t['total_bonus_paid_cents'].to_list()[-1])
    time1 = []
    time2 = []
    time3 = []
    for key,value in t.iterrows():
        get_time = [x for x in value[71:133] if x > 0]
        if not get_time: continue
        if 'part1' in value[1]: time1.append(get_time[-1])
        elif 'part2' in value[1]: time2.append(get_time[-1])
        else: time3.append(get_time[-1])
    t1.append(np.mean(time1))
    t1.append(np.mean(time2))
    t1.append(np.mean(time3))
    temp[i] = t1


## SAVE FILE
temp2 = pd.DataFrame(temp, columns = ['participant_ID','csv', 'total_bonus_paid_cents', 'part1_average'
            ,'part2_average', 'part3_average'])
temp2.to_csv(oloc+'companion.csv')

