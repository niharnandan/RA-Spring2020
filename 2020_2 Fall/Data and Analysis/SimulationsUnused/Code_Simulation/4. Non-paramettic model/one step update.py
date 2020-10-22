# import packages
import math
import numpy as np
import matplotlib.pyplot as plt





################################ Explanation ################################
# This code is for plotting one step update version of the two graphs:
# 1) Pr(sample) v.s. V(sample) - V(stop)
# 2) Pr(confirmative) v.s. V(confirmative) - V(contradictory)
# It is calculated with value function table and randomness function, not simulation.
# Note that the second graph doesn't seem very well





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




################### function for action table NOT encoding randomness ###################

def action_table(cost,alpha1,alpha2,stop_cost):

    
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

    return actiontable




################### one step update for Pr(sample) v.s. V(sample) - V(stop) ###################

# optimal value table with cost=80, alpha1=alpha2=1, stop_cost=0
V_optimal = action_table(80,1,1,0)
# conservative value table with cost=80, alpha1=alpha2=0.8, stop_cost=0
V_conservative = action_table(80,0.8,0.8,0)
# confirmative value table with cost=80, alpha1=1.2, alpha2=0.8, stop_cost=0
V_confirmative = action_table(80,1.2,0.8,0)
# with stop cost value table with cost=80, alpha1=alpha2=1, stop_cost=47
V_stopcost = action_table(80,1,1,47)
# V(sample) - V(stop)
sample_stop = np.maximum(V_optimal[1,:],V_optimal[2,:]) - V_optimal[0,:]
# inititate probability of sampling for the optimal case
prob_sample_optimal = []
# initiate probability of sampling for the conservative case
prob_sample_conservative = []
# initiate probability of sampling for the confirmative case
prob_sample_confirmative = []
# initiate probability of sampling for the with stop cost case
prob_sample_stopcost = []
for i in range(1001):
    prob_sample_optimal.append(1-randomness(0.04,V_optimal[0,i],V_optimal[1,i],V_optimal[2,i])[0])
    prob_sample_conservative.append(1-randomness(0.04,V_conservative[0,i],V_conservative[1,i],V_conservative[2,i])[0])
    prob_sample_confirmative.append(1-randomness(0.04,V_confirmative[0,i],V_confirmative[1,i],V_confirmative[2,i])[0])
    prob_sample_stopcost.append(1-randomness(0.04,V_stopcost[0,i],V_stopcost[1,i],V_stopcost[2,i])[0])
# plotting
plt.plot(sample_stop, prob_sample_optimal, 'k', linewidth=3, label='optimal') # optimal with randomness
plt.plot(sample_stop, prob_sample_conservative, 'r', linewidth=3, label='conservative') # conservative with randomness
plt.plot(sample_stop, prob_sample_confirmative, 'b', linewidth=3, label='confirmative') # confirmative with randomness
plt.plot(sample_stop, prob_sample_stopcost, 'g', linewidth=3, label='stop cost') # with stop cost with randomness
lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=4) # add legend




############## one step update for Pr(confirmative) v.s. V(confirmative) - V(contradictory) ##############

# optimal value table with cost=5, alpha1=alpha2=1, stop_cost=0
V_optimal = action_table(5,1,1,0)
# conservative value table with cost=5, alpha1=alpha2=0.8, stop_cost=0
V_conservative = action_table(5,0.8,0.8,0)
# confirmative value table with cost=5, alpha1=1.2, alpha2=0.8, stop_cost=0
V_confirmative = action_table(5,1.2,0.8,0)
# with stop cost value table with cost=5, alpha1=alpha2=1, stop_cost=47
V_stopcost = action_table(5,1,1,47)
# V(confirmative) - V(contradictory)
confirm_contra = []
# inititate probability of sampling confirmative for the optimal case
prob_optimal = []
# inititate probability of sampling confirmative for the conservative case
prob_conservative = []
# inititate probability of sampling confirmative for the confirmative case
prob_confirmative = []
# inititate probability of sampling confirmative for the stop cost case
prob_stopcost = []
for i in range(1001):
    if i < 500: # if i < 500, confirmative case is sampling 2
        confirm_contra.append(V_optimal[2,i]-V_optimal[1,i])
        prob_optimal.append(randomness(0.04,V_optimal[0,i],V_optimal[1,i],V_optimal[2,i])[2])
        prob_conservative.append(randomness(0.04,V_conservative[0,i],V_conservative[1,i],V_conservative[2,i])[2])
        prob_confirmative.append(randomness(0.04,V_confirmative[0,i],V_confirmative[1,i],V_confirmative[2,i])[2])
        prob_stopcost.append(randomness(0.04,V_stopcost[0,i],V_stopcost[1,i],V_stopcost[2,i])[2])
    elif i > 500: # if i > 500, confirmative case is sampling 1
        confirm_contra.append(V_optimal[1,i]-V_optimal[2,i])
        prob_optimal.append(randomness(0.04,V_optimal[0,i],V_optimal[1,i],V_optimal[2,i])[1])
        prob_conservative.append(randomness(0.04,V_conservative[0,i],V_conservative[1,i],V_conservative[2,i])[1])
        prob_confirmative.append(randomness(0.04,V_confirmative[0,i],V_confirmative[1,i],V_confirmative[2,i])[1])
        prob_stopcost.append(randomness(0.04,V_stopcost[0,i],V_stopcost[1,i],V_stopcost[2,i])[1])
# plotting
plt.plot(confirm_contra, prob_optimal, 'k', linewidth=3, label='optimal') # optimal with randomness
plt.plot(confirm_contra, prob_conservative, 'r', linewidth=3, label='conservative') # conservative with randomness
plt.plot(confirm_contra, prob_confirmative, 'b', linewidth=3, label='confirmative') # confirmative with randomness
plt.plot(confirm_contra, prob_stopcost, 'g', linewidth=3, label='stop cost') # with stop cost with randomness
lgd = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=4) # add legend

