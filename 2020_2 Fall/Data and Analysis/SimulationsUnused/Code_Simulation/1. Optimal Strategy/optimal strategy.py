# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# set print options
np.set_printoptions(threshold=1200)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',500)





############################### Explanation ###############################
# The code consists of two base cases: 1) fixed number of trials (p=0.6, acc=0.25), with no cost
# 2) with cost each investigation, agent choose to stop


# in the 1) part, three tables are printed: 
# - (number of investigations, probability of reveal, posterior, expected value)
# - given different prior, the optimal number of times to investigate 1
# - given different prior, percentage of times to investigate 1


# in the 2) part, we invesitgate the following:
# - for a fixed level of investigation cost, we plot the following:
#     1. color indicated optimal strategy
#     2. expected value of optimal strategy v.s. immediate stop
#     3. expected value of optimal strategy with corresponding stretagy indicated 
#   NOTE: To plot the graph, change 'if False' to 'if True'

# - for five different cost levels, we plot the optimal investigation strategy 
#   over the prior grid for each cost level with four senarios:
#     1. symmetric cost
#     2. asymetric cost
#     3. conservative updating
#     4. confirmative updating

# This is a base case code. In 'optimal strategy final.py', we write code in part 2 into
# combined single one piece with parameters






##################### fixed number of trials, with no cost #####################
p = 0.6 # probability that the state is 1
accuracy = 0.25 # probability of finding evidence conditional on searching the right state
n = 9 # number of available samples
table = pd.DataFrame(columns=['num_invst', 'prob_reveal', 'posterior', 'EV']) 
# initiate a dataframe for results of different sampling strategy

# for evaluating sampling strategies
for i in range(n+1):
    # sampling strategy: draw #sample1 of samples from 1 and #sample2 of samples from 2
    sample1 = i #number of samples from state 1
    sample2 = n - i #number of sample from state 2
    
    # probability of revealing a signal = 1 - probability of not revealing a signal
    # = 1 - Pr(not revealing|the state is 1) * Pr(the state is 1) 
    # - Pr(not revealing|the state is 2) * Pr(the state is 2)
    prob_reveal = 1 - p*(1-accuracy)**sample1 - (1-p)*(1-accuracy)**sample2
    
    # Bayes updates after n sample drawn:
    # Pr(the state is 1|no signal shown) = Pr(no signal shown|the state is 1) * Pr(the state is 1)
    # / Pr(no signal shown)
    prior = p
    likelihood = (1-accuracy)**sample1
    posterior = prior*likelihood/(1 - prob_reveal)
    
    # subject's valuation of the strategy under Bayes rule
    expected_valuation = prob_reveal + (1-prob_reveal)*max(posterior, 1-posterior)
    
    # store information
    table = table.append({'num_invst': i, 'prob_reveal': prob_reveal, 'posterior': posterior, 'EV': expected_valuation}, ignore_index=True)
table['num_invst'] = table['num_invst'].astype(int) #change type
# print the table
print(table.to_string(index = False))


##################### grid of posterior #####################
p = 0.6 # probability that the state is 1
accuracy = 0.25 # probability of finding evidence conditional on searching the right state
n = 9 # number of available samples
posterior_grid = pd.DataFrame(np.zeros((n+1,n+1)))
for i in range(n+1):
    for j in range(n+1):
        sample1 = i
        sample2 = j
        prob_reveal = 1 - p*(1-accuracy)**sample1 - (1-p)*(1-accuracy)**sample2
        prior = p
        likelihood = (1-accuracy)**sample1
        posterior = prior*likelihood/(1 - prob_reveal)
        posterior_grid.at[i,j] = posterior
# symmetric along the secondary dignonal (i,j),(9-j,9-i)


##################### optimal strategy for each condition #####################
p_grid = np.around(np.linspace(0.1,0.9,5,endpoint=True), decimals=1) # probability that the state is 1
n_grid = np.arange(1,11,2) # total number of times to investigate
# assume no fully reveal signal, given a total number of trials available, the table gives
# optimal time a subject should investigate 1

optimal_table = pd.DataFrame() 

for p in p_grid:
    for n in n_grid:
        table = np.zeros((n+1,3))
        table[:,0] = range(n+1)
        for i in range(n+1):
            sample1 = i
            sample2 = n-i
            prob_reveal = 1 - p*(1-accuracy)**sample1 - (1-p)*(1-accuracy)**sample2
            prior = p
            likelihood = (1-accuracy)**sample1
            posterior = prior*likelihood/(1 - prob_reveal)
            expected_valuation = prob_reveal + (1-prob_reveal)*max(posterior, 1-posterior)
            table[i,0:3] = [prob_reveal, posterior, expected_valuation]
        best_row = np.argmax(table[:,2], axis = 0)
        optimal_table.at[p, n] = best_row
        
optimal_table = optimal_table.astype(int)
print(optimal_table)        

# in relative value: number of time investigating 1 / number of total investigation
print(optimal_table/n_grid)        










##################### with cost for each search, choose to stop #####################



##################### with one cost level cost=20 #####################

# parameters of the problem
accuracy1 = 0.25 # probability of finding evidence searching 1 condition on state 1 is guilty
accuracy2 = 0.25 # probability of finding evidence searching 2 condition on state 2 is guilty
cost1 = 20 # cost of collecting sample from 1
cost2 = 20 # cost of collecting sample from 2
reward = 1000 # reward for finding the correct state

# grid of probability
number = 1001 # number of grids
p_grid = np.linspace(0,1,number,endpoint=True)

# matrix of transition matrix: each entry (prior, posterior) is the probability 
# from prior to posterior investigating the state once
t1 = np.zeros((number, number))
t2 = np.zeros((number, number))

# if investigate state 1
for i in range(number):
    p = p_grid[i]
    prob_reveal = p*accuracy1
    posterior = p*(1-accuracy1)/(1 - prob_reveal)
    # find the position of number in p_grid that are most close to posterior calculated
    no_signal = np.argmax(-(abs(p_grid - posterior))) 
    # if there is signal shown (with probability 'prob_reveal'), posterior is 1
    t1[i,number-1] = prob_reveal 
    t1[i,no_signal] = 1 - prob_reveal # if there is no signal shown
    if no_signal == (number-1): # if posterior of no signal found is also 1, 
        t1[i, no_signal] = 1 # then probability of posterior being 1 is 1

# if investigate state 2
for i in range(number):
    p = p_grid[i]
    prob_reveal = (1-p)*accuracy2
    posterior = p/(1 - prob_reveal)
    # find the position of number in p_grid that are most close to posterior calculated
    no_signal = np.argmax(-(abs(p_grid - posterior))) 
    # if there is signal shown (with probability 'prob_reveal'), posterior is 1
    t2[i,number-1] = prob_reveal 
    t2[i,no_signal] = 1 - prob_reveal # if there is no signal shown
    if no_signal == (number-1): # if posterior of no signal found is also 1, 
        t2[i,no_signal] = 1 # then probability of posterior being 1 is 1


### We now investigate given a probability p, what is optimal to do next (stop, investgate 1, investigate 2 ###        

# value function for stop (for each p grid)
stop_value = reward * np.maximum(p_grid, 1-p_grid)

# initiate value for each probability
value = np.zeros(number)
# tolerance for convergence
error = 0.00000005

### convergence to the optimal strategy ###
limit = 1000000 # maximum number to iterate
diff = 1 # initiate value for difference between Vk and Vk+1
count = 1 # to keep track of the number of times we have iterated

while diff > error: # iterate until reach tolerance level
    V_stop = stop_value # value if stop (for each p)
    # value%*%t(t1) - cost gives the value of investigating 1 for each p 
    # think! the value of investigating 1 for each prior is the probability of getting to 
    # each posterior * the value of that that posterior
    V_1 = np.matmul(value,np.transpose(t1)) - cost1 #value of investigate 1
    V_2 = np.matmul(value,np.transpose(t2)) - cost2 #value of investigate 2
    V = np.maximum.reduce([V_stop,V_1,V_2])
    diff = max(abs(V- value))
    count += 1
    if count > limit:
        break
    else:
        value = V

# figure out what is the optimal strategy in each step
action_stop = (V_stop == value)
action_1 = (V_1 == value)
action_2 = (V_2 == value)


##################### plot graphs #####################

# plot: optimal stretagy 
if False:
    plt.xlim([0, 1])
    plt.ylim([0.9, 1.1])
    plt.plot(p_grid, np.ma.masked_where(action_stop==False, action_stop), 'k', linewidth=3, label='stop')
    plt.plot(p_grid, np.ma.masked_where(action_1==False, action_1), 'r', linewidth=3, label='investigate 1')
    plt.plot(p_grid, np.ma.masked_where(action_2==False, action_2), 'b', linewidth=3, label='investigate 2')
    plt.xlabel('Prior probability')
    plt.ylabel('Color indicated strategy')
    plt.legend()
    
# plot: expected value of optimal stretagy
if False:
    plt.xlim([0, 1])
    plt.ylim([min(value)-0.1*(max(value)-min(value)), max(value)+0.1*(max(value)-min(value))])
    plt.plot(p_grid, V_stop, 'k--', linewidth=3, label='immediate choice')
    plt.plot(p_grid, value, 'b', linewidth=3, label='optimal stretagy')
    plt.xlabel('Prior probability')
    plt.ylabel('Expected value')
    plt.legend()
   
# plot: expected value with corresponding stretagy indicated      
if False:
    plt.xlim([0, 1])
    plt.ylim([min(value)-0.1*(max(value)-min(value)), max(value)+0.1*(max(value)-min(value))])
    plt.plot(np.ma.masked_where(action_stop==False, p_grid), np.ma.masked_where(action_stop==False, value), 'k', linewidth=3, label='stop')
    plt.plot(np.ma.masked_where(action_1==False, p_grid), np.ma.masked_where(action_1==False, value), 'r', linewidth=3, label='investigate 1')
    plt.plot(np.ma.masked_where(action_2==False, p_grid), np.ma.masked_where(action_2==False, value), 'b', linewidth=3, label='investigate 2')
    plt.xlabel('Prior probability')
    plt.ylabel('Expected value')
    plt.legend()










##################### with five cost level #####################
   

##################### senario for symmetric cost, choose to stop #####################
cost_vector = [5,10,20,40,80]
for cost in cost_vector:
    #parameter
    accuracy1 = 0.25
    accuracy2 = 0.25
    cost1 = cost
    cost2 = cost
    reward = 1000
    #prob grid
    number = 1001 # number of grids
    p_grid = np.linspace(0,1,number,endpoint=True)

    # matrix of transition matrix
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))

    # if investigate state 1
    for i in range(number):
        p = p_grid[i]
        prob_reveal = p*accuracy1
        posterior = p*(1-accuracy1)/(1 - prob_reveal)
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t1[i,number-1] = prob_reveal 
        t1[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t1[i, no_signal] = 1 # then probability of posterior being 1 is 1

    # if investigate state 2
    for i in range(number):
        p = p_grid[i]
        prob_reveal = (1-p)*accuracy2
        posterior = p/(1 - prob_reveal)
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t2[i,no_signal] = 1 # then probability of posterior being 1 is 1
            
    # value function for stop (for each p grid)
    stop_value = reward * np.maximum(p_grid, 1-p_grid)

    # initiate optimal value for each probability
    value = np.zeros(number)
    # tolerance for convergence
    error = 0.00000005

    # convergence to the optimal strategy
    limit = 1000000 # maximum number to iterate
    diff = 1 # initiate value for difference between Vk and Vk+1
    count = 1 # to keep track of the number of times we have iterated

    while diff > error: # iterate until reach tolerance level
        V_stop = stop_value # value if stop (for each p)
        V_1 = np.matmul(value,np.transpose(t1)) - cost1 #value of investigate 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2 #value of investigate 2
        V = np.maximum.reduce([V_stop,V_1,V_2])
        diff = max(abs(V- value))
        count += 1
        if count > limit:
            break
        else:
            value = V

    # optimal strategy
    action_stop = (V_stop == value)
    action_1 = (V_1 == value)
    action_2 = (V_2 == value)
    
    # plot scatter plot
    plt.plot(p_grid, cost*np.ma.masked_where(action_stop==False, action_stop),'k', linewidth=3, label='stop')
    plt.plot(p_grid, cost*np.ma.masked_where(action_1==False, action_1),'r', linewidth=3, label='investigate 1')
    plt.plot(p_grid, cost*np.ma.masked_where(action_2==False, action_2),'b', linewidth=3, label='investigate 2')

plt.xlabel('Prior probability')
plt.ylabel('Cost per sample')
#plt.legend()
plt.title('Optimal Strategy with symmetric cost')

for i in np.linspace(0.1,0.9,5,endpoint=True):
    plt.plot((i, i), (0, 85), 'k:', linewidth=1)






##################### senario for asymmetric cost, choose to stop #####################
cost_vector = [5,10,20,40,80]
for cost in cost_vector:
    #parameter
    accuracy1 = 0.25
    accuracy2 = 0.25
    cost1 = cost*0.9
    cost2 = cost*1.1
    reward = 1000
    #prob grid
    number = 1001 # number of grids
    p_grid = np.linspace(0,1,number,endpoint=True)

    # matrix of transition matrix
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))

    # if investigate state 1
    for i in range(number):
        p = p_grid[i]
        prob_reveal = p*accuracy1
        posterior = p*(1-accuracy1)/(1 - prob_reveal)
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t1[i,number-1] = prob_reveal 
        t1[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t1[i, no_signal] = 1 # then probability of posterior being 1 is 1

    # if investigate state 2
    for i in range(number):
        p = p_grid[i]
        prob_reveal = (1-p)*accuracy2
        posterior = p/(1 - prob_reveal)
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t2[i,no_signal] = 1 # then probability of posterior being 1 is 1
            
    # value function for stop (for each p grid)
    stop_value = reward * np.maximum(p_grid, 1-p_grid)

    # initiate optimal value for each probability
    value = np.zeros(number)
    # tolerance for convergence
    error = 0.00000005

    # convergence to the optimal strategy
    limit = 1000000 # maximum number to iterate
    diff = 1 # initiate value for difference between Vk and Vk+1
    count = 1 # to keep track of the number of times we have iterated

    while diff > error: # iterate until reach tolerance level
        V_stop = stop_value # value if stop (for each p)
        V_1 = np.matmul(value,np.transpose(t1)) - cost1 #value of investigate 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2 #value of investigate 2
        V = np.maximum.reduce([V_stop,V_1,V_2])
        diff = max(abs(V- value))
        count += 1
        if count > limit:
            break
        else:
            value = V

    # optimal strategy
    action_stop = (V_stop == value)
    action_1 = (V_1 == value)
    action_2 = (V_2 == value)
    
    # plot scatter plot
    plt.plot(p_grid, cost*np.ma.masked_where(action_stop==False, action_stop),'k', linewidth=3, label='stop')
    plt.plot(p_grid, cost*np.ma.masked_where(action_1==False, action_1),'r', linewidth=3, label='investigate 1')
    plt.plot(p_grid, cost*np.ma.masked_where(action_2==False, action_2),'b', linewidth=3, label='investigate 2')

plt.xlabel('Prior probability')
plt.ylabel('Cost per sample')
#plt.legend()
plt.title('Optimal Strategy with asymmetric cost')

for i in np.linspace(0.1,0.9,5,endpoint=True):
    plt.plot((i, i), (0, 85), 'k:', linewidth=1)






##################### senario for conservative, choose to stop #####################
coef = 0.8 #coefficient for conservative
cost_vector = [5,10,20,40,80]
for cost in cost_vector:
    #parameter
    accuracy1 = 0.25
    accuracy2 = 0.25
    cost1 = cost
    cost2 = cost
    reward = 1000
    #prob grid
    number = 1001 # number of grids
    p_grid = np.linspace(0,1,number,endpoint=True)

    # matrix of transition matrix
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))

    # if investigate state 1
    for i in range(number):
        p = p_grid[i]
        prob_reveal = p*accuracy1
        posterior = p*(1-accuracy1)/(1 - prob_reveal)
        posterior = coef*(posterior-p)+p
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t1[i,number-1] = prob_reveal 
        t1[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t1[i, no_signal] = 1 # then probability of posterior being 1 is 1

    # if investigate state 2
    for i in range(number):
        p = p_grid[i]
        prob_reveal = (1-p)*accuracy2
        posterior = p/(1 - prob_reveal)
        posterior = coef*(posterior-p)+p
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t2[i,no_signal] = 1 # then probability of posterior being 1 is 1
            
    # value function for stop (for each p grid)
    stop_value = reward * np.maximum(p_grid, 1-p_grid)

    # initiate optimal value for each probability
    value = np.zeros(number)
    # tolerance for convergence
    error = 0.00000005

    # convergence to the optimal strategy
    limit = 1000000 # maximum number to iterate
    diff = 1 # initiate value for difference between Vk and Vk+1
    count = 1 # to keep track of the number of times we have iterated

    while diff > error: # iterate until reach tolerance level
        V_stop = stop_value # value if stop (for each p)
        V_1 = np.matmul(value,np.transpose(t1)) - cost1 #value of investigate 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2 #value of investigate 2
        V = np.maximum.reduce([V_stop,V_1,V_2])
        diff = max(abs(V- value))
        count += 1
        if count > limit:
            break
        else:
            value = V

    # optimal strategy
    action_stop = (V_stop == value)
    action_1 = (V_1 == value)
    action_2 = (V_2 == value)
    
    # plot scatter plot
    plt.plot(p_grid, cost*np.ma.masked_where(action_stop==False, action_stop),'k', linewidth=3, label='stop')
    plt.plot(p_grid, cost*np.ma.masked_where(action_1==False, action_1),'r', linewidth=3, label='investigate 1')
    plt.plot(p_grid, cost*np.ma.masked_where(action_2==False, action_2),'b', linewidth=3, label='investigate 2')

plt.xlabel('Prior probability')
plt.ylabel('Cost per sample')
#plt.legend()
plt.title('Optimal Strategy with conservative belief')

for i in np.linspace(0.1,0.9,5,endpoint=True):
    plt.plot((i, i), (0, 85), 'k:', linewidth=1)






##################### senario for confirmative, choose to stop #####################
coef = [1.1, 0.9] #coefficient for conservative
cost_vector = [5,10,20,40,80]
for cost in cost_vector:
    #parameter
    accuracy1 = 0.25
    accuracy2 = 0.25
    cost1 = cost
    cost2 = cost
    reward = 1000
    #prob grid
    number = 1001 # number of grids
    p_grid = np.linspace(0,1,number,endpoint=True)

    # matrix of transition matrix
    t1 = np.zeros((number, number))
    t2 = np.zeros((number, number))

    # if investigate state 1
    for i in range(number):
        p = p_grid[i]
        prob_reveal = p*accuracy1
        posterior = p*(1-accuracy1)/(1 - prob_reveal)
        if (p >= 0.5 and posterior > p) or (p < 0.5 and posterior < p):
            posterior = coef[1]*(posterior-p)+p
        else:
            posterior = coef[0]*(posterior-p)+p
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t1[i,number-1] = prob_reveal 
        t1[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t1[i, no_signal] = 1 # then probability of posterior being 1 is 1

    # if investigate state 2
    for i in range(number):
        p = p_grid[i]
        prob_reveal = (1-p)*accuracy2
        posterior = p/(1 - prob_reveal)
        if (p >= 0.5 and posterior > p) or (p < 0.5 and posterior < p):
            posterior = coef[1]*(posterior-p)+p
        else:
            posterior = coef[0]*(posterior-p)+p
        # find the position of number in p_grid that are most close to posterior calculated
        no_signal = np.argmax(-(abs(p_grid - posterior))) 
        # if there is signal shown (with probability 'prob_reveal'), posterior is 1
        t2[i,number-1] = prob_reveal 
        t2[i,no_signal] = 1 - prob_reveal # if there is no signal shown
        if no_signal == (number-1): # if posterior of no signal found is also 1, 
            t2[i,no_signal] = 1 # then probability of posterior being 1 is 1
            
    # value function for stop (for each p grid)
    stop_value = reward * np.maximum(p_grid, 1-p_grid)

    # initiate optimal value for each probability
    value = np.zeros(number)
    # tolerance for convergence
    error = 0.00000005

    # convergence to the optimal strategy
    limit = 1000000 # maximum number to iterate
    diff = 1 # initiate value for difference between Vk and Vk+1
    count = 1 # to keep track of the number of times we have iterated

    while diff > error: # iterate until reach tolerance level
        V_stop = stop_value # value if stop (for each p)
        V_1 = np.matmul(value,np.transpose(t1)) - cost1 #value of investigate 1
        V_2 = np.matmul(value,np.transpose(t2)) - cost2 #value of investigate 2
        V = np.maximum.reduce([V_stop,V_1,V_2])
        diff = max(abs(V- value))
        count += 1
        if count > limit:
            break
        else:
            value = V

    # optimal strategy
    action_stop = (V_stop == value)
    action_1 = (V_1 == value)
    action_2 = (V_2 == value)
    
    # plot scatter plot
    plt.plot(p_grid, cost*np.ma.masked_where(action_stop==False, action_stop),'k', linewidth=3, label='stop')
    plt.plot(p_grid, cost*np.ma.masked_where(action_1==False, action_1),'r', linewidth=3, label='investigate 1')
    plt.plot(p_grid, cost*np.ma.masked_where(action_2==False, action_2),'b', linewidth=3, label='investigate 2')

plt.xlabel('Prior probability')
plt.ylabel('Cost per sample')
#plt.legend()
plt.title('Optimal Strategy with confirmative')

for i in np.linspace(0.1,0.9,5,endpoint=True):
    plt.plot((i, i), (0, 85), 'k:', linewidth=1)

