% Detective Bayes optimal strategy
% Dynamic setting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear all;
close all;
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% cd('/Users/silvioravaioli/Desktop')

%% Parameters of the problem
%p = 0.6;            % prior probability that the state is 1
accuracy1 = 0.25;   % poisson signal (prob of 1 conditional on searching state 1 - correct)
accuracy2 = 0.25;   % poisson signal (prob of 1 conditional on searching state 2 - correct)
cost1 = 20;         % cost of collecting sample 1
cost2 = 20;         % cost of collecting sample 2
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

if (1)
figure(1)
hold on
plot(pGrid,Action_Stop,'k','LineWidth',3)
plot(pGrid,Action_Sample1,'r','LineWidth',3)
plot(pGrid,Action_Sample2,'b','LineWidth',3)
axis([0 1 0.9 1.1])
xlabel('Prior probability','Interpreter','Latex')
ylabel('Color indicate strategy','Interpreter','Latex')
set(gcf, 'Position',  [0, 0, 300, 230])
end


%% Figures

if (0)
figure(10)
hold on
l_stop =    plot(pGrid,StopValue,'--k','LineWidth',3);
l_optimal = plot(pGrid,initial,'LineWidth',3);
xticks([0 0.25 0.5 0.75 1])
%yticks([500 750 1000])
xlabel('Prior probability','Interpreter','Latex')
ylabel('Expected value','Interpreter','Latex')
axis([0 1 min(initial)-0.1*(max(initial)-min(initial)) max(initial)+0.1*(max(initial)-min(initial))])
legend([l_optimal l_stop],{'Optimal Strategy', 'Immediate Choice'},'Location','north','Interpreter','Latex')
set(gcf, 'Position',  [0, 0, 300, 230])
end

if (0)
figure(11)
hold on
l_stop =    plot(pGrid(V_choose==initial),initial(V_choose==initial),'k','LineWidth',3);
l_sample1 = plot(pGrid(V_sample1==initial),initial(V_sample1==initial),'r','LineWidth',3);
l_sample2 = plot(pGrid(V_sample2==initial),initial(V_sample2==initial),'b','LineWidth',3);
xticks([0 0.25 0.5 0.75 1])
%yticks([500 750 1000])
xlabel('Prior probability','Interpreter','Latex')
ylabel('Expected value','Interpreter','Latex')
axis([0 1 min(initial)-0.1*(max(initial)-min(initial)) max(initial)+0.1*(max(initial)-min(initial))])
legend([l_stop l_sample1 l_sample2],{'Stop', 'Sample Red', 'Sample Blue'},'Location','north','Interpreter','Latex')
set(gcf, 'Position',  [0, 0, 300, 230])
end

if (0)
figure(12)
hold on
l_stop =    plot(pGrid(V_choose==initial & pGrid<0.5),initial(V_choose==initial & pGrid<0.5),'k','LineWidth',3);
l_sample1 = plot(pGrid(V_sample1==initial & pGrid<0.5),initial(V_sample1==initial & pGrid<0.5),'r','LineWidth',3);
l_sample2 = plot(pGrid(V_sample2==initial & pGrid<0.5),initial(V_sample2==initial & pGrid<0.5),'b','LineWidth',3);
l_stop =    plot(pGrid(V_choose==initial & pGrid>0.5),initial(V_choose==initial & pGrid>0.5),'k','LineWidth',3);
l_sample1 = plot(pGrid(V_sample1==initial & pGrid>0.5),initial(V_sample1==initial & pGrid>0.5),'r','LineWidth',3);
l_sample2 = plot(pGrid(V_sample2==initial & pGrid>0.5),initial(V_sample2==initial & pGrid>0.5),'b','LineWidth',3);
xticks([0 0.25 0.5 0.75 1])
%yticks([500 750 1000])
xlabel('Prior probability','Interpreter','Latex')
ylabel('Expected value','Interpreter','Latex')
axis([0 1 min(initial)-0.1*(max(initial)-min(initial)) max(initial)+0.1*(max(initial)-min(initial))])
legend([l_stop l_sample1 l_sample2],{'Stop', 'Sample Red', 'Sample Blue'},'Location','north','Interpreter','Latex')
set(gcf, 'Position',  [0, 0, 300, 230])
end

if (0)
figure(13)
hold on
l_stop =    plot(pGrid,V_choose,'k','LineWidth',3);
l_sample1 = plot(pGrid,V_sample1,'r','LineWidth',3);
l_sample2 = plot(pGrid,V_sample2,'b','LineWidth',3);
xticks([0 0.25 0.5 0.75 1])
%yticks([500 750 1000])
xlabel('Prior probability','Interpreter','Latex')
ylabel('Value','Interpreter','Latex')
axis([0 1 min(initial)-0.1*(max(initial)-min(initial)) max(initial)+0.1*(max(initial)-min(initial))])
legend([l_stop l_sample1 l_sample2],{'Stop', 'Sample Red', 'Sample Blue'},'Location','north','Interpreter','Latex')
set(gcf, 'Position',  [0, 0, 300, 230])
end

