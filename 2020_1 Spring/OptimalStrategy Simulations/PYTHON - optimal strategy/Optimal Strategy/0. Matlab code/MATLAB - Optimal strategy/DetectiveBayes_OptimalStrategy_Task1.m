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
