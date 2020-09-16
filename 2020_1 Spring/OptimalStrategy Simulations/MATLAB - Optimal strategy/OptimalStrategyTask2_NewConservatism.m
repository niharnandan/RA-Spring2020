% Detective Bayes optimal strategy
% Dynamic setting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
clc

alpha_1=1; % coefficient for conservatism (update in the direction of the most likely option)
alpha_2=1; % coefficient for conservatism (update in the direction of the least likely option)
stop_cost=100; % additional (psychological) cost for stopping if posterior is not sure
sample_diff=0.01; % maximum difference that makes two sample actions indifferent

figure(100)
FIGURE_PDF_NAME = 'Baseline 1-1-100';             % name the file

%% Define cost and prior values to show

%cost_vector=[40 50 60 70 80]; % this is helpful to check high levels
cost_vector=[5 5*sqrt(2) 10 10*sqrt(2) 20 20*sqrt(2) 40 40*sqrt(2) 80];
showGrid = [101 301 501 701 901];

title('Optimal Strategy Task 2','Interpreter','Latex')
hold on

for i_cost=1:length(cost_vector)
    
    %% Parameters of the problem
    %p = 0.6;            % prior probability that the state is 1
    accuracy1 = 0.25;   % poisson signal (prob of 1 conditional on searching state 1 - correct)
    accuracy2 = 0.25;   % poisson signal (prob of 1 conditional on searching state 2 - correct)
    cost1 = cost_vector(i_cost);         % cost of collecting sample 1
    cost2 = cost_vector(i_cost);         % cost of collecting sample 2
    reward= 1000;       % reward for matching the state


    %% Grid of probabilities
    l_p  = 0;
    h_p  = 1;
    sGrid = 10001;       % size of the grid
    pGrid = linspace(l_p,h_p,sGrid);   % value indicate prob(state 1)


    %% Matrix of transition of probabilities
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


    %% Value Function
    StopValue = reward*max([pGrid; 1-pGrid]);
    StopValue(2:end-1)=StopValue(2:end-1)-stop_cost;


    %% Initial Value
    initial = zeros(1,sGrid);


    %% Error (to stop convergence)
    error = 0.0005;


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
    
    test1 = Action_Sample1+Action_Sample2>0;
    test2 = abs(V_sample1-V_sample2)<sample_diff;
    Action_Sample_Indiff = (test1 + test2 == 2);
    
    
    %% Display optimal strategy with scatter plot
    scatterplotsize=15;
    scatter(pGrid,i_cost*Action_Stop,scatterplotsize,'k','filled')
    scatter(pGrid,i_cost*Action_Sample1,scatterplotsize,'r','filled')
    scatter(pGrid,i_cost*Action_Sample2,scatterplotsize,'b','filled')
    scatter(pGrid,i_cost*Action_Sample_Indiff,scatterplotsize,'w','filled')

    
    
end

for i_level=0.1:0.2:0.9
   plot([i_level i_level],[0 10],':k') 
end

scatter(pGrid,0*Action_Sample2,'white')
xlabel('Prior probability','Interpreter','Latex')
ylabel('Cost per sample','Interpreter','Latex')
axis([0 1 0.5 9.5])
set(gcf, 'Position',  [0, 0, 300, 230])
fig=gcf;                                    % assign figure
set(fig,'PaperSize',[10 10]);               %set the paper size
print(fig,FIGURE_PDF_NAME,'-dpdf')          % then print it


