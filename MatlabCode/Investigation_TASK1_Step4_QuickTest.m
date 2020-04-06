%% Investigation_TASK1_Step4_QuickTest

% vector of colors
color_red  = [1 0 0];
color_blue = [0 0 1];
n_colors = 5;
v_colors = [0:1/(n_colors-1):1]'.*color_red + [1:-1/(n_colors-1):0]'.*color_blue;

% input
open('t1_4')

% read relevant information
participant_ID = t1_4(:,1);
treatment_condition = t1_4(:,2);
number_rounds_available = t1_4(:,5);
prior_guilty_prob = t1_4(:,6);
action_type = t1_4(:,8);
action_target = t1_4(:,9);
evidence_found = t1_4(:,12);
posterior_guilty_prob = t1_4(:,14);
correct_guilty = t1_4(:,15);
accused_guilty = t1_4(:,16);



%% FIGURE 1
% investigation probability as a function of prior belief

% main figure (both treatments)
figureID = 11101;
db = t1_4;
% remove rounds in which the evidence was found and accusation rounds
db = db(db(:,12)==0,:);
db = db(db(:,8)==0,:);
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

% pr_accuse, all data
x = [0.1 0.3 0.5 0.7 0.9];
y_investigate = x*0;
for i_y=1:5
    db_condition = db(db(:,6)==x(i_y),:);
    y_investigate(i_y) = mean(db_condition(:,9));
end
plot(x,y_investigate,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,6)==x(i_y),:);
        y_investigate(i_y) = mean(db_condition(:,9));
    end
    plot(x,y_investigate,'Color',v_colors(i_round,:)); 
end
% cosmetics
axis([0 1 0 1])
xlabel('Prior probability guilty','Interpreter','Latex')
ylabel('Investigate probability','Interpreter','Latex')
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it




%% FIGURE 2
% investigation probability as a function of current belief

% main figure (both treatments)
figureID = 11201;
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
% cosmetics
axis([0 1 0 1])
xlabel('Current probability guilty','Interpreter','Latex')
ylabel('Investigate probability','Interpreter','Latex')
xticks(round(x,2))
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it




%% FIGURE 3
% accusation probability as a function of prior belief

% main figure (both treatments)
figureID = 11301;
db = t1_4;
% remove rounds in which the evidence was found and investigation rounds
db = db(db(:,12)==0,:);
db = db(db(:,8)==1,:);
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

% pr_accuse, all data
x = [0.1 0.3 0.5 0.7 0.9];
y_investigate = x*0;
for i_y=1:5
    db_condition = db(db(:,6)==x(i_y),:);
    y_investigate(i_y) = mean(db_condition(:,9));
end
plot(x,y_investigate,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,6)==x(i_y),:);
        y_investigate(i_y) = mean(db_condition(:,9));
    end
    plot(x,y_investigate,'Color',v_colors(i_round,:)); 
end
% cosmetics
axis([0 1 0 1])
xlabel('Prior probability guilty','Interpreter','Latex')
ylabel('Accuse probability','Interpreter','Latex')
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it




%% FIGURE 4
% accusation probability as a function of current belief

% main figure (both treatments)
figureID = 11401;
db = t1_4;
% remove rounds in which the evidence was found and investigation rounds
db = db(db(:,12)==0,:);
db = db(db(:,8)==1,:);
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

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
% cosmetics
axis([0 1 0 1])
xlabel('Current probability guilty','Interpreter','Latex')
ylabel('Accuse probability','Interpreter','Latex')
xticks(round(x,2))
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it


