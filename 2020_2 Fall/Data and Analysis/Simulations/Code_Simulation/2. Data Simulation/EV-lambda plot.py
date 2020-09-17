# import packages
import math
import random
import numpy as np
import csv
import matplotlib.pyplot as plt





############################### Explanation ###############################
# This is a code that plots expected value of a sequence of decisions, over randomness
# (the expected value is approximated by empirical simulation). It has the following structure:
# 1) helper function for randomness
# 2) set parameters (note we have a new parameter k_grid, which is the x-axis grid of lambda)
# 3) empirical simulation and calculation of expected value. It is very much the same process
#    as 'data simulation.py' but keeps track of the value gained for each simulation.
#    Notice parameter 'multiple = True' (this is what we do):
#    - if 'multiple' is set to 'False', it simulates 10000 trials and plots EV over lambda 
#      based on one specific (cost, prior, true state) pair. It is just a toy case for fun.
#      [NOTE: 1. you have to set (c,p) in the code  
#             2. to simulate a different sample size, change 1000 in two places in the code] 
#    - if 'multiple' is set to 'True', it simulates 25*40 trials based on 25 sets of
#      (cost, prior, true state) pair.
#      [NOTE: to simulate a different sample size, change two numbers: 40 and 1000 in the code] 
# 4) plot EV over lambda
# 5) plot difference in V_stop, V_1 and V_2 over the p grid [which intuitively shows why lambda
#    bigger than 0.1 is like a deterministic case. Hence we choose lambda grid to be 0-0.1 for plot.] 

# NOTE 1: if you want to change alpha1, alpha2, stop_cost, change in the 'value functions.py'
#         to generate a different 'value function.csv'
# NOTE 2: what we need to run the code: 'value functions.csv'





############################### helper function ###############################

# function for randomness of the decision making
def randomness(k,v_stop,v_red,v_blue):
    try:
        p_stop = 1/(1+math.exp(k*(v_red-v_stop))+math.exp(k*(v_blue-v_stop)))
    except OverflowError:
        p_stop = 0
    try:
        p_red = 1/(1+math.exp(k*(v_stop-v_red))+math.exp(k*(v_blue-v_red)))
    except OverflowError:
        p_red = 0    
    try:
        p_blue = 1/(1+math.exp(k*(v_stop-v_blue))+math.exp(k*(v_red-v_blue)))
    except OverflowError:
        p_blue = 0
    return (p_stop,p_red,p_blue)




############################### set parameters ###############################
 
# we have a new parameter k_grid here, which is a lambda grid
k_grid = np.linspace(0,0.1,101,endpoint=True) # parameter (lambda) in randomness
p_grid = np.linspace(0,1,1001,endpoint=True) # p grid
reward = 1000 # initial reward for guessing the correct state
trial = 60 # total number of available trials
cost = [5,10,20,40,80] # cost per investigation
prior = [0.1,0.3,0.5,0.7,0.9] # prior probability of 1 guilty
count = 0 # keep track of the number of trial (no greater than 60)
true_state = ['red','blue','blue','red','red','blue','red','blue','red',
              'red','blue','red','blue','red','red','blue','blue','blue',
              'red','red','blue','red','blue','red','blue'] # truly guilty state
EV = [] #expected value for different grid of randomness
multiple = True # whether we use multiple cost and prior for calculating expected value


# read from csv file stored as 'value functions.csv' the following parameters:
# accuracy1 (prob of finding 1 guilty conditional on 1 guilty), accuracy2, alpha_1, alpha_2
with open('value functions.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    accuracy1 = float(next(filereader)[1])
    accuracy2 = float(next(filereader)[1])
    alpha_1 = float(next(filereader)[1])
    alpha_2 = float(next(filereader)[1])




########################## simulation and calculating EV from empirical distribution ##########################

# simulation for empiricial expected value for each lambda grid
for k in k_grid:
    
    sum_value = 0 # initiate for carrying expected value



    ################### below part calculate EV for a specific (cost, prior, true state) pair ###################
    
    if multiple == False: 
        
        # assign cost and prior
        c = 5
        p = 0.1
        
        # read V_stop, V_1, and V_2 of the cost level
        with open('value functions.csv','r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            for line, content in enumerate(filereader):
                if content == [''.join(['cost=',str(c)])]:
                    line_num = line # identify the line of cost = c
                    break
            V_stop = next(filereader)
            V_stop = [float(i) for i in V_stop] # change str type to float
            V_1 = next(filereader)
            V_1 = [float(i) for i in V_1]
            V_2 = next(filereader)
            V_2 = [float(i) for i in V_2]
        
        idx = cost.index(c)*5 + prior.index(p) # index for truly guilty state of (c,p)
        guilty = true_state[idx] # true state
        p0 = p # instore value of p into p0, so that we can reset after break from one trial

        for i in range(1000): # 1000 simulations
            choice_made = False # keep track of whether a choice is made
            value = reward #initial value for each trial
            count = 0 # keep track of the number of investigation (60 maximum)
            while (count <= trial): # when we have not reached total available investigation number (60)
                count += 1 # keep track of number of times we have investigated
                p_index = np.argmax(-(abs(p_grid - p))) # find the position of p in p_grid
                # find the value of stop, 1, 2 for that p, and the prob of stop, 1, 2 based on randomness
                choice = randomness(k,V_stop[p_index],V_1[p_index],V_2[p_index])
                random_action = random.random() # generate a random number
                
                # case 1: accuse
                if random_action <= choice[0]:
                    if (p>=0.5 and guilty == 'red') or (p<0.5 and guilty == 'blue'): # accuse the right state
                        sum_value += value
                        p = p0 # reset p
                        choice_made = True # indicater of choice made
                        break
                
                # case 2: investigate red
                elif random_action <= 1-choice[2]:
                    value -= c # investigation cost
                    # red is guilty and evidence is shown, then accuse red
                    if random.random()<=accuracy1 and guilty == 'red':
                        sum_value += value # accuse the right state
                        p = p0 # reset p
                        choice_made = True # indicater of choice made
                        break
                    else: # no evidence
                        posterior = p*(1-accuracy1)/(1 - p*accuracy1)
                        if p < 0.5: # more likely
                            p = alpha_1*posterior + (1-alpha_1)*p
                        else: # less likely
                            p = alpha_2*posterior + (1-alpha_2)*p
                        p = min(max(p,0),1) # updated p in (0,1)
                
                # case 3: investigate blue
                else:
                    value -= c # investigation cost
                    # blue is guilty and evidence is shown, then accuse blue
                    if random.random()<=accuracy2 and guilty == 'blue':
                        sum_value += value # accuse the right state
                        p = p0 # reset p
                        choice_made = True # indicater of choice made
                        break
                    else: # no evidence
                        posterior = p/(1 - (1-p)*accuracy2)
                        if p >= 0.5: # more likely
                            p = alpha_1*posterior + (1-alpha_1)*p
                        else:
                            p = alpha_2*posterior + (1-alpha_2)*p
                        p = min(max(p,0),1) # updated p in (0,1)
            
            # if we run out of investigation opportunities, but don't make a decision yet                
            if choice_made == False:
                if (p>=0.5 and guilty == 'red') or (p<0.5 and guilty == 'blue'):
                    sum_value += value # accuse the right state
                    p = p0
            
        EV.append(sum_value/1000) # empirical expected value for the 1000 simulation



    ################# below part calculate EV for all combinations (cost, prior, true state) pair #################
    else:
        
        for c in cost: # for each cost level
    
            # the following lines read V_stop, V_1, V_2 of the corresponding cost from 'value functions.csv'
            with open('value functions.csv','r') as csvfile:
                filereader = csv.reader(csvfile, delimiter=',')
                for line, content in enumerate(filereader):
                    if content == [''.join(['cost=',str(c)])]:
                        line_num = line # identify the line of cost = c
                        break
                V_stop = next(filereader)
                V_stop = [float(i) for i in V_stop] # change str type to float
                V_1 = next(filereader)
                V_1 = [float(i) for i in V_1]
                V_2 = next(filereader)
                V_2 = [float(i) for i in V_2]
                        
            for p in prior: # for each prior level
        
                idx = cost.index(c)*5 + prior.index(p) # index for truly guilty state of (c,p)
                guilty = true_state[idx] # true state
                p0 = p # instore value of p into p0, so that we can reset after break from one trial
        
                for i in range(40): # forty simulations
                    choice_made = False # keep track of whether a choice is made
                    value = reward # initial value for each trial
                    count = 0 # keep track of the number of investigation (60 maximum)
                    while (count <= trial): # when we have not reached total available investigation number (60)
                        count += 1 # keep track of number of times we have investigated
                        p_index = np.argmax(-(abs(p_grid - p))) # find the position of p in p_grid
                        # find the value of stop, 1, 2 for that p, and the prob of stop, 1, 2 based on randomness
                        choice = randomness(k,V_stop[p_index],V_1[p_index],V_2[p_index])
                        random_action = random.random() # generate a random number
                
                        # case 1: accuse
                        if random_action <= choice[0]:
                            if (p>=0.5 and guilty == 'red') or (p<0.5 and guilty == 'blue'): # accuse the right state
                                sum_value += value
                            p = p0 # reset p
                            choice_made = True # indicater of choice made
                            break
                
                        # case 2: investigate red
                        elif random_action <= 1-choice[2]:
                            value -= c # investigation cost
                            # red is guilty and evidence is shown, then accuse red
                            if random.random()<=accuracy1 and guilty == 'red':
                                sum_value += value # accuse the correct state
                                p = p0 # reset p
                                choice_made = True # indicater of choice made
                                break
                            else: # no evidence
                                posterior = p*(1-accuracy1)/(1 - p*accuracy1)
                                if p < 0.5: # more likely
                                    p = alpha_1*posterior + (1-alpha_1)*p
                                else: # less likely
                                    p = alpha_2*posterior + (1-alpha_2)*p
                                p = min(max(p,0),1) # updated p in (0,1)
                
                        # case 3: investigate blue
                        else:
                            value -= c # investigation cost
                            # blue is guilty and evidence is shown, then accuse blue
                            if random.random()<=accuracy2 and guilty == 'blue':
                                sum_value += value # accuse the right state
                                p = p0 # reset p
                                choice_made = True # indicater of choice made
                                break
                            else: # no evidence
                                posterior = p/(1 - (1-p)*accuracy2)
                                if p >= 0.5: # more likely
                                    p = alpha_1*posterior + (1-alpha_1)*p
                                else: # less likely
                                    p = alpha_2*posterior + (1-alpha_2)*p
                                p = min(max(p,0),1) # updated p in (0,1)
            
                    # if we run out of investigation opportunities, but don't make a decision yet                
                    if choice_made == False:
                        if (p>=0.5 and guilty == 'red') or (p<0.5 and guilty == 'blue'): # red likely to be guilty
                            sum_value += value # accuse the right state
                        p = p0 # reset p
            
        EV.append(sum_value/1000) # empirical expected value for the 1000 simulation




############################### plot EV over lambda ###############################
plt.rcParams['axes.labelsize'] = 11
plt.plot(k_grid, EV,'k', linewidth=2)
plt.xlabel('lambda')
plt.ylabel('EV')




########################## plot difference in V_stop, V_1 and V_2 over the p grid ##########################
if False:
    V_stop = np.array(V_stop)
    V_1 = np.array(V_1)
    V_2 = np.array(V_2)
    plt.plot(p_grid, abs(V_stop-V_1),'r', linewidth=1, label='V_stop - V_1') # absolute difference between V_stop and V_red
    plt.plot(p_grid, abs(V_stop-V_2),'b', linewidth=1, label='V_stop - V_2') # absolute difference between V_stop and V_blue
    plt.plot(p_grid, abs(V_1-V_2),'k', linewidth=1, label='V_1 - V_2') # absolute difference between V_red and V_blue
    plt.xlabel('Probability')
    plt.ylabel('Value')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3) # add legend
    plt.title('Difference in Value')   
     