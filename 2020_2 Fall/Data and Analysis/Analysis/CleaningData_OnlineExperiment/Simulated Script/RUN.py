import os
import shutil

r_alpha_1 = [1,2] # r_alpha_1, update in the direction of more likely
r_alpha_2 = [1,1] # alpha_2, update in the direction of less likely
r_accuracy1 = [0.25,0.25] # accuracy1, prob of reveal for 1
r_accuracy2 = [0.25,0.25] # accuracy2, prob of reveal for 2
r_cost_vector = [[5,10,20,40,80],[5,10,20,40,80]]
r_cost_vector = list(map(str,r_cost_vector)) # cost_vector, cost levels for investigation 
r_stop_cost  = [0,0] # stop_cost, stop cost
r_reward = [1000,1000] # reward, reward for getting the right state
r_number = [1001,1001] # number in value function
r_no_files = len(r_alpha_1) # Total Number of files
data_folder = "../Simulated_Data/"

for iterate in range(r_no_files):
	file = open("values.txt", "w")
	file.write(str(r_alpha_1[iterate]))
	file.write('\n')
	file.write(str(r_alpha_2[iterate]))
	file.write('\n')
	file.write(str(r_accuracy1[iterate]))
	file.write('\n')
	file.write(str(r_accuracy2[iterate]))
	file.write('\n')
	file.write(str(r_cost_vector[iterate].strip('[]').replace(' ','')))
	file.write('\n')
	file.write(str(r_stop_cost[iterate]))
	file.write('\n')
	file.write(str(r_reward[iterate]))
	file.write('\n')
	file.write(str(r_number[iterate]))
	file.write('\n')
	file.write(str(r_no_files))
	file.close()
	exec(open('./value function.py').read())
	exec(open('./data simulation.py').read())
	if not os.path.exists('simulation results '+chr(iterate+65)+'.csv'):	os.rename('simulation results.csv','simulation results '+chr(iterate+65)+'.csv')
	shutil.move('./simulation results '+chr(iterate+65)+'.csv', data_folder+'simulation results '+chr(iterate+65)+'.csv')

exec(open('./Step2.py').read())

exec(open('./Step3.py').read())

exec(open('./Step4.py').read())