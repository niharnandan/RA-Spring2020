# import packages
import csv
import math
import numpy as np
import scipy.optimize
    




################################ Explanation ################################
# This code calculate one single MLE of alpha1, alpha2, lambda(k), stop_cost for 
# simulated dataset. It has the the structure:
# 1) define function for randomness in decision making
# 2) define function for action table for given cost, alpha1, alpha2, lambda(k), stop_cost,
#    encoding randomness (entries are probabilities)
# 3) define function for log-likelihood for observing the simulated data, given the four parameters
# 4) calculate the MLE for 4 parameters/ 3 parameters, with one parameter fixed. The 2-stage brute
#    force is the one work best now, which is done by grid search first on a sparser grid, and
#    then search on a denser grid near the maximum obtained in the first step search.

# Note 1: We need 'simulation results.csv' to run the code.
# Note 2: If estimate MLE for 3 parameters only, keep the remaining one consistant
# with the simulation by changing parameter in the objective function (last part)





###################### function for randomness in decision making ######################

def randomness(k,v_stop,v_red,v_blue):
    try:
        p_stop = 1/(1+math.exp(k*(v_red-v_stop))+math.exp(k*(v_blue-v_stop)))
    except OverflowError: # have a large term in denominator
        p_stop = 0
    try:
        p_red = 1/(1+math.exp(k*(v_stop-v_red))+math.exp(k*(v_blue-v_red)))
    except OverflowError: # have a large term in denominator
        p_red = 0    
    try:
        p_blue = 1/(1+math.exp(k*(v_stop-v_blue))+math.exp(k*(v_red-v_blue)))
    except OverflowError: # have a large term in denominator
        p_blue = 0
    return (p_stop,p_red,p_blue)

        


################### function for action table encoding randomness ###################

def action_table(cost,alpha1,alpha2,k,stop_cost):

    
    ######### set parameters #########
    
    accuracy1 = 0.25
    accuracy2 = 0.25
    reward = 1000
    number = 1001
    p_grid = np.linspace(0,1,number,endpoint=True)

    
    ######### calculate transition matrices #########
    
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))

    # if investigate state 1
    for i in range(number):
        
        p = p_grid[i] # probability 1 is guilty
        prob_reveal = p*accuracy1 # probability of revealing 1 guilty
        # posterior prob of 1 being guilty conditional on no signal found after investigating 1 once
        posterior = p*(1-accuracy1)/(1 - prob_reveal) 
        
        if p < 0.5: # update in the more likely direction
            posterior = alpha1*posterior + (1-alpha1)*p
        else: # update in the less likely direction
            posterior = alpha2*posterior + (1-alpha2)*p   
            
        no_signal = np.argmax(-(abs(p_grid - posterior))) # find the position in p_grid most close to posterior
        t1[i,number-1] = prob_reveal # probability of reveal
        t1[i,no_signal] = 1 - prob_reveal # probability of not revealing
        if no_signal == (number-1):
            t1[i, no_signal] = 1


    # if investigate state 2
    for i in range(number):
        p = p_grid[i] # probability 1 is guilty
        prob_reveal = (1-p)*accuracy2 # probability of revealing 2 guilty
        # posterior prob of 1 being guilty conditional on no signal found after investigating 2 once
        posterior = p/(1 - prob_reveal)
        
        if p >= 0.5: # update in the more likely direction
            posterior = alpha1*posterior + (1-alpha1)*p
        else: # update in the less likely direction
            posterior = alpha2*posterior + (1-alpha2)*p
        
        no_signal = np.argmax(-(abs(p_grid - posterior)))
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal
        if no_signal == (number-1):
            t2[i,no_signal] = 1


    ######### calculate value functions (without randomness) #########
    
    # value function for stop
    V_stop = reward * np.maximum(p_grid, 1-p_grid) # value of stop (accuse the more likely one)
    V_stop[1:(number-1)] = V_stop[1:(number-1)] - stop_cost # if uncertain, minus stop cost

    # DP for convergence
    value = np.zeros(number) # initial v0
    error = 0.0005 # maximum error allowed
    limit = 100000000 # maximum iteration time
    diff = 1 # difference between Vt and Vt-1
    count = 1 # keep track of number of iteration

    while diff > error: # iterate until reach the error level allowed
        V_1 = np.matmul(value,np.transpose(t1)) - cost # value of investigating 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost # value of investigating 2
        V = np.maximum.reduce([V_stop,V_1,V_2]) # optimal to do is to choose the max value of the three
        diff = max(abs(V- value)) # difference between Vt and Vt-1
        count += 1 # keep track of number of iteration
        if count > limit: # break out of loop if reached the maximum iteration time
            break
        else:
            value = V # update Vt
     
    # action table (entries are value of choosing the strategy for given prior)
    actiontable = np.zeros((3,number)) # initiate a 3*1001 action table
    actiontable[0,:] = V_stop # store the value of stop in first line
    actiontable[1,:] = V_1 # store value of investigating 1 in second line
    actiontable[2,:] = V_2 # store value of investigating 2 in third line
    
    
    ######### encode randomness in action table #########
    
    # action table (entries are probabilities of choosing each strategy)
    for i in range(number):
        v = actiontable[:,i] # choose ith column
        v_stop = v[0] # value of stop for this specific p
        v_1 = v[1] # value of investigate 1 for this specific p
        v_2 = v[2] # value of investigate 2 for this specific p
        actiontable[:,i] = randomness(k,v_stop,v_1,v_2) # encode randomness, store back to action table

    return actiontable




################### function for calculating log-likelihood ###################

def log_likelihood(alpha1,alpha2,k,stop_cost):
    
    
    ######### set parameters #########
    
    accuracy1 = 0.25 # probability of finding evidence investigating 1
    accuracy2 = 0.25 # probability of finding evidence investigating 2
    number = 1001 # number of grids
    p_grid = np.linspace(0,1,number,endpoint=True) # prob grids
    ll = 0 # initiate log likelihood to be 0
    
    
    ######### action table for different cost level #########
    
    # for all the experiments we have, there are in total 5 cost levels, we find the actiontables
    # first, and store them so that can be used later without calculating multiple times
    actiontable1 = action_table(5,alpha1,alpha2,k,stop_cost) # action table with cost = 5
    actiontable2 = action_table(10,alpha1,alpha2,k,stop_cost) # action table with cost = 10
    actiontable3 = action_table(20,alpha1,alpha2,k,stop_cost) # action table with cost = 20
    actiontable4 = action_table(40,alpha1,alpha2,k,stop_cost) # action table with cost = 40
    actiontable5 = action_table(80,alpha1,alpha2,k,stop_cost) # action table with cost = 80   


    ######### calculte log-likelihood of the simulated results #########
    
    # open the simulation file
    with open('simulation results.csv','r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        next(filereader) # skip the first line
        for file_row in filereader: # each row is one simulation (one experiment)
            cost = float(file_row[2]) # identify the cost for this simulation (experiment)
            prior = float(file_row[3]) # identify the prior for this simulation (experiment)
            action = file_row[7:] # identify the sequence of choices for this simulation (experiment)
            
            # choose actiontable 1 to 5 according to cost level identified
            if cost == 5:
                actiontable = actiontable1
            elif cost == 10:
                actiontable = actiontable2
            elif cost == 20:
                actiontable = actiontable3
            elif cost == 40:
                actiontable = actiontable4
            else:
                actiontable = actiontable5

            # calculate log-likelihood
            length = len(action)-1 # length of the sequence of choice of one simulation
            for i in range(length): # look at each choice in the sequence
                choice = action.pop(0) # current choice
                if (choice == 'accuse_red') or (choice == 'accuse_blue'):
                    row = 0 # if stop, look at 1st row of actiontable
                elif choice == 'investigate_red':
                    row = 1 # if investigate 1, look at 2nd row of actiontable
                elif choice == 'investigate_blue':
                    row = 2 # if investigate 2,look at 3rd row of actiontable
                elif choice == 'evidence_shown': # if there is evidence shown
                    break # break from for loop as in this case log(likelihood) = log(1) = 0
                column = np.argmax(-(abs(p_grid - prior))) # column to look at: closest in grid to prior
                likelihood = actiontable[row,column] # it is the prob of choosing the action given prior
                try:
                    ll += math.log10(likelihood) # compute lod and add to ll (sum of all likelihood of choice)
                except ValueError:
                    ll -= math.inf # if likelihood is nearly zero, add negative infinity
        
                # update prior after investigating
                if row == 1: # investigate 1
                    posterior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                if row == 2: # investigate 2
                    posterior = prior/(1 - (1-prior)*accuracy2)
                if length > 1: # update with alpha1 and alpha2
                    if (prior >= 0.5 and posterior > prior) or (prior < 0.5 and posterior < prior): # more likely
                        prior = alpha1*posterior + (1-alpha1)*prior
                    else: # less likely
                        prior = alpha2*posterior + (1-alpha2)*prior
                    prior = min(max(prior,0),1) # keep in range of (0,1)
    
    return ll




################### calcuate MLE for simulated results ###################

# calculate MLE for 4 parameters using 2-stage brute-force

likelihood = lambda x: -log_likelihood(x[0],x[1],x[2],x[3])    
MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.5),slice(0,2,0.5),slice(0,0.1,0.025),slice(-100,100,10)),finish=None)
x11 = max(MLE_brute[0]-0.5,0)
x12 = min(MLE_brute[0]+0.5,2)
x21 = max(MLE_brute[1]-0.5,0)
x22 = min(MLE_brute[1]+0.5,2)
x31 = max(MLE_brute[2]-0.025,0)
x32 = min(MLE_brute[2]+0.025,0.1)
x41 = max(MLE_brute[3]-10,-100)
x42 = min(MLE_brute[3]+10,100)
MLE_brute = scipy.optimize.brute(likelihood,(slice(x11,x12,0.25),slice(x21,x22,0.25),slice(x31,x32,0.01),slice(x41,x42,1)))


# calculate MLE for 3 parameters using gradient/brute force/2-stage brute force
# change 'method' to calculate by the selected method
# [Note: the below code calculate MLE of alpha1, alpha2, lambda, with stop_cost = 0.
# Simulate corresponding datasets with zero stop cost.]

method = 'none' # method of calculating MLE

if method == 'gradient': # use scipy.optimize.minimize
    likelihood = lambda x: -log_likelihood(x[0],x[1],x[2],0) # objective function to minimize
    # [Note: here stop_cost = 0, change the number if simulate with a different stop_cost]
    optimized = scipy.optimize.minimize(likelihood,x0=np.array([1.3,0.6,0.02]),bounds=((0,2),(0,2),(0,0.1)))
    print(optimized) 
    if optimized.success: # if successfully converges, store MLE
        MLE_gradient = optimized.x
    else:
        raise ValueError(optimized.message)
        
elif method == 'brute force':
    likelihood = lambda x: -log_likelihood(x[0],x[1],x[2],0)
    MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.1),slice(0,2,0.1),slice(0,0.1,0.01)))
    print(MLE_brute) 
    
elif method == '2-stage brute force':
    likelihood = lambda x: -log_likelihood(x[0],x[1],x[2],0)    
    MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.5),slice(0,2,0.5),slice(0,0.1,0.025)),finish=None)
    x11 = max(MLE_brute[0]-0.5,0)
    x12 = min(MLE_brute[0]+0.5,2)
    x21 = max(MLE_brute[1]-0.5,0)
    x22 = min(MLE_brute[1]+0.5,2)
    x31 = max(MLE_brute[2]-0.025,0)
    x32 = min(MLE_brute[2]+0.025,0.1)
    MLE_brute = scipy.optimize.brute(likelihood,(slice(x11,x12,0.25),slice(x21,x22,0.25),slice(x31,x32,0.01)))

