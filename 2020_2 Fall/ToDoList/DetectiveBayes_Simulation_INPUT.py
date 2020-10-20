## DetectiveBayes_Simulation_INPUT
# This script contains the input information to run the simulation

## PARAMETERS OF THE DATASET
cost = [5,10,20,40,80] 			# cost per investigation
prior = [0.1,0.3,0.5,0.7,0.9] 	# prior probability of 1 guilty
n_datasets = 100				# number of repetitions for the block of questions

# PARAMETERS OF THE TASK (ALWAYS IDENTICAL)
accuracy1 = 0.25		# chance of finding 0 guilty by investigating 0
accuracy2 = 0.25		# chance of finding 0 guilty by investigating 1
reward = 1000 			# initial reward for guessing the correct state
trial = 60 				# maximum number of investigations

# PARAMETERS OF THE SIMULATED BEHAVIOR
alpha_1 = 1				# default=1		# relative update after a signal (consistent with prior)
alpha_2 = 1				# default=1		# relative update after a signal (at odd with prior)
stop_cost = 0			# default=0		# cognitive cost for stopping without certainty
k = 2					# default=2 for precise answer, or 0.4 for noisy answer		# coefficient of precision 

