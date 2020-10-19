import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
sns.set_style("darkgrid")
warnings.filterwarnings('ignore')
oloc = open("../Output_Location (Simulated).txt", "r").read()

f = open("values.txt").read().split('\n')
no_files = int(f[8])

for name in range(65,65+no_files):
    temp1 = pd.read_csv(oloc+'Step2_'+chr(name)+'.csv')
    for key,value in temp1.iterrows():
        if value[1] == 0:
            temp = temp1.iloc[key, 9:69].to_list()
            temp1.iloc[key, 9:69] = [int(x) ^ 1 if x == 1.0 or x == 0.0 else np.nan for x in temp]
    temp1.to_csv(oloc+'Step3_'+chr(name)+'.csv', index=False)