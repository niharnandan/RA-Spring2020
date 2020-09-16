% Detective Bayes optimal strategy
% Dynamic setting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Define cost and prior values to show

cost_vector=[5 10 20 40 80];
p_start = 0.1:0.2:0.9;

n_rounds_conditions = 100;

% store the information here
trials_summary_table = [];
% 1 - prior
% 2 - cost
% 3 - progressive number
% 4 - round ID - each round is an action
% 5 - action type 0=investigate, 1=accuse
% 6 - suspect  [1=blue]
% 7 - count red samples
% 8 - count blue samples
% 9 - evidence found (1=yes, 0=no)
% 10 - posterior
% 11 - true guilty suspect
% 12 - suspect accused [1=blue]
% 13 - correct answer (1=yes, 0=no)
% 14 - trial payoff

% DEFINE HERE USEFUL PARAMETERS
alpha_1=1; % coefficient for conservatism (update in the direction of the most likely option)
alpha_2=1; % coefficient for conservatism (update in the direction of the least likely option)
stop_cost=200; % additional (psychological) cost for stopping if posterior is not sure
sample_diff=0.01; % maximum difference that makes two sample actions indifferent

for i_cost=1:length(cost_vector)
    
    % Parameters of the problem
    %p = 0.6;            % prior probability that the state is 1
    accuracy1 = 0.25;   % poisson signal (prob of 1 conditional on searching state 1 - correct)
    accuracy2 = 0.25;   % poisson signal (prob of 1 conditional on searching state 2 - correct)
    cost1 = cost_vector(i_cost);         % cost of collecting sample 1
    cost2 = cost_vector(i_cost);         % cost of collecting sample 2
    reward= 1000;       % reward for matching the state


    % Grid of probabilities
    l_p  = 0;
    h_p  = 1;
    sGrid = 1001;       % size of the grid
    pGrid = linspace(l_p,h_p,sGrid);   % value indicate prob(state 1)

    % Matrix of transition of probabilities
    t1  = zeros(sGrid, sGrid);
    t2  = zeros(sGrid, sGrid);

    for i_prob = 1: sGrid

        p=pGrid(i_prob);

        % if sample 1
        prob_reveal=p*accuracy1;
        posterior=p*(1-accuracy1)/(1-p*accuracy1);
        if (posterior>p && p>=0.5) || (posterior<p && p<=0.5)
            posterior=alpha_1*posterior+(1-alpha_1)*p;
        else
            posterior=alpha_2*posterior+(1-alpha_2)*p;            
        end
        [~,nosignal] = min(abs(pGrid-posterior));
        t1(i_prob,sGrid)=prob_reveal;
        t1(i_prob,nosignal)=1-prob_reveal;
        if sGrid==nosignal
                t1(i_prob,nosignal)=1;
        end

        % if sample 2
        prob_reveal=(1-p)*accuracy2;
        posterior=p/(1-(1-p)*accuracy2);    
        if (posterior>p && p>=0.5) || (posterior<p && p<=0.5)
            posterior=alpha_1*posterior+(1-alpha_1)*p;
        else
            posterior=alpha_2*posterior+(1-alpha_2)*p;            
        end
        [~,nosignal] = min(abs(pGrid-posterior));
        t2(i_prob,sGrid)=prob_reveal;
        t2(i_prob,nosignal)=1-prob_reveal;
        if sGrid==nosignal
                t2(i_prob,nosignal)=1;
        end

    end

    % Value Function
    StopValue = reward*max([pGrid; 1-pGrid]);
    StopValue(2:end-1)=StopValue(2:end-1)-stop_cost;

    % Initial Value
    initial = zeros(1,sGrid);

    % Error (to stop convergence)
    error = 0.00000005;

    % Convergence to the optimal strategy
    limit=1000000;
    diff=1;
    i_count=1;
    while diff>error

        V_choose=StopValue; %converge to stop value
        V_sample1=initial*t1'-cost1;
        V_sample2=initial*t2'-cost2;
        V=max([V_choose;V_sample1;V_sample2]);

        diff =  max(max(abs(V-initial)));
        i_count=i_count+1;
        if i_count>limit
            break
        end  
        initial=V;
    end

    % Define the optimal strategy in each point

    Action_Stop = V_choose==initial;
    Action_Sample1 = V_sample1==initial;
    Action_Sample2 = V_sample2==initial;
    
    
for i_prior=1:length(p_start)
    
    prior = p_start(i_prior);
    cost = cost_vector(i_cost);
    
    % do many rounds
    for i_round = 1:n_rounds_conditions
    
        % store info in trial round table
        trial_summary_round=[];
        flag_stop = 0;
        i_action = 0;
        count_red_samples = 0;
        count_blue_samples = 0;
        evidence_found = 0;
        posterior = prior;
        suspect_accused=0;
        correct_answer=0;
        trial_payoff=0;
            
        % generate true guilty
        true_guilty_suspect=0;
        if rand>prior
            true_guilty_suspect=1;
        end
        % initial beliefs
        current_prob = prior;
        current_prob = round(current_prob,3);
        
        while flag_stop==0
            i_action=i_action+1;
            % choose the best action
            % stop
            if Action_Stop(current_prob*1000+1)==1
                  action_type=1;
                  % choose who to accuse
                  if current_prob>0.5
                      suspect = 0;
                      suspect_accused = 0;
                  else
                      suspect = 1;
                      suspect_accused = 1;
                  end
                  if suspect_accused == true_guilty_suspect
                      correct_answer=1;
                  else
                      correct_answer=0;                      
                  end
                  posterior = current_prob;
                  flag_stop=1;
                  trial_payoff = 1000*correct_answer+500-(count_red_samples+count_blue_samples)*cost;

            else
            % sample
                action_type=0;
                % red
                if Action_Sample1(current_prob*1000+1)==1
                    suspect = 0;
                    count_red_samples=count_red_samples+1;
                     
                    if (true_guilty_suspect==0 && rand<0.25)
                        posterior=1;
                        evidence_found=1;
                    else
                        p=current_prob;
                        posterior=p*(1-accuracy1)/(1-p+p*(1-accuracy1));
                    end

                % blue
                else
                    suspect = 1;
                    count_blue_samples=count_blue_samples+1;
                    
                    if (true_guilty_suspect==1 && rand<0.25)
                        posterior=0;
                        evidence_found=1;
                    else
                        q=current_prob;
                        p = 1-q;
                        posterior=p*(1-accuracy1)/(1-p+p*(1-accuracy1));
                        posterior=1-posterior;
                    end         
                    
                end
                current_prob = round(posterior,3);
            
            end   
            
            round_vector = [prior cost i_round i_action action_type suspect count_red_samples count_blue_samples...
                evidence_found posterior true_guilty_suspect suspect_accused correct_answer trial_payoff];
            trial_summary_round = [trial_summary_round; round_vector];
            
        end
        
% 1 - prior
% 2 - cost
% 3 - progressive number
% 4 - round ID - each round is an action
% 5 - action type 0=investigate, 1=accuse
% 6 - suspect  [1=blue]
% 7 - count red samples
% 8 - count blue samples
% 9 - evidence found (1=yes, 0=no)
% 10 - posterior
% 11 - true guilty suspect
% 12 - suspect accused [1=blue]
% 13 - correct answer (1=yes, 0=no)
% 14 - trial payoff        
        
        trials_summary_table = [trials_summary_table; trial_summary_round];
    
    end
end
    
    
end


%%

% SEPARATE ACCUSE AND INVESTIGATE
t2_accuse = trials_summary_table(trials_summary_table(:,5)==1,:);
t2_investigate =  trials_summary_table(trials_summary_table(:,5)==0,:);
% clean out the times in which the final evidence is already found
t2_accuse_clean = t2_accuse(t2_accuse(:,9)==0,:);
t2_investigate_clean = t2_investigate(t2_investigate(:,9)==0,:);



% percentage correct guesses
t2_perc_correct = mean(t2_accuse(:,13));

% percentage evidence found
t2_perc_evidence_found = mean(t2_accuse(:,9));

% round 1 only
select_rounds = t2_investigate;
select_rounds = select_rounds(select_rounds(:,4)==1,:);
select_rounds_low = select_rounds(select_rounds(:,10)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,6));
select_rounds_high = select_rounds(select_rounds(:,10)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,6));
t2_perc_confirmatory_round1 = mean([avg_rounds_low, avg_rounds_high]);

% all rounds
select_rounds = t2_investigate_clean;
select_rounds_low = select_rounds(select_rounds(:,10)<0.5,:);
avg_rounds_low = mean(select_rounds_low(:,6));
select_rounds_high = select_rounds(select_rounds(:,10)>0.5,:);
avg_rounds_high = 1-mean(select_rounds_high(:,6));
t2_perc_confirmatory_allrounds = mean([avg_rounds_low, avg_rounds_high]);

disp('Summary t2 Bayes')
summary_outcome_t2(3,1:4) = [t2_perc_correct, t2_perc_evidence_found, t2_perc_confirmatory_round1, t2_perc_confirmatory_allrounds]


% number of samples
t2_totsamples = t2_accuse(:,7)+t2_accuse(:,8);
t2_avg_samples = mean(t2_totsamples);

% score
t2_avg_score = mean(t2_accuse(:,14));
t2_avg_score = t2_avg_score*0.95;

summary_outcome_t2(3,5:6) = [t2_avg_samples t2_avg_score]
