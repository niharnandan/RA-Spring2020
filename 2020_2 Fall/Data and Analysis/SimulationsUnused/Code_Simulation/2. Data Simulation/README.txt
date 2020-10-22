
files included:


Python codes:

  Major pieces:
  - value function.py: it records a 3*1001 matrix which is the value of stopping,
    investigating 1, investigating 2 for each p_grid.
  - data simulation.py: it simulates 25*40 sequences of decision making with given 
    lambda, and value functions. It will be used to calculate one single MLE.
  - data simulation distribution.py: it simulates 100 samples of 25*4 sequences of 
    decision making. It will be used to calculate distribution of MLE.

  Minor pieces:
  - EV-lambda plot.py: it plots expected value (approximated by empirical 
    distribution) over lambda grid


csv files:

- Bayes Results.csv: this is the experimental data file
- value functions.csv: this is the simulated results from value function.py
- simulation results.csv: this is the 25*40 simulated results from data simulation.py
- simulation results 2.csv: this is the 100*25*4 simulated results from data 
  simulation distribution.py

* For details of the Python code explanation and comments, refer to the specific 
  ‘.py’ file