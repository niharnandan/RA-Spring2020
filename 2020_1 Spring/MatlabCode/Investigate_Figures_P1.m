%% Investigate_Figures_P1

%% TASK 1 - Y = ACCUSE PROB, X = CURRENT BELIEF

% main figure (both treatments)
figureID = 11101;
db = t1_accuse_clean;

% Discretize the posterior beliefs (divide into N bins)
n_bins = 7;
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

% CREATE THE FIGURE
figure(figureID)
hold on
% optimal behavior
plot([0 0.5 0.5 1],[0 0 1 1],':k','LineWidth',2);
% pr_accuse, all data
x = n_bins_table(:,3)';
y_investigate = x*0;
for i_y=1:n_bins
    db_condition = db(db(:,19)==x(i_y),:);
    y_investigate(i_y) = 1-mean(db_condition(:,10));
end
plot(x,y_investigate,'k','LineWidth',2);

% cosmetics
axis([0 1 0 1])
xlabel('Updated Pr(Red Guilty)','Interpreter','Latex')
ylabel('Pr(Accuse Red)','Interpreter','Latex')
%xticks(round(x,2))
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it



% divide by prior or by number of rounds
if (1)
% pr_accuse, based on the prior
n_prior = [1 3 5 7 9]/10;
for i_prior=[2,4]
    db_round = db(db(:,7)==n_prior(i_prior),:);
    y_accused = x*0;
    for i_y=1:n_bins
        db_condition = db_round(db_round(:,19)==x(i_y),:);
        y_investigate(i_y) = 1-mean(db_condition(:,10));
    end
    plot(x,y_investigate,'Color',v_colors(i_prior*2-3,:)); 
end
end

figureID=figureID+1;
scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it


%% TASK 1 - Y = ACCUSE PROB, X = CURRENT BELIEF

% main figure (both treatments)
figureID = 11201;
db = t1_investigate_clean;

% Discretize the posterior beliefs (divide into N bins)
n_bins = 7;
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
print(gcf,figureNAME,'-dpdf')          % then print it

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

figureID=figureID+1;
scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it


% divide by prior or by number of rounds
if (1)
% pr_accuse, based on the prior
n_prior = [1 3 5 7 9]/10;
for i_prior=[1:5]
    db_round = db(db(:,7)==n_prior(i_prior),:);
    y_accused = x*0;
    for i_y=1:n_bins
        db_condition = db_round(db_round(:,19)==x(i_y),:);
        y_investigate(i_y) = 1-mean(db_condition(:,10));
    end
    plot(x,y_investigate,'Color',v_colors(i_prior,:)); 
end
end

figureID=figureID+1;
scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it

%%







%% TASK 2 - Y = ACCUSE PROB, X = CURRENT BELIEF

% main figure (both treatments)
figureID = 21101;
db = t2_accuse_clean;

% Discretize the posterior beliefs (divide into N bins)
n_bins = 7;
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

% CREATE THE FIGURE
figure(figureID)
hold on
% optimal behavior
plot([0 0.5 0.5 1],[0 0 1 1],':k','LineWidth',2);
% pr_accuse, all data
x = n_bins_table(:,3)';
y_investigate = x*0;
for i_y=1:n_bins
    db_condition = db(db(:,19)==x(i_y),:);
    y_investigate(i_y) = 1-mean(db_condition(:,10));
end
plot(x,y_investigate,'k','LineWidth',2);

% divide by prior or by number of rounds
if (0)
% pr_accuse, based on the prior
n_prior = [1 3 5 7 9]/10;
for i_prior=[2,4]
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
ylabel('Pr(Accuse Red)','Interpreter','Latex')
%xticks(round(x,2))
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
print(gcf,figureNAME,'-dpdf')          % then print it


%% TASK 2 - Y = ACCUSE PROB, X = CURRENT BELIEF

% main figure (both treatments)
figureID = 21201;
db = t2_investigate_clean;

% Discretize the posterior beliefs (divide into N bins)
n_bins = 7;
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
if (0)
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
print(gcf,figureNAME,'-dpdf')          % then print it













