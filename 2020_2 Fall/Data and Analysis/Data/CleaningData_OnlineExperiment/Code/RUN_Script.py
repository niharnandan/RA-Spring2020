## IMPORT PACKAGES
import os
import shutil

print('------------')
print('Currently running Step 1 Human Trials')
exec(open('./Step1_HumanTrials.py').read())

print('------------')
print('Currently running Step 2 Human Trials')
exec(open('./Step2_HumanTrials.py').read())

print('------------')
print('Currently running Step 3 Human Trials')
exec(open('./Step3_HumanTrials.py').read())

print('------------')
print('Currently running Step 4 Human Trials')
exec(open('./Step4_HumanTrials.py').read())

print('------------')
print('Generate Companion file')
exec(open('./Generate_Companion_HumanTrials.py').read())
print('Generate Payoff file')
exec(open('./Generate_Payoffs_HumanTrials.py').read())

print('Data cleaning completed')

