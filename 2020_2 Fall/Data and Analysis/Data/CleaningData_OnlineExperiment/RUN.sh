#!/bin/bash

# My first script
mytitle="Run Jupyter Notebooks"
echo -e '\033k'$mytitle'\033\\'


ECHO ============================
ECHO Running Companion File
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Companion.ipynb
ECHO ============================
ECHO Calculating Payoff
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Payoff.ipynb

read -n 1 -s -r -p "Press any key to continue"