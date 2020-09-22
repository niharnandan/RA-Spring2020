@ECHO OFF
TITLE Run Jupyter Notebooks
ECHO ============================
ECHO Running Step 1
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Step1.ipynb
ECHO ============================
ECHO Running Step 2
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Step2.ipynb
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
PAUSE