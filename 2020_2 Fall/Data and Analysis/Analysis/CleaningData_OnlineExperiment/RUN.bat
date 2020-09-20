@ECHO OFF
TITLE Run Jupyter Notebooks
ECHO ============================
ECHO Running Step 1
ECHO ============================
jupyter nbconvert --to notebook --execute Step1.ipynb
PAUSE