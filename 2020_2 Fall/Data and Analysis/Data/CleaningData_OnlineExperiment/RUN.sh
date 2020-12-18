#!/bin/bash

# Run Python Script
mytitle="Run Jupyter Notebooks"
echo -e '\033k'$mytitle'\033\\'


ECHO ============================
ECHO Running Scripts
ECHO ============================
python Code/Step1_HumanTrials.py
ECHO ============================
python Code/Step2_HumanTrials.py
ECHO ============================
python Code/Step3_HumanTrials.py
ECHO ============================
python Code/Step4_HumanTrials.py
ECHO ============================
python Code/Generate_Companion_HumanTrials.py
ECHO ============================
python Code/Generate_Payoffs_HumanTrials.py

read -n 1 -s -r -p "Press any key to continue"