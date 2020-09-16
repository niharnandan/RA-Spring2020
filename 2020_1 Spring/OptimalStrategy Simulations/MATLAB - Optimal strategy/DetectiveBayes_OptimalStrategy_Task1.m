%% Input variables

p=0.6;          % probability that the state is 1
accuracy=0.25;  % poisson signal (prob of 1 conditional on searching the right state)
n=9;            % number of available samples
table=[0:n]';   % prepare table for results - the first column is the number of samples from state 1

for i_line=1:n+1
    
    % Sampling strategy
    samples1= i_line-1;
    samples2= n-i_line+1; % wen p>0.5 you should only test state 2 (less likely)
    
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
    table(i_line,2:4)=[prob_reveal posterior EV];
end

disp('  Samples1 - P(reveal)-Posterior-   EV')
disp(table)

%% Grid of posteriors

p=0.6;          % probability that the state is 1
accuracy=0.25;  % poisson signal (prob of 1 conditional on searching the right state)
n=9;            % number of available samples
grid=[];

for i_row=1:n+1
for i_col=1:n+1

    % Sampling strategy
    samples1= i_row-1; % row: test state 1
    samples2= i_col-1; % col: test state 2
    
    % Reveal a signal
    prob_reveal=1-p*(1-accuracy)^samples1-(1-p)*(1-accuracy)^samples2;    % probability a fully revealing signal is observed
    % Bayes rule
    prior=p;
    likelihood=(1-accuracy)^samples1;
    predictor=1-prob_reveal;
    posterior=prior*likelihood/predictor;                                  % posterior belief if no fully revealing signal is observed
        
    % Store information
    grid(i_row,i_col)=posterior;
    
end
end

%% Determine optimal strategy for each condition

% Grid of trials (25 conditions)
p_start = 0.1:0.2:0.9;
n_samples = 1:2:9;

% determine for each trial how many red samples should be picked (assuming
% no fully revealing signal is observed)
optimal_table=[];

for i_row=1:length(p_start)
for i_col=1:length(n_samples)

    accuracy=0.25;  
    p=p_start(i_row);
    n=n_samples(i_col);            

    table=[0:n]';   
    for i_line=1:n+1

        % Sampling strategy
        samples1= i_line-1;
        samples2= n-i_line+1; % wen p>0.5 you should only test state 2 (less likely)
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
        table(i_line,2:4)=[prob_reveal posterior EV];
        
    end
    [~,best_row]=max(table(:,4));
    optimal_table(i_row,i_col)=table(best_row,1);
    
end
end

% the table indicates how many red samples should be observed (absolute
% value)
disp(optimal_table)

% and in relative value - note it is a bang-bang solution
disp(optimal_table./n_samples)




%% for each condition determine percentage correct and percentage evidence


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
summary_outcome_t1(1,:) = [t1_perc_correct, t1_perc_evidence_found, t1_perc_confirmatory_round1, t1_perc_confirmatory_allrounds]




