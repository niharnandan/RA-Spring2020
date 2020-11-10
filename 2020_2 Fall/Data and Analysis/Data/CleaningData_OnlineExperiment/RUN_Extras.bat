@ECHO OFF
TITLE Run Jupyter Notebooks

ECHO ============================
ECHO Running Companion File
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Companion.ipynb
ECHO ============================
ECHO Calculating Payoff
ECHO ============================
jupyter nbconvert --to notebook --execute Code/Payoff.ipynb
PAUSE