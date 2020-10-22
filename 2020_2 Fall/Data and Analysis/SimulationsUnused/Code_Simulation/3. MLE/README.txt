
files included:


Python codes:

  Major pieces:
  - MLE.py: it calculates one single MLE of the simulated data
  - MLE distribution.py: it calculates 100 MLEs of 100 samples of simulated data and 
    plots the histogram
  - MLE experiment.py: it calculates MLE based on the experimental data (the result
    doesn’t very much make sense)

  Minor pieces:
  - normal MLE.py: it is a toy case of calculate the MLE of mean and variance of 1000 
    data points simulated from N(0,1)
  - 3D Plot.ipynb: it is a 3D plot of log-likelihood with input to be 2 of 4 
    parameters (alpha1, alpha2, lambda, stop_cost). 6 graphs in total. Notice that 
    the plot is negative of log-likelihood


csv files:

- Bayes Results.csv: this is the experimental data file
- simulation results.csv: this is the 25*40 simulated results from data simulation.py
- simulation results 2.csv: this is the 100*25*4 simulated results from data 
  simulation distribution.py
- normal simulation.csv: 1000 simulations from N(0,1)

* For details of the Python code explanation and comments, refer to the specific 
  ‘.py’ file