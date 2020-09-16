# import packages
import csv
import math
import numpy as np
import scipy.optimize
from scipy.integrate import quad





################################ Explanation ################################
# This is a piece of toy code for calculating MLE of mean and variance for 
# normal distribution N(0,1). We first discretize the normal distribution by
# trunctate it into pieces and calculate the likelihood of the the simulated
# results fall into the specific intervals.
# - We first define three functions:
#   1) pdf of normal distribution N(mu, sigma**2)
#   2) discretized probability grid for normal distribution: it calculates the
#      probability of falling into the intervals
#   3) log-likelihood function, which gives the log-likelihood of observing the
#      the sequence of simulated data given mean mu and variance sigma square.
# - We then calculate MLE by optimize the log-likelihood





###################### pdf of normal distribution N(mu, sigma**2) ######################

def integrand(x,mu,sigma):
    x = 1/math.sqrt(2*math.pi*sigma**2)*math.exp(-(x-mu)**2/(2*sigma**2)) # normal pdf formula
    return x




################## discretized probability grid for normal distribution ##################

# trunctate [-100,100] into 2000 pieces and calculate the probability of falling into each
# interval for normal distribution

def prob_table(mu,sigma):
    table = np.zeros(2000) # initiate a table of size 2000
    for i in range(2000):
        x_low = -100+i*0.1 # starting point of interval
        x_high = -100 + i*0.1 + 0.1 # ending point of interval
        fcn = lambda x : integrand(x,mu,sigma) # function for pdf of of normal
        # integrate from x_low to x_high to get probability of falling in the interval
        ans, err = quad(fcn,x_low,x_high)
        table[i] = ans # store in table
    return table




######################## log-likelihood function ########################

# Given the simulated data, what is the likelihood of mu, sigma being the true
# mean and s.d. This is the objective function to be maximized.

def log_likelihood(mu, sigma):
    ll = 0 # initiate log-likelihood to be 0
    x_grid = np.linspace(-100,100,2000,endpoint=True) # trunctate [-100,100] into 2000 pieces
    # probability table of falling into each interval given mean and variance
    table = prob_table(mu, sigma)
    
    # open the csv file simulated by N(0,1)
    with open('normal simulation.csv','r') as csvfile:
      filereader = csv.reader(csvfile, delimiter=',')  
      for row in filereader:
          # find out the index of closest number in x_grid to the simulated number
          position = np.argmax(-(abs(x_grid - float(row[0]))))
          # find out the probability of getting the simulated number given the mean and variance
          # the if-else is just to find out the right index
          if x_grid[position] > float(row[0]):
              likelihood = table[position-1]
          else:    
              likelihood = table[position]
          try:
              ll += math.log10(likelihood) # add log-likelihood to ll
          except ValueError:
              ll -= math.inf
    return ll
      



######################## MLE by optimizing likelihood ########################

likelihood = lambda x: -log_likelihood(x[0],x[1]) 
optimized = scipy.optimize.minimize(likelihood,x0=np.array([100,100]),method = 'Nelder-Mead')
print(optimized) 
if optimized.success:
    MLE = optimized.x
else:
    raise ValueError(optimized.message)


