#!/bin/bash

# My first script
mytitle="Run Jupyter Notebooks"
echo -e '\033k'$mytitle'\033\\'

ECHO ============================
ECHO Running Step 1
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Step1.ipynb
ECHO ============================
ECHO Running Step 2
ECHO ============================
jupyter nbconvert --to notebook --ExecutePreprocessor.timeout=120 --execute Code/Step2.ipynb
ECHO ============================
ECHO Running Step 3
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Step3.ipynb
ECHO ============================
ECHO Running Step 4
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Step4.ipynb
ECHO ============================
ECHO Running Companion File
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Companion.ipynb
ECHO ============================
ECHO Calculating Payoff
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Payoff.ipynb

read -n 1 -s -r -p "Press any key to continue"