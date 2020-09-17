# import packages
import numpy as np
import csv
    




############################### Explanation ###############################
# This is a code for finding the value functions for stopping, investigating 1, 
# and investigating 2 for each prior grid. This is very much the same procedure
# as 'optimal strategy final.py' but store the value functions instead of plotting.

# IMPORTANT NOTE: the value function changes if you change alpha_1, alpha_2, stop_cost.
# If you want to change these three parameters in simulation, change the parameters part
# in this code to get a new value function.





############################### set parameters ###############################
alpha_1 = 0.5 # update in the direction of more likely
alpha_2 = 0.5 # update in the direction of less likely
accuracy1 = 0.25 # prob of reveal for 1
accuracy2 = 0.25 # prob of reveal for 2
cost_vector = [5,10,20,40,80] # cost levels for investigation
stop_cost = 0 # stop cost
reward = 1000 # reward for getting the right state
number = 1001 # number of grids
p_grid = np.linspace(0,1,number,endpoint=True) # p grid




############################### value functions and store into csv ###############################

# write the result in a csv file. It includes:
# 1) parameters: accuracy1, accuracy2, alpha1, alpha2
# 2) for each cost level: V_stop, V_1, V_2
with open('value functions.csv','w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|',quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['accuracy1=',accuracy1])
    filewriter.writerow(['accuracy2=',accuracy2])
    filewriter.writerow(['alpha_1=',alpha_1])
    filewriter.writerow(['alpha_2=',alpha_2])
    filewriter.writerow([])
    filewriter.writerow(['order:','V_stop','V_1','V_2'])
    filewriter.writerow([])


for cost in cost_vector:
    cost1 = cost # same investigation cost for 1 and 2
    cost2 = cost


    ############################### calculate the transition matrix ###############################
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))


    # if investigate state 1
    for i in range(number):
        
        p = p_grid[i] # prob 1 is guilty
        prob_reveal = p*accuracy1 # prob of revealing 1 guilty
        posterior = p*(1-accuracy1)/(1 - prob_reveal) 
        # posterior prob of 1 being guilty conditional on no signal found after investigating 1 once
        
        if (p >= 0.5 and posterior > p) or (p < 0.5 and posterior < p): # update in the more likely direction
            posterior = alpha_1*posterior + (1-alpha_1)*p
        else:
            posterior = alpha_2*posterior + (1-alpha_2)*p # update in the less likely direction   
            
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
        
        if (p >= 0.5 and posterior > p) or (p < 0.5 and posterior < p): # update in the more likely direction
            posterior = alpha_1*posterior + (1-alpha_1)*p
        else:
            posterior = alpha_2*posterior + (1-alpha_2)*p # update in the less likely direction
        
        no_signal = np.argmax(-(abs(p_grid - posterior)))
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal
        if no_signal == (number-1):
            t2[i,no_signal] = 1


    ###################### dynamic programming for convergence of value function ######################
            
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
        V_1 = np.matmul(value,np.transpose(t1)) - cost1 # value of investigating 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2 # value of investigating 2
        V = np.maximum.reduce([V_stop,V_1,V_2]) # optimal to do is to choose the max value of the three
        diff = max(abs(V- value)) # difference between Vt and Vt-1
        count += 1 # keep track of number of iteration
        if count > limit: # break out of loop if reached the maximum iteration time
            break
        else:
            value = V # update Vt


    ############################## record V_stop, V_1, V_2 ##############################

    # write cost, V_stop, V_1, V_2 into csv file
    with open('value functions.csv','a') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow([''.join(['cost=',str(cost)])])
        filewriter.writerow(V_stop)
        filewriter.writerow(V_1)
        filewriter.writerow(V_2)
csvfile.close()
