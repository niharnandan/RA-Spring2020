# import packages
import csv
import numpy as np
import matplotlib.pyplot as plt





################################ Explanation ################################
# This code plots Pr(sampling) v.s. V(sample)-V(stop), for different set of parameters
# alpha1-alpha2-lambda-stop_cost. It plots the following senarios:
# 1) optimal case: 1-1-10-0
# 2) noisy unbiased case: 1-1-0.04-0
# 3) conservative case: 0.8-0.8-0.04-0
# 4) noisy with stop cost case: 1-1-0.04-47
# 5) confirmatory case: 1.2-0.8-0.04-0
# 6) experimental data

# Note: we need 1) 'value functions.csv' which the the value functions for Baysian optimal
#               2) '1-1-10-0.csv', '1-1-0.04-0.csv', '0.8-0.8-0.04-0.csv', '1-1-0.04-47.csv',
#                  '1.2-0.8-0.04-0.csv', 'Bayes Results.csv', which are the simulated data
#                  with the parameters specified and the experimental data.  





################### function for calculate V(sample) - V(stop) ###################
def sample_stop(index, V):
    v_sample = max(V[1,index],V[2,index])
    v_stop = V[0,index]
    return v_sample-v_stop 




############### Baysian optimal value function for different cost level ###############

# The value functions are calculated with alpha1 = 1, alpha2 = 1,
# lambda = infinity (deterministic), stop_cost = 0. For each cost level cost = c,
# the 3*1001 value function is stored as Vc, e.g. V5 is the Baysian optimal 
# value function for cost = 5.

cost = [5,10,20,40,80] # five cost level
for c in cost:
    
    # the following lines read V_stop, V_1, V_2 of the corresponding cost from 'value functions.csv'
    with open('value functions.csv','r') as csvfile:
        filereader = csv.reader(csvfile, delimiter=',')
        for line, content in enumerate(filereader):
            if content == [''.join(['cost=',str(c)])]:
                line_num = line # identify the line of cost = c
                break
        V_stop = next(filereader) # V_stop
        V_stop = [float(i) for i in V_stop] # change str type to float
        V_1 = next(filereader) # V_1
        V_1 = [float(i) for i in V_1] # change str type to float
        V_2 = next(filereader) # V_2
        V_2 = [float(i) for i in V_2] # change str type to float
    # value table of 3*1001 for cost level c, store as variable
    vars()[''.join(['V',str(c)])] = np.zeros((3,1001)) 
    vars()[''.join(['V',str(c)])][0,:] = V_stop
    vars()[''.join(['V',str(c)])][1,:] = V_1
    vars()[''.join(['V',str(c)])][2,:] = V_2




########################## for optimal case: 1-1-10-0 ##########################

# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('1-1-10-0.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader) # skip the first line
    for file_row in filereader: # read each row of the simulation
        c = float(file_row[2]) # identify the cost
        V = vars()[''.join(['V',str(int(c))])] # find the value function for the cost level
        prior = float(file_row[3]) # identify the prior
        action = file_row[7:] # identify the sequence of decisions
        # for each choice in the decision sequence, identify: 1) stop or sample 2) V(sample)-V(stop)
        for choice in action:
            index = np.argmax(-(abs(p_grid - prior)))
            value = sample_stop(index, V)
            if choice == 'investigate_red':
                prior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                sampling = 1
            elif choice == 'investigate_blue':
                prior = prior/(1 - (1-prior)*accuracy2)
                sampling = 1
            elif choice == 'evidence_shown':
                prior = 1
            elif choice == 'accuse_red' or choice == 'accuse_blue':
                sampling = 0
            dict[sampling].append(value)
            
# scatter plot for stopping and sampling
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.ones(len(dict[1])), marker='o')

# look at the values (V(sample)-V(stop)) in stopping and sampling
if False:
    np.unique(dict[0])
    np.unique(dict[1])
    
# calculate the probability of sampling versus V(sample)-V(stop)
prob = []
v_diff = [-80,-55,-40,-20,-15,-10,-5,5,25,35,45,60,75]
prob.append(sum(1 for i in dict[1] if i==-80)/(sum(1 for i in dict[0] if i==-80)+sum(1 for i in dict[1] if i==-80)))
prob.append(sum(1 for i in dict[1] if -60 <=i <=-50)/(sum(1 for i in dict[0] if -60 <=i <=-50)+sum(1 for i in dict[1] if -60 <=i <=-50)))
prob.append(sum(1 for i in dict[1] if i==-40)/(sum(1 for i in dict[0] if i==-40)+sum(1 for i in dict[1] if i==-40)))
prob.append(sum(1 for i in dict[1] if i==-20)/(sum(1 for i in dict[0] if i==-20)+sum(1 for i in dict[1] if i==-20)))
prob.append(sum(1 for i in dict[1] if -20 <i <-10)/(sum(1 for i in dict[0] if -20 <i <-10)+sum(1 for i in dict[1] if -20 <i <-10)))
prob.append(sum(1 for i in dict[1] if i==-10)/(sum(1 for i in dict[0] if i==-10)+sum(1 for i in dict[1] if i==-10)))
prob.append(sum(1 for i in dict[1] if -10 <i <=0)/(sum(1 for i in dict[0] if -10 <i <=0)+sum(1 for i in dict[1] if -10 <i <=0)))
prob.append(sum(1 for i in dict[1] if 0 <i <=10)/(sum(1 for i in dict[0] if 0 <i <=10)+sum(1 for i in dict[1] if 0 <i <=10)))
prob.append(sum(1 for i in dict[1] if 20 <=i <30)/(sum(1 for i in dict[0] if 20 <=i <30)+sum(1 for i in dict[1] if 20 <=i <30)))
prob.append(sum(1 for i in dict[1] if 30 <=i <40)/(sum(1 for i in dict[0] if 30 <=i <40)+sum(1 for i in dict[1] if 30 <=i <40)))
prob.append(sum(1 for i in dict[1] if 40 <=i <50)/(sum(1 for i in dict[0] if 40 <=i <50)+sum(1 for i in dict[1] if 40 <=i <50)))
prob.append(sum(1 for i in dict[1] if 60 <=i <70)/(sum(1 for i in dict[0] if 60 <=i <70)+sum(1 for i in dict[1] if 60 <=i <70)))
prob.append(sum(1 for i in dict[1] if 70 <=i <80)/(sum(1 for i in dict[0] if 70 <=i <80)+sum(1 for i in dict[1] if 70 <=i <80)))

# plot of probability of sampling versus V_diff
if False:
    plt.plot(v_diff, prob, marker='o')
            
            


########################## for noisy unbiased case: 1-1-0.04-0 ##########################

# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)            
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('1-1-0.04-0.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader) # skip the first line
    for file_row in filereader: # read each row
        c = float(file_row[2]) # identify the cost
        V = vars()[''.join(['V',str(int(c))])] # identify the value function for the cost level
        prior = float(file_row[3]) # identify the prior
        action = file_row[7:] # identify the sequence of decisions
        # for each choice in the decision sequence, identify: 1) stop or sample 2) V(sample)-V(stop)
        for choice in action:
            index = np.argmax(-(abs(p_grid - prior)))
            value = sample_stop(index, V)
            if choice == 'investigate_red':
                prior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                sampling = 1
            elif choice == 'investigate_blue':
                prior = prior/(1 - (1-prior)*accuracy2)
                sampling = 1
            elif choice == 'evidence_shown':
                prior = 1
            elif choice == 'accuse_red' or choice == 'accuse_blue':
                sampling = 0
            dict[sampling].append(value)    

# scatter plot for stopping and sampling
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.ones(len(dict[1])), marker='o')

# look at the values (V(sample)-V(stop)) in stopping and sampling
if False:
    np.unique(dict[0])
    np.unique(dict[1])

# calculate the probability of sampling versus V(sample)-V(stop), 
# each probability is calculated within interval of length 10
prob = []
v_diff = [-55,-45,-35,-25,-15,-5,5,15,25,35,45,55,65,75,85,95,105]
prob.append(sum(1 for i in dict[1] if -60 <=i <-50)/(sum(1 for i in dict[0] if -60 <=i <-50)+sum(1 for i in dict[1] if -60 <=i <-50)))
prob.append(sum(1 for i in dict[1] if -50 <=i <-40)/(sum(1 for i in dict[0] if -50 <=i <-40)+sum(1 for i in dict[1] if -50 <=i <-40)))
prob.append(sum(1 for i in dict[1] if -40 <=i <-30)/(sum(1 for i in dict[0] if -40 <=i <-30)+sum(1 for i in dict[1] if -40 <=i <-30)))
prob.append(sum(1 for i in dict[1] if -30 <=i <-20)/(sum(1 for i in dict[0] if -30 <=i <-20)+sum(1 for i in dict[1] if -30 <=i <-20)))
prob.append(sum(1 for i in dict[1] if -20 <=i <-10)/(sum(1 for i in dict[0] if -20 <=i <-10)+sum(1 for i in dict[1] if -20 <=i <-10)))
prob.append(sum(1 for i in dict[1] if -10 <=i <0)/(sum(1 for i in dict[0] if -10 <=i <0)+sum(1 for i in dict[1] if -10 <=i <0)))
prob.append(sum(1 for i in dict[1] if 0 <=i <10)/(sum(1 for i in dict[0] if 0 <=i <10)+sum(1 for i in dict[1] if 0 <=i <10)))
prob.append(sum(1 for i in dict[1] if 10 <=i <20)/(sum(1 for i in dict[0] if 10 <=i <20)+sum(1 for i in dict[1] if 10 <=i <20)))
prob.append(sum(1 for i in dict[1] if 20 <=i <30)/(sum(1 for i in dict[0] if 20 <=i <30)+sum(1 for i in dict[1] if 20 <=i <30)))
prob.append(sum(1 for i in dict[1] if 30 <=i <40)/(sum(1 for i in dict[0] if 30 <=i <40)+sum(1 for i in dict[1] if 30 <=i <40)))
prob.append(sum(1 for i in dict[1] if 40 <=i <50)/(sum(1 for i in dict[0] if 40 <=i <50)+sum(1 for i in dict[1] if 40 <=i <50)))
prob.append(sum(1 for i in dict[1] if 50 <=i <60)/(sum(1 for i in dict[0] if 50 <=i <60)+sum(1 for i in dict[1] if 50 <=i <60)))
prob.append(sum(1 for i in dict[1] if 60 <=i <70)/(sum(1 for i in dict[0] if 60 <=i <70)+sum(1 for i in dict[1] if 60 <=i <70)))
prob.append(sum(1 for i in dict[1] if 70 <=i <80)/(sum(1 for i in dict[0] if 70 <=i <80)+sum(1 for i in dict[1] if 70 <=i <80)))
prob.append(sum(1 for i in dict[1] if 80 <=i <90)/(sum(1 for i in dict[0] if 80 <=i <90)+sum(1 for i in dict[1] if 80 <=i <90)))
prob.append(sum(1 for i in dict[1] if 90 <=i <100)/(sum(1 for i in dict[0] if 90 <=i <100)+sum(1 for i in dict[1] if 90 <=i <100)))
prob.append(sum(1 for i in dict[1] if 100 <=i <110)/(sum(1 for i in dict[0] if 100 <=i <110)+sum(1 for i in dict[1] if 100 <=i <110)))

# plot of probability of sampling versus V(sample)-V(stop)
if False:
    plt.plot(v_diff, prob, marker='o')




########################## for conservative case: 0.8-0.8-0.04-0 ##########################
      
# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)            
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('0.8-0.8-0.04-0.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader) # skip the first line
    for file_row in filereader: # read each row
        c = float(file_row[2]) # identify the cost
        V = vars()[''.join(['V',str(int(c))])] # identify the value function for 
        prior = float(file_row[3]) # identify the prior for this simulation
        action = file_row[7:] # identify the sequence of choices for this simulation
        for choice in action:
            index = np.argmax(-(abs(p_grid - prior)))
            value = sample_stop(index, V)
            if choice == 'investigate_red':
                prior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                sampling = 1
            elif choice == 'investigate_blue':
                prior = prior/(1 - (1-prior)*accuracy2)
                sampling = 1
            elif choice == 'evidence_shown':
                prior = 1
            elif choice == 'accuse_red' or choice == 'accuse_blue':
                sampling = 0
            dict[sampling].append(value) 
            
# scatter plot for stopping and sampling
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.ones(len(dict[1])), marker='o')

# look at the values (V(sample)-V(stop)) in stopping and sampling
if False:
    np.unique(dict[0])
    np.unique(dict[1])

# calculate the probability of sampling versus V(sample)-V(stop)
prob = []
v_diff = [-55,-45,-35,-25,-15,-5,5,15,25,35,45,55,65,75,85,95,105]
prob.append(sum(1 for i in dict[1] if -60 <=i <-50)/(sum(1 for i in dict[0] if -60 <=i <-50)+sum(1 for i in dict[1] if -60 <=i <-50)))
prob.append(sum(1 for i in dict[1] if -50 <=i <-40)/(sum(1 for i in dict[0] if -50 <=i <-40)+sum(1 for i in dict[1] if -50 <=i <-40)))
prob.append(sum(1 for i in dict[1] if -40 <=i <-30)/(sum(1 for i in dict[0] if -40 <=i <-30)+sum(1 for i in dict[1] if -40 <=i <-30)))
prob.append(sum(1 for i in dict[1] if -30 <=i <-20)/(sum(1 for i in dict[0] if -30 <=i <-20)+sum(1 for i in dict[1] if -30 <=i <-20)))
prob.append(sum(1 for i in dict[1] if -20 <=i <-10)/(sum(1 for i in dict[0] if -20 <=i <-10)+sum(1 for i in dict[1] if -20 <=i <-10)))
prob.append(sum(1 for i in dict[1] if -10 <=i <0)/(sum(1 for i in dict[0] if -10 <=i <0)+sum(1 for i in dict[1] if -10 <=i <0)))
prob.append(sum(1 for i in dict[1] if 0 <=i <10)/(sum(1 for i in dict[0] if 0 <=i <10)+sum(1 for i in dict[1] if 0 <=i <10)))
prob.append(sum(1 for i in dict[1] if 10 <=i <20)/(sum(1 for i in dict[0] if 10 <=i <20)+sum(1 for i in dict[1] if 10 <=i <20)))
prob.append(sum(1 for i in dict[1] if 20 <=i <30)/(sum(1 for i in dict[0] if 20 <=i <30)+sum(1 for i in dict[1] if 20 <=i <30)))
prob.append(sum(1 for i in dict[1] if 30 <=i <40)/(sum(1 for i in dict[0] if 30 <=i <40)+sum(1 for i in dict[1] if 30 <=i <40)))
prob.append(sum(1 for i in dict[1] if 40 <=i <50)/(sum(1 for i in dict[0] if 40 <=i <50)+sum(1 for i in dict[1] if 40 <=i <50)))
prob.append(sum(1 for i in dict[1] if 50 <=i <60)/(sum(1 for i in dict[0] if 50 <=i <60)+sum(1 for i in dict[1] if 50 <=i <60)))
prob.append(sum(1 for i in dict[1] if 60 <=i <70)/(sum(1 for i in dict[0] if 60 <=i <70)+sum(1 for i in dict[1] if 60 <=i <70)))
prob.append(sum(1 for i in dict[1] if 70 <=i <80)/(sum(1 for i in dict[0] if 70 <=i <80)+sum(1 for i in dict[1] if 70 <=i <80)))
prob.append(sum(1 for i in dict[1] if 80 <=i <90)/(sum(1 for i in dict[0] if 80 <=i <90)+sum(1 for i in dict[1] if 80 <=i <90)))
prob.append(sum(1 for i in dict[1] if 90 <=i <100)/(sum(1 for i in dict[0] if 90 <=i <100)+sum(1 for i in dict[1] if 90 <=i <100)))
prob.append(sum(1 for i in dict[1] if 100 <=i <110)/(sum(1 for i in dict[0] if 100 <=i <110)+sum(1 for i in dict[1] if 100 <=i <110)))

# plot of probability of sampling versus V(sample)-V(stop)
if False:
    plt.plot(v_diff, prob, marker='o')




########################## for noisy with stop cost case: 1-1-0.04-47 ##########################

# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('1-1-0.04-47.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader) # skip the first line
    for file_row in filereader: # read each row
        c = float(file_row[2]) # identify the cost
        V = vars()[''.join(['V',str(int(c))])] # identify the value function
        prior = float(file_row[3]) # identify the prior
        action = file_row[7:] # identify the sequence of decisions
        for choice in action:
            index = np.argmax(-(abs(p_grid - prior)))
            value = sample_stop(index, V)
            if choice == 'investigate_red':
                prior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                sampling = 1
            elif choice == 'investigate_blue':
                prior = prior/(1 - (1-prior)*accuracy2)
                sampling = 1
            elif choice == 'evidence_shown':
                prior = 1
            elif choice == 'accuse_red' or choice == 'accuse_blue':
                sampling = 0
            dict[sampling].append(value)   
            
# scatter plot for stop and sample
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.ones(len(dict[1])), marker='o')

# look at the values (V(sample)-V(stop)) in stopping and sampling
if False:
    np.unique(dict[0])
    np.unique(dict[1])

# calculate the probability of sampling versus V(sample)-V(stop)
prob = []
v_diff = [-55,-45,-35,-25,-15,-5,5,15,25,35,45,55,65,75,85,95,105]
prob.append(sum(1 for i in dict[1] if -60 <=i <-50)/(sum(1 for i in dict[0] if -60 <=i <-50)+sum(1 for i in dict[1] if -60 <=i <-50)))
prob.append(sum(1 for i in dict[1] if -50 <=i <-40)/(sum(1 for i in dict[0] if -50 <=i <-40)+sum(1 for i in dict[1] if -50 <=i <-40)))
prob.append(sum(1 for i in dict[1] if -40 <=i <-30)/(sum(1 for i in dict[0] if -40 <=i <-30)+sum(1 for i in dict[1] if -40 <=i <-30)))
prob.append(sum(1 for i in dict[1] if -30 <=i <-20)/(sum(1 for i in dict[0] if -30 <=i <-20)+sum(1 for i in dict[1] if -30 <=i <-20)))
prob.append(sum(1 for i in dict[1] if -20 <=i <-10)/(sum(1 for i in dict[0] if -20 <=i <-10)+sum(1 for i in dict[1] if -20 <=i <-10)))
prob.append(sum(1 for i in dict[1] if -10 <=i <0)/(sum(1 for i in dict[0] if -10 <=i <0)+sum(1 for i in dict[1] if -10 <=i <0)))
prob.append(sum(1 for i in dict[1] if 0 <=i <10)/(sum(1 for i in dict[0] if 0 <=i <10)+sum(1 for i in dict[1] if 0 <=i <10)))
prob.append(sum(1 for i in dict[1] if 10 <=i <20)/(sum(1 for i in dict[0] if 10 <=i <20)+sum(1 for i in dict[1] if 10 <=i <20)))
prob.append(sum(1 for i in dict[1] if 20 <=i <30)/(sum(1 for i in dict[0] if 20 <=i <30)+sum(1 for i in dict[1] if 20 <=i <30)))
prob.append(sum(1 for i in dict[1] if 30 <=i <40)/(sum(1 for i in dict[0] if 30 <=i <40)+sum(1 for i in dict[1] if 30 <=i <40)))
prob.append(sum(1 for i in dict[1] if 40 <=i <50)/(sum(1 for i in dict[0] if 40 <=i <50)+sum(1 for i in dict[1] if 40 <=i <50)))
prob.append(sum(1 for i in dict[1] if 50 <=i <60)/(sum(1 for i in dict[0] if 50 <=i <60)+sum(1 for i in dict[1] if 50 <=i <60)))
prob.append(sum(1 for i in dict[1] if 60 <=i <70)/(sum(1 for i in dict[0] if 60 <=i <70)+sum(1 for i in dict[1] if 60 <=i <70)))
prob.append(sum(1 for i in dict[1] if 70 <=i <80)/(sum(1 for i in dict[0] if 70 <=i <80)+sum(1 for i in dict[1] if 70 <=i <80)))
prob.append(sum(1 for i in dict[1] if 80 <=i <90)/(sum(1 for i in dict[0] if 80 <=i <90)+sum(1 for i in dict[1] if 80 <=i <90)))
prob.append(sum(1 for i in dict[1] if 90 <=i <100)/(sum(1 for i in dict[0] if 90 <=i <100)+sum(1 for i in dict[1] if 90 <=i <100)))
prob.append(sum(1 for i in dict[1] if 100 <=i <110)/(sum(1 for i in dict[0] if 100 <=i <110)+sum(1 for i in dict[1] if 100 <=i <110)))

# plot of probability of sampling versus V(sample)-V(stop)
if False:
    plt.plot(v_diff, prob, marker='o')




########################## for confirmatory case: 1.2-0.8-0.04-0 ##########################

# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('1.2-0.8-0.04-0.csv','r') as csvfile:
    filereader = csv.reader(csvfile, delimiter=',')
    next(filereader) # skip the first line
    for file_row in filereader: # read each row
        c = float(file_row[2]) # identify the cost
        V = vars()[''.join(['V',str(int(c))])] # identify the value function
        prior = float(file_row[3]) # identify the prior
        action = file_row[7:] # identify the sequence of decisions
        for choice in action:
            index = np.argmax(-(abs(p_grid - prior)))
            value = sample_stop(index, V)
            if choice == 'investigate_red':
                prior = prior*(1-accuracy1)/(1 - prior*accuracy1)
                sampling = 1
            elif choice == 'investigate_blue':
                prior = prior/(1 - (1-prior)*accuracy2)
                sampling = 1
            elif choice == 'evidence_shown':
                prior = 1
            elif choice == 'accuse_red' or choice == 'accuse_blue':
                sampling = 0
            dict[sampling].append(value) 

# scatter plot for stop and sample
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.zeros(len(dict[1])), marker='o')

# look at the values (V(sample)-V(stop)) in stopping and sampling
if False:
    np.unique(dict[0])
    np.unique(dict[1])

# calculate the probability of sampling versus V(sample)-V(stop)
prob = []
v_diff = [-55,-45,-35,-25,-15,-5,5,15,25,35,45,55,65,75,85,95,105,125,135,165,175,215,345]
prob.append(sum(1 for i in dict[1] if -60 <=i <-50)/(sum(1 for i in dict[0] if -60 <=i <-50)+sum(1 for i in dict[1] if -60 <=i <-50)))
prob.append(sum(1 for i in dict[1] if -50 <=i <-40)/(sum(1 for i in dict[0] if -50 <=i <-40)+sum(1 for i in dict[1] if -50 <=i <-40)))
prob.append(sum(1 for i in dict[1] if -40 <=i <-30)/(sum(1 for i in dict[0] if -40 <=i <-30)+sum(1 for i in dict[1] if -40 <=i <-30)))
prob.append(sum(1 for i in dict[1] if -30 <=i <-20)/(sum(1 for i in dict[0] if -30 <=i <-20)+sum(1 for i in dict[1] if -30 <=i <-20)))
prob.append(sum(1 for i in dict[1] if -20 <=i <-10)/(sum(1 for i in dict[0] if -20 <=i <-10)+sum(1 for i in dict[1] if -20 <=i <-10)))
prob.append(sum(1 for i in dict[1] if -10 <=i <0)/(sum(1 for i in dict[0] if -10 <=i <0)+sum(1 for i in dict[1] if -10 <=i <0)))
prob.append(sum(1 for i in dict[1] if 0 <=i <10)/(sum(1 for i in dict[0] if 0 <=i <10)+sum(1 for i in dict[1] if 0 <=i <10)))
prob.append(sum(1 for i in dict[1] if 10 <=i <20)/(sum(1 for i in dict[0] if 10 <=i <20)+sum(1 for i in dict[1] if 10 <=i <20)))
prob.append(sum(1 for i in dict[1] if 20 <=i <30)/(sum(1 for i in dict[0] if 20 <=i <30)+sum(1 for i in dict[1] if 20 <=i <30)))
prob.append(sum(1 for i in dict[1] if 30 <=i <40)/(sum(1 for i in dict[0] if 30 <=i <40)+sum(1 for i in dict[1] if 30 <=i <40)))
prob.append(sum(1 for i in dict[1] if 40 <=i <50)/(sum(1 for i in dict[0] if 40 <=i <50)+sum(1 for i in dict[1] if 40 <=i <50)))
prob.append(sum(1 for i in dict[1] if 50 <=i <60)/(sum(1 for i in dict[0] if 50 <=i <60)+sum(1 for i in dict[1] if 50 <=i <60)))
prob.append(sum(1 for i in dict[1] if 60 <=i <70)/(sum(1 for i in dict[0] if 60 <=i <70)+sum(1 for i in dict[1] if 60 <=i <70)))
prob.append(sum(1 for i in dict[1] if 70 <=i <80)/(sum(1 for i in dict[0] if 70 <=i <80)+sum(1 for i in dict[1] if 70 <=i <80)))
prob.append(sum(1 for i in dict[1] if 80 <=i <90)/(sum(1 for i in dict[0] if 80 <=i <90)+sum(1 for i in dict[1] if 80 <=i <90)))
prob.append(sum(1 for i in dict[1] if 90 <=i <100)/(sum(1 for i in dict[0] if 90 <=i <100)+sum(1 for i in dict[1] if 90 <=i <100)))
prob.append(sum(1 for i in dict[1] if 100 <=i <110)/(sum(1 for i in dict[0] if 100 <=i <110)+sum(1 for i in dict[1] if 100 <=i <110)))
prob.append(sum(1 for i in dict[1] if 120 <=i <130)/(sum(1 for i in dict[0] if 120 <=i <130)+sum(1 for i in dict[1] if 120 <=i <130)))
prob.append(sum(1 for i in dict[1] if 130 <=i <140)/(sum(1 for i in dict[0] if 130 <=i <140)+sum(1 for i in dict[1] if 130 <=i <140)))
prob.append(sum(1 for i in dict[1] if 160 <=i <170)/(sum(1 for i in dict[0] if 160 <=i <170)+sum(1 for i in dict[1] if 160 <=i <170)))
prob.append(sum(1 for i in dict[1] if 170 <=i <180)/(sum(1 for i in dict[0] if 170 <=i <180)+sum(1 for i in dict[1] if 170 <=i <180)))
prob.append(sum(1 for i in dict[1] if 210 <=i <220)/(sum(1 for i in dict[0] if 210 <=i <220)+sum(1 for i in dict[1] if 210 <=i <220)))
prob.append(sum(1 for i in dict[1] if 340 <=i <350)/(sum(1 for i in dict[0] if 340 <=i <350)+sum(1 for i in dict[1] if 340 <=i <350)))

# plot of probability of sampling versus V(sample)-V(stop)
if False:
    plt.plot(v_diff, prob, marker='o')




############################## for experimental data ##############################

# initiate a dictionary with keys: 0 (stop) and 1 (sample); values are V(sample)-V(stop)
dict = {0:[],1:[]}
accuracy1 = 0.25
accuracy2 = 0.25
p_grid = np.linspace(0,1,1001,endpoint=True)
with open('Bayes Results.csv','r') as f:
    file = [row for row in csv.reader(f.read().splitlines())]
file = file[26:51] # select data for the second experiment
for file_row in file: # read each row
    c = float(file_row[2]) # identify the cost
    V = vars()[''.join(['V',str(int(c))])] # identify the value function
    prior = float(file_row[3]) # identify the prior
    action = file_row[7:69] # identify the sequence of decisions
    evidence_shown = file_row[192] # identify if evidence is shown finally
    if evidence_shown == '0': # evidence not shown
        evidence_shown = False
    else: # evidence shown
        evidence_shown = True
    for choice in action: # for each choice in the sequence
        index = np.argmax(-(abs(p_grid - prior)))
        value = sample_stop(index, V)
        if choice == 'investigate_red':
            prior = prior*(1-accuracy1)/(1 - prior*accuracy1) # update prior
            dict[1].append(value) # sampling
        elif choice == 'investigate_blue':
            prior = prior/(1 - (1-prior)*accuracy2) # update prior
            dict[1].append(value) # sampling
        elif choice == 'accuse_red' or choice == 'accuse_blue':
            if evidence_shown == True: # if 'evidence_shown', updated prior = 1
                value = sample_stop(1000, V)
            dict[0].append(value)           
        elif choice == 'advance_to_next_trial': # done with the trial
            break 

# scatter plot for stopping and sampling
if False:
    plt.scatter(dict[0], np.zeros(len(dict[0])), marker='o')
    plt.scatter(dict[1], np.ones(len(dict[1])), marker='o')

# calculate the probability of sampling versus V(sample)-V(stop)
np.unique(dict[0])
np.unique(dict[1])

# calculate the probability of sampling versus V(sample)-V(stop)
prob = []
v_diff = [-50,-30,-10,10,30,50,90,150]
prob.append(sum(1 for i in dict[1] if -60 <i <=-40)/(sum(1 for i in dict[0] if -60 <i <=-40)+sum(1 for i in dict[1] if -60 <i <=-40)))
prob.append(sum(1 for i in dict[1] if -40 <i <=-20)/(sum(1 for i in dict[0] if -40 <i <=-20)+sum(1 for i in dict[1] if -40 <i <=-20)))
prob.append(sum(1 for i in dict[1] if -20 <i <=0)/(sum(1 for i in dict[0] if -20 <i <=0)+sum(1 for i in dict[1] if -20 <i <=0)))
prob.append(sum(1 for i in dict[1] if 0 <i <=20)/(sum(1 for i in dict[0] if 0 <i <=20)+sum(1 for i in dict[1] if 0 <i <=20)))
prob.append(sum(1 for i in dict[1] if 20 <i <=40)/(sum(1 for i in dict[0] if 20 <i <=40)+sum(1 for i in dict[1] if 20 <i <=40)))
prob.append(sum(1 for i in dict[1] if 40 <i <=60)/(sum(1 for i in dict[0] if 40 <i <=60)+sum(1 for i in dict[1] if 40 <i <=60)))
prob.append(sum(1 for i in dict[1] if 80 <i <=100)/(sum(1 for i in dict[0] if 80 <i <=100)+sum(1 for i in dict[1] if 80 <i <=100)))
prob.append(sum(1 for i in dict[1] if 140 <i <=160)/(sum(1 for i in dict[0] if 140 <i <=160)+sum(1 for i in dict[1] if 140 <i <=160)))

# plot of probability of sampling versus V(sample)-V(stop)
if False:
    plt.plot(v_diff, prob, marker='o')

