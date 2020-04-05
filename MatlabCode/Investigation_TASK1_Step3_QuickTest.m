%% Investigation_TASK1_Step3_QuickTest

% vector of colors
color_red  = [1 0 0];
color_blue = [0 0 1];
n_colors = 5;
v_colors = [0:1/(n_colors-1):1]'.*color_red + [1:-1/(n_colors-1):0]'.*color_blue;

% input
open('t1_3')

% read relevant information
participant_ID = t1_3(:,1);
treatment_condition = t1_3(:,2);
number_rounds_available = t1_3(:,5);
prior_guilty_prob = t1_3(:,6);
correct_guilty = t1_3(:,7);
accused_guilty = t1_3(:,8);
correct_accused = t1_3(:,38);
evidence_round = t1_3(:,39);
evidence_found = evidence_round>0;


