# import packages
import numpy as np
import csv
    
print('Currently running VALUE FUNCTION')

############################### Explanation ###############################
# This is a code for finding the value functions for stopping, investigating 1, 
# and investigating 2 for each prior grid. 
# The output of the script is the value functions, i.e. the value of EACH action 
# (accuse, investigate 1 or 2, given the current belief that 1 is guilty)

# IMPORTANT NOTE: the value function changes if you change alpha_1, alpha_2, stop_cost.
# If you want to change these three parameters in simulation, change the parameters part
# in this code to get a new value function, or edit in the RUN file that uses this script.



############################### Set parameters ###############################

# open file that contains all the relevant parameters
f = open("values.txt", "r")
content = f.read()
content_list = content.split()

## INPUT PARAMETERS - CAN RUN SIMULATIONS FOR SEVERAL CONDITIONS
alpha_1 = float(content_list[0]) # update in the direction of more likely
alpha_2 = float(content_list[1]) # update in the direction of less likely
stop_cost = float(content_list[5]) # stop cost
# file_name

## PARAMETER - FIXED (do not change across simulations)
# NOT USED - r_lambda_action = 2        # accuracy in the action choice (accuse vs investigate)
# NOT USED - r_lambda_investigate = 2   # accuracy in investigation choices
# NOT USED - r_lambda_accuse = 2        # accuracy in accusation choices
number = int(content_list[7])             # grid size - number in value function
# NOT USED - n_datasets = 100           # number of repetitions for the block of questions

## PARAMETER - PROBLEM (these do not change)
accuracy1 = float(content_list[2]) # prob of reveal for 1
accuracy2 = float(content_list[3]) # prob of reveal for 2
# prior_vector
cost_vector = content_list[4].split(',')
cost_vector = [int(i) for i in cost_vector]# cost levels for investigation
reward = int(content_list[6]) # reward for getting the right state
# max_investigate

## process input information
p_grid = np.linspace(0,1,number,endpoint=True) # p grid



##################### value functions and store into csv #####################

# write the result in a csv file. It includes:
# 1) parameters: accuracy1, accuracy2, alpha1, alpha2
# 2) for each cost level: V_stop, V_1 (investigate 1), V_2 (investigate 2)

# write the parameters used to calculate the value function
with open('value functions.csv','w',newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['accuracy1=',accuracy1])
    filewriter.writerow(['accuracy2=',accuracy2])
    filewriter.writerow(['alpha_1=',alpha_1])
    filewriter.writerow(['alpha_2=',alpha_2])
    filewriter.writerow([])
    filewriter.writerow(['order:','V_stop','V_1','V_2'])
    filewriter.writerow([])


# generate and write the value functions (for each cost level)
for cost in cost_vector:
    # same investigation cost for 1 and 2
    cost1 = cost            # cost investigate 1
    cost2 = cost            # cost investigate 2


    ############################### calculate the transition matrix ###############################
    # the transition matrix (for each investigation action) indicates the likelihood
    # of moving from the current belief (pr(1 is guilty)) to another belief
    
    # write the empty transition matrices
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))


    # if investigate state 1
    for i in range(number):
        
        p = p_grid[i]                   # initial prob 1 is guilty
        prob_reveal = p*accuracy1       # prob of revealing 1 guilty
        posterior = p*(1-accuracy1)/(1 - prob_reveal) 
        # posterior prob of 1 being guilty, conditional on no signal found after investigating 1 once
        
        # alphas are used to update with different coefficients for confirmatory or contradictory evidence
        if (p >= 0.5 and posterior > p) or (p <= 0.5 and posterior < p):    
            posterior = alpha_1*posterior + (1-alpha_1)*p   # update in the more likely direction
        else:
            posterior = alpha_2*posterior + (1-alpha_2)*p   # update in the less likely direction   
        
        # fill the transition matrix
        no_signal = np.argmax(-(abs(p_grid - posterior)))   # find the position in p_grid most close to posterior
        t1[i,number-1] = prob_reveal                        # (i,1000) entry of transition matrix t1 is prob of REVEAL
        t1[i,no_signal] = 1 - prob_reveal                   # (i,no_signal) entry of transition matrix t1 is prob of NON_REVEAL
        if no_signal == (number-1):                         # if posterior is very close to 1
            t1[i, no_signal] = 1                            # (i,1000) entry is 1 = prob reveal + prob non_reveal


    # if investigate state 2
    for i in range(number):
        
        p = p_grid[i]                    # initial prob 1 is guilty
        prob_reveal = (1-p)*accuracy2    # prob of revealing 2 guilty
        posterior = p/(1 - prob_reveal) 
        # posterior = 1-(1-p)*(1-accuracy2)/(1 - prob_reveal) # EQUIVALENT BUT LONGER EQUATION
        # posterior prob of 1 being guilty conditional on no signal found after investigating 2 once
        
        # alphas are used to update with different coefficients for confirmatory or contradictory evidence
        if (p >= 0.5 and posterior > p) or (p <= 0.5 and posterior < p):    
            posterior = alpha_1*posterior + (1-alpha_1)*p   # update in the more likely direction
        else:
            posterior = alpha_2*posterior + (1-alpha_2)*p   # update in the less likely direction
        
        # fill the transition matrix
        no_signal = np.argmax(-(abs(p_grid - posterior)))
        t2[i,0] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal
        if no_signal == (number-1):
            t2[i,no_signal] = 1


    ###################### dynamic programming for convergence of value function ######################
            
    # value function for stop
    V_stop = reward * np.maximum(p_grid, 1-p_grid) # value of stop (accuse the more likely one)
    V_stop[1:(number-1)] = V_stop[1:(number-1)] - stop_cost # if uncertain, minus stop cost


    # dynamic programming for convergence
    # initialize variables
    value = np.zeros(number)    # initial v0
    error = 0.0005              # maximum error allowed
    limit = 100000000           # maximum iteration time
    diff = 1                    # difference between Vt and Vt-1
    count = 1                   # keep track of number of iteration

    # iterate until reach the error level allowed
    while diff > error: 
        V_1 = np.matmul(value,np.transpose(t1)) - cost1     # value of investigating 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2     # value of investigating 2
        V = np.maximum.reduce([V_stop,V_1,V_2])             # optimal to do is to choose the max value of the three
        diff = max(abs(V- value))                           # difference between Vt and Vt-1
        count += 1                                          # keep track of number of iteration
        if count > limit:    # break out of loop if reached the maximum iteration time
            break
        else:
            value = V       # update Vt


    ############################## record V_stop, V_1, V_2 ##############################

    # write cost, V_stop, V_1, V_2 into csv file
    with open('value functions.csv','a',newline='') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow([''.join(['cost=',str(cost)])])
        filewriter.writerow(V_stop)
        filewriter.writerow(V_1)
        filewriter.writerow(V_2)
        
# done, close file        
csvfile.close()

