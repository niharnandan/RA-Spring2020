% Detective Bayes optimal strategy
% Dynamic setting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
clc

%% Define cost and prior values to show

cost_vector=[5 10 20 40 80];
showGrid = [101 301 501 701 901];

figure(1)
title('Optimal Strategy Task 3','Interpreter','Latex')
hold on
for i_level=0.1:0.2:0.9
   plot([i_level i_level],[0 6],':k') 
end


for i_cost=1:length(cost_vector)
    
    %% Parameters of the problem
    %p = 0.6;            % prior probability that the state is 1
    accuracy1 = 0.25;   % poisson signal (prob of 1 conditional on searching state 1 - correct)
    accuracy2 = 0.25;   % poisson signal (prob of 1 conditional on searching state 2 - correct)
    cost1 = cost_vector(i_cost)*0.9;         % cost of collecting sample 1
    cost2 = cost_vector(i_cost)*1.1;         % cost of collecting sample 2
    reward= 1000;       % reward for matching the state


    %% Grid of probabilities
    l_p  = 0;
    h_p  = 1;
    sGrid = 1001;       % size of the grid
    pGrid = linspace(l_p,h_p,sGrid);   % value indicate prob(state 1)


    %% Matrix of transition of probabilities
    t1  = zeros(sGrid, sGrid);
    t2  = zeros(sGrid, sGrid);

    for i_prob = 1: sGrid

        p=pGrid(i_prob);

        % if sample 1
        prob_reveal=1-p*(1-accuracy1)-(1-p);
        posterior=p*(1-accuracy1)/(1-p+p*(1-accuracy1));    
        [~,nosignal] = min(abs(pGrid-posterior));
        t1(i_prob,sGrid)=prob_reveal;
        t1(i_prob,nosignal)=1-prob_reveal;
        if sGrid==nosignal
                t1(i_prob,nosignal)=1;
        end

        % if sample 2
        prob_reveal=1-(1-p)*(1-accuracy2)-p;
        posterior=(1-p)*(1-accuracy2)/(p+(1-p)*(1-accuracy2));    
        [~,nosignal] = min(abs(pGrid-posterior));
        t2(i_prob,sGrid)=prob_reveal;
        t2(i_prob,nosignal)=1-prob_reveal;
        if sGrid==nosignal
                t2(i_prob,nosignal)=1;
        end

    end


    %% Value Function
    StopValue = reward*max([pGrid; 1-pGrid]);


    %% Initial Value
    initial = zeros(1,sGrid);


    %% Error (to stop convergence)
    error = 0.00000005;


    %% Convergence to the optimal strategy
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


    %% Define the optimal strategy in each point

    Action_Stop = V_choose==initial;
    Action_Sample1 = V_sample1==initial;
    Action_Sample2 = V_sample2==initial;
    
    
    %% Display optimal strategy with scatter plot
    scatter(pGrid,i_cost*Action_Stop,'k')
    scatter(pGrid,i_cost*Action_Sample1,'r')
    scatter(pGrid,i_cost*Action_Sample2,'b')

    
    
end

scatter(pGrid,0*Action_Sample2,'white')
xlabel('Prior probability','Interpreter','Latex')
ylabel('Cost per sample','Interpreter','Latex')
axis([0 1 0.5 5.5])
set(gcf, 'Position',  [0, 0, 300, 230])

