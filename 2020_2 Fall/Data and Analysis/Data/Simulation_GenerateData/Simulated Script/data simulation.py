# import packages
import math
import random
import numpy as np
import csv

print('Currently running DATA SIMULATION')

############################### Explanation ###############################
# This is a code for simulating fictional sequences of decisions made by agents.
# It has the following parts:
# 1) helper function for randomness in decision making: use softmax function to calculate
#    the probability of choosing each option given lambda and repective values.
# 2) parameters setting
# 3) simulation for each (cost, prior) combination
#    The simulation goes as follows:
#      1. for each cost level, find value functions (V_stop, V_1, V_2)
#      2. then, for each prior level, generate simulations, each simulation is 
#         a sequence of investigation/accusation generated as follows.
#      3. generate (prob of stopping, prob of invesitgating red, prob of invesitgating blue)
#         according to randmness(k,v_stop,v_red,v_blue) function
#         - if random_action < Pr(stop):
#           stop, accuse, start next simulation
#         - if random_action <= 1 - Pr(blue):
#           investigate red
#             - if evidence shown:
#               stop, accuse red, start new simulation
#             - if no evidence shown:
#               update prior, iterate 
#         - if random_action > 1 - Pr(blue):
#           investigate blue
#             - if evidence shown:
#               stop, accuse blue, start new simulation
#             - if no evidence shown:
#               update prior, iterate 
#         - if run out of 60 opportunities for investigation, accuse


# IMPORTANT NOTE: four parameters that would affect the simulation results: 
# lambda(k), alpha1, alpha2, stop_cost.
# If you want to change lambda(k), change in this code. To change the other three, change 
# 'value functions.py' to generate a different 'value functions.csv' first.

# NOTE 2: what we need to run the code: 'value functions.csv', 'Bayes Results.csv' (experiment data)

# NOTE 3: write into csv file called 'simulation results.csv'



############################### Set parameters ###############################

## Parameter of stochasticity in the action
#k = 0.04               # parameter (lambda) in randomness
#k = 2.0                # parameter (lambda) in randomness
k_action = 20.0          # parameter (lambda) in randomness (action choice)
k_accuse = 20.0          # parameter (lambda) in randomness accusation
k_investigate = 20.0     # parameter (lambda) in randomness investigation

## Maximum number of search
trial = 58              # total number of available trials
#trial = 60             # total number of available trials
count = 0               # keep track of the number of trial (no greater than 60)

## Number of datasets repeated (25 trials in each dataset)
number_datasets = 100

# These parameters are not edited
p_grid = np.linspace(0,1,1001,endpoint=True) # probability grid
cost = [5,10,20,40,80] # cost per investigation
prior = [0.1,0.3,0.5,0.7,0.9] # prior probability of 1 guilty
true_state = [] # guilty state for each cost, prior



############################### Helper function ###############################
# capture the randomness of decision making. prob of choosing stop, 1, 2, given lambda(k), V_stop, V_1, V_2 
# input: lambda(k), V_stop, V_1, V_2
# output: prob of choosing stop, investigate 1, and investigate 2, probability calculated by softmax
def randomness(k_action, k_accuse, k_investigate, v_stop, v_red, v_blue):
    
    v_investigate = np.maximum(v_red, v_blue)
    try:
        p_stop = 1 / (1 + math.exp(k_action*(v_investigate-v_stop)))
    except OverflowError:
        p_stop = 0
    try:
        p_red = 1 / (1 + math.exp(k_investigate*(v_blue-v_red)))
    except OverflowError:
        p_red = 0    
    try:
        p_blue = 1 - p_red
    except OverflowError:
        p_blue = 0
    p_investigate = 1-p_stop
    p_red = p_red *p_investigate
    p_blue= p_blue*p_investigate
    
    return (p_stop,p_red,p_blue)



############################### Read behavioral parameters of the model ###############################

# Read from csv file stored as 'value functions.csv' the following parameters:
# accuracy1 (prob of finding 1 guilty conditional on 1 guilty), accuracy2, alpha_1, alpha_2
## ???? WOULD BE EASIER TO READ DIRECTLY FROM THE INPUT FILE? but it works now...
with open('value functions.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    accuracy1 = float(next(filereader)[1])
    accuracy2 = float(next(filereader)[1])
    alpha_1 = float(next(filereader)[1])
    alpha_2 = float(next(filereader)[1])



############################### Simulation and write into csv file ###############################
# Write simulation results into csv file
    
# Write the first line to be column names
# create a list of column names, same format as the experiment data csv file
column_name = ['trial_no','block_name','setup_cost','red_prior_prob',
               'guilty_suspect_chosen','timing_valid','timing_error']
for i in range(1,63):
    column_name.append('_'.join(['choice',str(i)]))
with open('simulation results.csv','w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(column_name)

    
    
## Simulation of decision sequences    

# iterate through cost levels
for c in cost:
    
    # the following lines read V_stop, V_1, V_2 of the corresponding cost from 'value functions.csv'
    with open('value functions.csv','r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for line, content in enumerate(filereader):
            if content == [''.join(['cost=',str(c)])]:
                line_num = line # identify the line of cost = c
                break
        # retrieve the values from the value functions file
        V_stop = next(filereader)
        V_stop = [float(i) for i in V_stop]         # change string type to float
        V_1 = next(filereader)
        V_1 = [float(i) for i in V_1]
        V_2 = next(filereader)
        V_2 = [float(i) for i in V_2]
        
    # iterate through prior levels
    for p in prior:
        
        p0 = p      # store the value of p into p0, so that we can reset after break from one trial
        
        # for each level of c(cost) and p(prior), we append the simulation result into the 
        # created csv file, which contains N simulations for each (c,p) combination, and 
        # each simulation consists of up to 60 available investigation opportunities
        for i in range(number_datasets): # N simulations
            
            # Generate random guilty suspect
            if random.random()>p0:
                guilty = 'blue'
            else:
                guilty = 'red'
            
            # Initialize the new trial
            investigation = ['','',c,p,guilty,'','']    # for each trial, keep track of the choices made
            count = 0                                   # keep track of the number of investigation (60 maximum)
            
            while (count <= trial):                     # when we have not reached total available investigation number (60)
                count += 1                              # keep track of number of times we have investigated
                p_index = np.argmax(-(abs(p_grid - p))) # find the position of p in p_grid (current belief)
                
                # find the value of stop, 1, 2 for that p, and the prob of stop, 1, 2 based on randomness
                choice = randomness(k_action,k_accuse,k_investigate,V_stop[p_index],V_1[p_index],V_2[p_index])
                random_action = random.random() # generate a random number
                
                # case 1: accuse
                if random_action <= choice[0]:
                    if p>=0.5:                                      # red is more likely to be guilty
                        investigation.append('accuse_red')
                        investigation.append('advance_to_next_trial')
                    else:                                           # blue is more likely to be guilty
                        investigation.append('accuse_blue')
                        investigation.append('advance_to_next_trial')
                    p = p0                                          # reset the probability
                    break
                
                # case 2: investigate red
                elif random_action <= 1-choice[2]:
                    investigation.append('investigate_red')
                    
                    # red is guilty and evidence is shown, then accuse red
                    if random.random()<=accuracy1 and guilty == 'red':
                        investigation.append('evidence_shown')
                        investigation.append('accuse_red')
                        investigation.append('advance_to_next_trial')
                        p = p0                                          # reset the probability
                        break
                    
                    else:                                               # no evidence
                        posterior = p*(1-accuracy1)/(1 - p*accuracy1)
                        if p <= 0.5:
                            p = alpha_1*posterior + (1-alpha_1)*p
                        else:
                            p = alpha_2*posterior + (1-alpha_2)*p
                        p = min(max(p,0),1)                             # updated p in (0,1)
                
                # case 3: investigate blue
                else:
                    investigation.append('investigate_blue')
                    
                    # blue is guilty and evidence is shown, then accuse blue
                    if random.random()<=accuracy2 and guilty == 'blue':
                        investigation.append('evidence_shown')
                        investigation.append('accuse_blue')
                        investigation.append('advance_to_next_trial')
                        p = p0                                          # reset the probability
                        break
                    
                    else:                                               # no evidence
                        posterior = p/(1 - (1-p)*accuracy2)
                        if p >= 0.5:
                            p = alpha_1*posterior + (1-alpha_1)*p
                        else:
                            p = alpha_2*posterior + (1-alpha_2)*p
                        p = min(max(p,0),1)                             # updated p in (0,1)
            
            
            # if we run out of investigation opportunities, but don't make a decision yet                
            if investigation[-1] != 'advance_to_next_trial':
                if p>=0.5:                                      # red likely to be guilty
                    investigation.append('accuse_red')
                else:                                           # blue likely to be guilty
                    investigation.append('accuse_blue')
                investigation.append('advance_to_next_trial')
                p = p0                                          # reset the probability
            
            
            # write the sequence of investigation choice of one trial into the csv
            with open('simulation results.csv','a',newline='') as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow(investigation)
        
        
csvfile.close()

