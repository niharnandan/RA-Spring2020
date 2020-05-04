%% Investigate_ProcessData

%% TASK 1

% SEPARATE ACCUSE AND INVESTIGATE
t1_accuse = t1_s4(t1_s4(:,9)==1,:);
t1_investigate = t1_s4(t1_s4(:,9)==0,:);
% clean out the times in which the final evidence is already found
t1_accuse_clean = t1_accuse(t1_accuse(:,13)==0,:);
t1_investigate_clean = t1_investigate(t1_investigate(:,13)==0,:);
% select only the times in which the final evidence is already found
t1_accuse_certain = t1_accuse(t1_accuse(:,13)==1,:);



%% TASK 2

% remove participant 7 (not reliable data)
t2_s4 = t2_s4(t2_s4(:,1)~=7,:);
% SEPARATE ACCUSE AND INVESTIGATE
t2_accuse = t2_s4(t2_s4(:,9)==1,:);
t2_investigate = t2_s4(t2_s4(:,9)==0,:);
% clean out the times in which the final evidence is already found
t2_accuse_clean = t2_accuse(t2_accuse(:,13)==0,:);
t2_investigate_clean = t2_investigate(t2_investigate(:,13)==0,:);
% select only the times in which the final evidence is already found
t2_accuse_certain = t2_accuse(t2_accuse(:,13)==1,:);


% number of rounds for stopping
distr_stop_time = t2_accuse(:,8);
distr_stop_time2 = distr_stop_time(distr_stop_time>1);
% beliefs when stopping
distr_stop_belief = t2_accuse(:,15);






