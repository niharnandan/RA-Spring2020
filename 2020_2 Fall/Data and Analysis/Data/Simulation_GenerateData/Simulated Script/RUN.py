## IMPORT PACKAGES
import os
import shutil

print('Currently running RUN')

##############################################################################

## INPUT PARAMETERS - CAN RUN SIMULATIONS FOR SEVERAL CONDITIONS
r_alpha_1 = [1,0.8]     # default=1		# relative update after a signal (consistent with prior)
r_alpha_2 = [1,0.8]     # default=1		# relative update after a signal (at odd with prior)
r_stop_cost  = [0,0]    # default=0		# cognitive cost for stopping without certainty
#r_file_name = ['Optimal','Conservative_08'] # names for the files

## PARAMETER - FIXED (do not change across simulations)
#r_lambda_action = 2        # accuracy in the action choice (accuse vs investigate)
#r_lambda_investigate = 2   # accuracy in investigation choices
#r_lambda_accuse = 2        # accuracy in accusation choices
r_number = 1001             # grid size - number in value function
#n_datasets = 100           # number of repetitions for the block of questions

## PARAMETER - PROBLEM (do not change this part)
r_accuracy1 = 0.25                  # chance of finding 0 guilty by investigating 0
r_accuracy2 = 0.25                  # chance of finding 1 guilty by investigating 1
#r_prior_vector = [0.1,0.3,0.5,0.7,0.9]         # conditions: prior belief
#r_cost_vector = [5,10,20,40,80]                # conditions: cost per investigation
r_cost_vector = [[5,10,20,40,80]]
r_cost_vector = list(map(str,r_cost_vector))    # cost_vector, cost levels for investigation 
r_reward = 1000                     # reward for getting the right state
r_no_files = len(r_alpha_1)         # Total Number of files (conditions for simulations)
#max_investigate = 60               # maximum number of investigation rounds allowed


##############################################################################

## SAVE RAW DATA IN THIS FOLDER
data_folder = "../Simulated_Data/"

## RUN ACROSS ALL THE CONDITIONS
for iterate in range(r_no_files):
    
    ## SAVE THE PARAMETERS IN VALUES.TXT
	file = open("values.txt", "w")
	file.write(str(r_alpha_1[iterate]))
	file.write('\n')
	file.write(str(r_alpha_2[iterate]))
	file.write('\n')
	file.write(str(r_accuracy1))
	file.write('\n')
	file.write(str(r_accuracy2))
	file.write('\n')
	file.write(str(r_cost_vector[0].strip('[]').replace(' ','')))
#	file.write(str(r_cost_vector))
	file.write('\n')
	file.write(str(r_stop_cost[iterate]))
	file.write('\n')
	file.write(str(r_reward))
	file.write('\n')
	file.write(str(r_number))
	file.write('\n')
	file.write(str(r_no_files))
    
    # ADD THE OTHER INFORMATION, REORDER THE CURRENT INFORMATION TO BE IN THE ORDER ABOVE
    
	file.close()
    
    ## RUN THE CODE - CALCULATE THE POLICY FUNCTION GIVEN THE PARAMETERS
	exec(open('./value function.py').read())

    ## RUN THE CODE - SIMULATE DATASET GIVEN THE OPTIMAL POLICY
	exec(open('./data simulation.py').read())
    
    ## SAVE THE RAW FILES
	if not os.path.exists('simulation results '+chr(iterate+65)+'.csv'):	os.rename('simulation results.csv','simulation results '+chr(iterate+65)+'.csv')
	shutil.move('./simulation results '+chr(iterate+65)+'.csv', data_folder+'simulation results '+chr(iterate+65)+'.csv')


##############################################################################

## CLEAN THE DATASET (STEPS 2,3,4)
exec(open('./Step2.py').read())
exec(open('./Step4.py').read())

