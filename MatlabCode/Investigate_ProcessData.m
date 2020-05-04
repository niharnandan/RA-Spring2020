%% Investigate_ProcessData

%% TASK 1

% SEPARATE ACCUSE AND INVESTIGATE
t1_accuse = t1_s4(t1_s4(:,9)==1,:);
t1_investigate = t1_s4(t1_s4(:,9)==0,:);
% clean out the times in which the final evidence is already found
t1_accuse_clean = t1_accuse(t1_accuse(:,13)==0,:);
t1_investigate_clean = t1_investigate(t1_investigate(:,13)==0,:);




%% TASK 2

% SEPARATE ACCUSE AND INVESTIGATE
t2_accuse = t2_s4(t2_s4(:,9)==1,:);
t2_investigate = t2_s4(t2_s4(:,9)==0,:);
% clean out the times in which the final evidence is already found
t2_accuse_clean = t2_accuse(t2_accuse(:,13)==0,:);
t2_investigate_clean = t2_investigate(t2_investigate(:,13)==0,:);


%%
% add discrete posteriors (divide into N bins)
n_bins = 11;
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
for i_trial=1:length(t1_4)
   p_posterior = t1_4(i_trial,14);
   for i_bin=1:n_bins
       if p_posterior>n_bins_table(i_bin,1)
           if p_posterior<=n_bins_table(i_bin,2)
               t1_4(i_trial,18)=n_bins_table(i_bin,3);
           end
       end
   end
end
% remove rounds in which the evidence was found and accusation rounds
db = t1_4;
db = db(db(:,12)==0,:);
db = db(db(:,8)==0,:);
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

% 45 degrees line
plot([0.1 0.9],[0.1 0.9],':k');
% pr_accuse, all data
x = n_bins_table(:,3)';
y_investigate = x*0;
for i_y=1:n_bins
    db_condition = db(db(:,18)==x(i_y),:);
    y_investigate(i_y) = mean(db_condition(:,9));
end
plot(x,y_investigate,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:n_bins
        db_condition = db_round(db_round(:,18)==x(i_y),:);
        y_investigate(i_y) = mean(db_condition(:,9));
    end
    plot(x,y_investigate,'Color',v_colors(i_round,:)); 
end




%% TASK 2






