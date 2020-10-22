import math
import numpy as np
import csv
import scipy.optimize





################################ Explanation ################################
# This is a code for calculating MLE of the expreimental data. It has a similar structure
# to 'MLE.py' but with minor difference because of minor difference in the format.
# It calculates MLEs based on three hypotheses:
# 1) stop cost = 0 (model = 'alpha1_alpha2_lambda')
# 2) alpha1 = alpha2 (model = 'alpha1=alpha2')
# 3) no restriction, estimate 4 parameters (model = 'alpha1_alpha2_lambda_stopcost')
# It has a similar structure as the 'MLE.py' code:
# 1) function for randomness in decision making
# 2) function for action table encoding randomness (entries are probabilities)
# 3) function for log-likelihood for observing the simulated data, given the four parameters
# 4) calculate the MLE under three hypotheses

# Note 1: We need 'Bayes Results.csv' to run the code, which is the experimental data
# Note 2: Revise (model = 'none') to approprimate hypothesis chosen in the code 
# Note 3: the result is not very good





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
        
        p = p_grid[i] # prob 1 is guilty
        prob_reveal = p*accuracy1 # prob of revealing 1 guilty
        posterior = p*(1-accuracy1)/(1 - prob_reveal) 
        # posterior prob of 1 being guilty conditional on no signal found after investigating 1 once
        
        if p < 0.5: # update in the more likely direction
            posterior = alpha1*posterior + (1-alpha1)*p
        else: # update in the less likely direction
            posterior = alpha2*posterior + (1-alpha2)*p   
            
        no_signal = np.argmax(-(abs(p_grid - posterior))) # find the position in p_grid most close to posterior
        t1[i,number-1] = prob_reveal # (i,1000) entry of transition matrix t1 is prob of reveal
        t1[i,no_signal] = 1 - prob_reveal # (i,no_signal) entry of transition matrix t1 is prob of non_reveal
        if no_signal == (number-1): # if posterior very close to 1
            t1[i, no_signal] = 1 # (i,1000) entry is 1 = prob reveal + prob non_reveal


    # if investigate state 2
    for i in range(number):
        p = p_grid[i] # prob 1 is guilty
        prob_reveal = (1-p)*accuracy2 # prob of revealing 2 guilty
        posterior = p/(1 - prob_reveal)
        # posterior prob of 1 being guilty conditional on no signal found after investigating 2 once
        
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

def log_likelihood(file,alpha1,alpha2,k,stop_cost):
        
    
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
    
    for file_row in file: # each row is one simulation (one experiment)
        cost = float(file_row[2]) # identify the cost for this simulation (experiment)
        prior = float(file_row[3]) # identify the prior for this simulation (experiment)
        action = file_row[7:69] # identify the sequence of choices for this simulation (experiment)
        evidence_shown = file_row[192] # if final evidence is shown
        if evidence_shown == '0': # no final evidence
            evidence_shown = False
        else: # there is final evidence
            evidence_shown = True
            
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
        for choice in action: # look at each choice in the sequence
            if (choice == 'accuse_red') or (choice == 'accuse_blue'):
                if evidence_shown == True: # if there is evidence shown
                    break # break from for loop as in this case log(likelihood) = log(1) = 0
                else: # no evidence shown
                    row = 0 # if stop, look at 1st row of actiontable
            elif choice == 'investigate_red':
                row = 1 # if investigate 1, look at 2nd row of actiontable
            elif choice == 'investigate_blue':
                row = 2 # if investigate 2,look at 3rd row of actiontable
            elif choice == 'advance_to_next_trial': # done with the trial
                break
            column = np.argmax(-(abs(p_grid - prior))) # column to look at: closest in grid to prior
            likelihood = actiontable[row,column] # it is the prob of choosing the action given prior
            try:
                ll += math.log10(likelihood) # compute lod and add to ll (sum of all likelihood of choice)
            except ValueError:
                ll -= math.inf # if likelihood is nearly zero, add negative infinity
        
            # update prior after investigating
            if row == 1: # investigate 1
                posterior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                if prior < 0.5: # more likely
                    prior = alpha1*posterior + (1-alpha1)*prior
                else: # less likely
                    prior = alpha2*posterior + (1-alpha2)*prior
                prior = min(max(prior,0),1) # keep in range of (0,1)
            if row == 2: # investigate 2
                posterior = prior/(1 - (1-prior)*accuracy2)
                if prior >= 0.5: # more likely
                    prior = alpha1*posterior + (1-alpha1)*prior
                else: # less likely
                    prior = alpha2*posterior + (1-alpha2)*prior
                prior = min(max(prior,0),1) # keep in range of (0,1)
    
    return ll




################### open csv, prepare 'file' input for log_likelihood function ###################

with open('Bayes Results.csv','r') as f:
    file = [row for row in csv.reader(f.read().splitlines())]
file = file[26:51] # select the second half of data (second experiment)




################### calculate MLE with 3 hypotheses ###################

# specify the parameters we want to fit:
# 'alpha1_alpha2_lambda','alpha1=alpha2','alpha1_alpha2_lambda_stopcost'
model = 'none'



##### fit 3 parameters: alpha1, alpha2, lambda, with no cost #####
if model == 'alpha1_alpha2_lambda':
    likelihood = lambda x: -log_likelihood(file,x[0],x[1],x[2],0) # objective function
        
        ### brute force: first search on larger grids, and then search on subfields ###
        ### works if the likelihood function is well-behaved ###
        
    MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.5),slice(0,2,0.5),slice(0,0.1,0.025)),finish=None)
    x11 = max(MLE_brute[0]-0.5,0)
    x12 = min(MLE_brute[0]+0.5,2)
    x21 = max(MLE_brute[1]-0.5,0)
    x22 = min(MLE_brute[1]+0.5,2)
    x31 = max(MLE_brute[2]-0.025,0)
    x32 = min(MLE_brute[2]+0.025,0.1)
    MLE_brute = scipy.optimize.brute(likelihood,(slice(x11,x12,0.25),slice(x21,x22,0.25),slice(x31,x32,0.01)))



##### fit three parameters: alpha, lambda, stop_cost, with alpha1 = alpha2 #####   
elif model == 'alpha1=alpha2':
    likelihood = lambda x: -log_likelihood(file,x[0],x[0],x[1],x[2]) # objective function  
        
        ### brute force: first search on larger grids, and then search on subfields ###
        ### works if the likelihood function is well-behaved ###
        
    MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.5),slice(0,0.1,0.025),slice(-100,100,25)),finish=None)
    x11 = max(MLE_brute[0]-0.5,0)
    x12 = min(MLE_brute[0]+0.5,2)
    x21 = max(MLE_brute[1]-0.025,0)
    x22 = min(MLE_brute[1]+0.025,0.1)
    x31 = max(MLE_brute[2]-25,-100)
    x32 = min(MLE_brute[2]+25,100)
    MLE_brute = scipy.optimize.brute(likelihood,(slice(x11,x12,0.25),slice(x21,x22,0.01),slice(x31,x32,10)))



##### fit four parameters: alpha1, alpha2, lambda, stop_cost #####
elif model == 'alpha1_alpha2_lambda_stopcost':
    likelihood = lambda x: -log_likelihood(file,x[0],x[1],x[2],x[3]) # objective function  
        
        ### brute force: first search on larger grids, and then search on subfields ###
        ### works if the likelihood function is well-behaved ###
        
    MLE_brute = scipy.optimize.brute(likelihood,(slice(0,2,0.5),slice(0,2,0.5),slice(0,0.1,0.025),slice(-100,100,25)),finish=None)
    x11 = max(MLE_brute[0]-0.5,0)
    x12 = min(MLE_brute[0]+0.5,2)
    x21 = max(MLE_brute[1]-0.5,0)
    x22 = min(MLE_brute[1]+0.5,2)
    x31 = max(MLE_brute[2]-0.025,0)
    x32 = min(MLE_brute[2]+0.025,0.1)
    x41 = max(MLE_brute[3]-25,-100)
    x42 = min(MLE_brute[3]+25,100)
    MLE_brute = scipy.optimize.brute(likelihood,(slice(x11,x12,0.25),slice(x21,x22,0.25),slice(x31,x32,0.01),slice(x41,x42,10)))

