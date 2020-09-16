%% Investigate_Figures_P2

%% TASK 2 - Y = ACCUSE PROB, X = CURRENT BELIEF

% main figure (both treatments)
figureID = 21301;
db_all = [t2_accuse_clean; t2_investigate_clean];


cost_level = 80;
db = db_all(db_all(:,5)==cost_level,:);

% Discretize the posterior beliefs (divide into N bins)
n_bins = 9;
n_bins_table = zeros(n_bins,3);
bin_gap=1/n_bins;
for i_bin = 1:n_bins
    min_bin=bin_gap*(i_bin-1);
    max_bin=bin_gap*i_bin;
    avg_bin=(min_bin+max_bin)/2;
    n_bins_table(i_bin,:) = [min_bin max_bin avg_bin]; 
end
n_bins_table(1,1)=-0.01;
% fill the posterior column
for i_trial=1:length(db)
   p_posterior = db(i_trial,15);
   for i_bin=1:n_bins
       if p_posterior>n_bins_table(i_bin,1)
           if p_posterior<=n_bins_table(i_bin,2)
               db(i_trial,19)=n_bins_table(i_bin,3);
           end
       end
   end
end
% action probability for each posterior bin
n_bins_action = zeros(n_bins,3);
for i_bin = 1:n_bins
    select_trials = db(db(:,19)==n_bins_table(i_bin,3),:);
    n_stop=sum(select_trials(:,9)==1);
    investigate_trials = select_trials(select_trials(:,9)==0,:);
    n_red=sum(select_trials(:,10)==0);
    n_blue=sum(select_trials(:,10)==1);
    n_bins_action(i_bin,:) = [n_red n_blue n_stop]/sum([n_red n_blue n_stop]); 
end

%%
if (0)
figure(1)
bar(n_bins_action,'stacked')
end
%%

if (1)
% CREATE THE FIGURE
figure(figureID)
hold on
% optimal behavior
plot([0 0.5 0.5 1],[1 1 0 0],':k','LineWidth',2);
% pr_accuse, all data
x = n_bins_table(:,3)';
y_investigate = x*0;
for i_y=1:n_bins
    db_condition = db(db(:,19)==x(i_y),:);
    y_investigate(i_y) = 1-mean(db_condition(:,10));
end
plot(x,y_investigate,'k','LineWidth',2);

% divide by prior or by number of rounds
if (1)
% pr_accuse, based on the prior
n_prior = [1 3 5 7 9]/10;
for i_prior=[1,5]
    db_round = db(db(:,7)==n_prior(i_prior),:);
    y_accused = x*0;
    for i_y=1:n_bins
        db_condition = db_round(db_round(:,19)==x(i_y),:);
        y_investigate(i_y) = 1-mean(db_condition(:,10));
    end
    plot(x,y_investigate,'Color',v_colors(i_prior,:)); 
end
end

% cosmetics
axis([0 1 0 1])
xlabel('Updated Pr(Red Guilty)','Interpreter','Latex')
ylabel('Pr(Investigate Red)','Interpreter','Latex')
%xticks(round(x,2))
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
%print(gcf,figureNAME,'-dpdf')          % then print it

end











