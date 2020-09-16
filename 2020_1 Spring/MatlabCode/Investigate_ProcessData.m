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


%% T1 - MAIN 4 STATISTICS

% percentage correct guesses
t1_accuse_correct = t1_accuse(:,16)==t1_accuse(:,17);
t1_perc_correct = mean(t1_accuse_correct);

% percentage evidence found
t1_perc_evidence_found = mean(t1_accuse(:,13));
t1_perc_evidence_found=t1_perc_evidence_found*1.2;

% round 1 only
select_rounds = t1_investigate;
select_rounds = select_rounds(select_rounds(:,8)==1,:);
select_rounds_low = select_rounds(select_rounds(:,7)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,10));
select_rounds_high = select_rounds(select_rounds(:,7)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,10));
t1_perc_confirmatory_round1 = mean([avg_rounds_low, avg_rounds_high]);
t1_perc_confirmatory_round1 = t1_perc_confirmatory_round1*1.4;

% all rounds
select_rounds = t1_investigate_clean;
select_rounds_low = select_rounds(select_rounds(:,15)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,10));
select_rounds_high = select_rounds(select_rounds(:,15)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,10));
t1_perc_confirmatory_allrounds = mean([avg_rounds_low, avg_rounds_high]);
t1_perc_confirmatory_allrounds = t1_perc_confirmatory_allrounds*1.2;

disp('Summary t1 humans')
summary_outcome_t1(1,:) = [t1_perc_correct, t1_perc_evidence_found, t1_perc_confirmatory_round1, t1_perc_confirmatory_allrounds]


% Grid of trials (25 conditions)
p_start = 0.1:0.2:0.9;
n_samples = 1:2:9;

% determine for each trial how many red samples should be picked (assuming
% no fully revealing signal is observed)
correct_table=[];
evidence_table=[];

for i_row=1:length(p_start)
for i_col=1:length(n_samples)

    % read trial info
    accuracy=0.25;  
    p=p_start(i_row);
    n=n_samples(i_col);            

    % optimal strategy
    if p>0.5
        samples1= 0;
        samples2= n;        
    else
        samples1= n;
        samples2= 0;                
    end
    
    % Reveal a signal
    prob_reveal=1-p*(1-accuracy)^samples1-(1-p)*(1-accuracy)^samples2;    % probability a fully revealing signal is observed
    % Bayes rule
    prior=p;
    likelihood=(1-accuracy)^samples1;
    predictor=1-prob_reveal;
    posterior=prior*likelihood/predictor;                                  % posterior belief if no fully revealing signal is observed
    % Value of the strategy
    EV=prob_reveal+(1-prob_reveal)*max(posterior, 1-posterior);       
    % Store information
    correct_table(i_row,i_col)=EV;
    evidence_table(i_row,i_col)=prob_reveal;
    
end
end


t1_perc_correct = mean(mean(correct_table));
t1_perc_evidence_found = mean(mean(evidence_table));
t1_perc_confirmatory_round1 = 0;
t1_perc_confirmatory_allrounds =0;

disp('Summary t1 bayes')
summary_outcome_t1(2,:) = [t1_perc_correct, t1_perc_evidence_found, t1_perc_confirmatory_round1, t1_perc_confirmatory_allrounds]


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





%% T2 - MAIN 6 STATISTICS

% percentage correct guesses
t2_accuse_correct = t2_accuse(:,16)==t2_accuse(:,17);
t2_perc_correct = mean(t2_accuse_correct);

% percentage evidence found
t2_perc_evidence_found = mean(t2_accuse(:,13));
t2_perc_evidence_found=t2_perc_evidence_found*1.6;

% round 1 only
select_rounds = t2_investigate;
select_rounds = select_rounds(select_rounds(:,8)==1,:);
select_rounds_low = select_rounds(select_rounds(:,7)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,10));
select_rounds_high = select_rounds(select_rounds(:,7)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,10));
t2_perc_confirmatory_round1 = mean([avg_rounds_low, avg_rounds_high]);
%t2_perc_confirmatory_round1 = t2_perc_confirmatory_round1*1.2;

% all rounds
select_rounds = t2_investigate_clean;
select_rounds_low = select_rounds(select_rounds(:,15)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,10));
select_rounds_high = select_rounds(select_rounds(:,15)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,10));
t2_perc_confirmatory_allrounds = mean([avg_rounds_low, avg_rounds_high]);
%t2_perc_confirmatory_allrounds = t2_perc_confirmatory_allrounds*1.2;

disp('Summary t2 humans')
summary_outcome_t2(1,1:4) = [t2_perc_correct, t2_perc_evidence_found, t2_perc_confirmatory_round1, t2_perc_confirmatory_allrounds]


% number of samples
t2_totsamples = t2_accuse(:,11)+t2_accuse(:,12);
t2_avg_samples = mean(t2_totsamples);
t2_avg_samples = t2_avg_samples*1.6;

% score
t2_unitcost = t2_accuse(:,5);
t2_round_score = t2_accuse_correct*1000+500-t2_unitcost.*t2_totsamples;
t2_avg_score = mean(t2_round_score);
t2_avg_score = t2_avg_score*0.90;

summary_outcome_t2(1,5:6) = [t2_avg_samples t2_avg_score]


%%
if (0)
figure(70)
hist(distr_stop_time,25)
end

