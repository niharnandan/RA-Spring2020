%% Investigation_TASK1_Step3_QuickTest

% vector of colors
color_red  = [1 0 0];
color_blue = [0 0 1];
n_colors = 5;
v_colors = [0:1/(n_colors-1):1]'.*color_red + [1:-1/(n_colors-1):0]'.*color_blue;

% input
open('t1_3')

% read relevant information
participant_ID = t1_3(:,1);
treatment_condition = t1_3(:,2);
number_rounds_available = t1_3(:,5);
prior_guilty_prob = t1_3(:,6);
correct_guilty = t1_3(:,7);
accused_guilty = t1_3(:,8);
correct_accused = t1_3(:,38);
evidence_round = t1_3(:,39);
evidence_found = evidence_round>0;

t1_3(:,40) = t1_3(:,39)>0;



%% FIGURE 1
% accuse probability as a function of prior

% main figure (both treatments)
figureID = 10101;
db = t1_3;
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

% 45 degrees line
plot([0.1 0.9],[0.9 0.1],':k');
% pr_accuse, all data
x = [0.1 0.3 0.5 0.7 0.9];
y_correct = x*0;
y_accused = x*0;
for i_y=1:5
    db_condition = db(db(:,6)==x(i_y),:);
    y_correct(i_y) = mean(db_condition(:,7));
    y_accused(i_y) = mean(db_condition(:,8));
end
plot(x,y_correct,':b');
plot(x,y_accused,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,6)==x(i_y),:);
        y_accused(i_y) = mean(db_condition(:,8));
    end
    plot(x,y_accused,'Color',v_colors(i_round,:)); 
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







% separate treatments
figureID = 10102;
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)

subplot(1,2,1)
db = t1_3;
db = db(db(:,2)==0,:);
hold on

% 45 degrees line
plot([0.1 0.9],[0.9 0.1],':k');
% pr_accuse, all data
x = [0.1 0.3 0.5 0.7 0.9];
y_correct = x*0;
y_accused = x*0;
for i_y=1:5
    db_condition = db(db(:,6)==x(i_y),:);
    y_correct(i_y) = mean(db_condition(:,7));
    y_accused(i_y) = mean(db_condition(:,8));
end
plot(x,y_correct,':b');
plot(x,y_accused,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,6)==x(i_y),:);
        y_accused(i_y) = mean(db_condition(:,8));
    end
    plot(x,y_accused,'Color',v_colors(i_round,:)); 
end
% cosmetics
axis([0 1 0 1])
xlabel('Prior probability guilty','Interpreter','Latex')
ylabel('Accuse probability','Interpreter','Latex')
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

subplot(1,2,2)
db = t1_3;
db = db(db(:,2)==1,:);
hold on

% 45 degrees line
plot([0.1 0.9],[0.9 0.1],':k');
% pr_accuse, all data
x = [0.1 0.3 0.5 0.7 0.9];
y_correct = x*0;
y_accused = x*0;
for i_y=1:5
    db_condition = db(db(:,6)==x(i_y),:);
    y_correct(i_y) = mean(db_condition(:,7));
    y_accused(i_y) = mean(db_condition(:,8));
end
plot(x,y_correct,':b');
plot(x,y_accused,'k','LineWidth',2);
% pr_accuse, based on the number of rounds
n_rounds = [1 3 5 7 9];
for i_round=1:5
    db_round = db(db(:,5)==n_rounds(i_round),:);
    y_accused = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,6)==x(i_y),:);
        y_accused(i_y) = mean(db_condition(:,8));
    end
    plot(x,y_accused,'Color',v_colors(i_round,:)); 
end
% cosmetics
axis([0 1 0 1])
xlabel('Prior probability guilty','Interpreter','Latex')
ylabel('Accuse probability','Interpreter','Latex')
xticks([0.1:0.2:0.9])
yticks([0.1:0.2:0.9])

scale = 1;
set(gcf, 'Position',  [0, 0, 2*360*scale, 300*scale])
set(gcf,'PaperSize',[14 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it







%% FIGURE 2
% correct accuse and evidence found probability as a function of n. rounds

% main figure (both treatments)
figureID = 10201;
db = t1_3;
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)
hold on

% horizontal line
plot([1 9],[1 1],':k');
% pr_correct and pr_evidence_found
x = [1 3 5 7 9];
y_accused_correct = x*0;
y_found = x*0;
for i_y=1:5
    db_condition = db(db(:,5)==x(i_y),:);
    y_accused_correct(i_y) = mean(db_condition(:,38));
    y_found(i_y) = mean(db_condition(:,40));
end
plot(x,y_accused_correct,'k','LineWidth',2);
plot(x,y_found,':k','LineWidth',1);
% pr_accuse, as a function of prior
prior_prob = [1 3 5 7 9]/10;
for i_prob=1:5
    db_round = db(db(:,6)==prior_prob(i_prob),:);
    y_accused_correct = x*0;
    y_found = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,5)==x(i_y),:);
        y_accused_correct(i_y) = mean(db_condition(:,38));
        y_found(i_y) = mean(db_condition(:,40));
    end
    plot(x,y_accused_correct,'Color',v_colors(i_prob,:),'LineWidth',2);
    plot(x,y_found,'Color',v_colors(i_prob,:),'LineWidth',0.5);
end
% cosmetics
axis([0 10 0 1.05])
xlabel('Number of rounds available','Interpreter','Latex')
ylabel('Prob. correct accusation','Interpreter','Latex')
xticks([1:2:9])
yticks([0:0.2:1])

scale = 1;
set(gcf, 'Position',  [0, 0, 360*scale, 300*scale])
set(gcf,'PaperSize',[7 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it







% separate treatments
figureID = 10202;
figureNAME = ['MatlabImages/Investigation_Figure',num2str(figureID)];
figure(figureID)

subplot(1,2,1)
db = t1_3;
db = db(db(:,2)==0,:);
hold on

% horizontal line
plot([1 9],[1 1],':k');
% pr_correct and pr_evidence_found
x = [1 3 5 7 9];
y_accused_correct = x*0;
y_found = x*0;
for i_y=1:5
    db_condition = db(db(:,5)==x(i_y),:);
    y_accused_correct(i_y) = mean(db_condition(:,38));
    y_found(i_y) = mean(db_condition(:,40));
end
plot(x,y_accused_correct,'k','LineWidth',2);
plot(x,y_found,':k','LineWidth',1);
% pr_accuse, as a function of prior
prior_prob = [1 3 5 7 9]/10;
for i_prob=1:5
    db_round = db(db(:,6)==prior_prob(i_prob),:);
    y_accused_correct = x*0;
    y_found = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,5)==x(i_y),:);
        y_accused_correct(i_y) = mean(db_condition(:,38));
        y_found(i_y) = mean(db_condition(:,40));
    end
    plot(x,y_accused_correct,'Color',v_colors(i_prob,:),'LineWidth',2);
    plot(x,y_found,'Color',v_colors(i_prob,:),'LineWidth',0.5);
end
% cosmetics
axis([0 10 0 1.05])
xlabel('Number of rounds available','Interpreter','Latex')
ylabel('Prob. correct accusation','Interpreter','Latex')
xticks([1:2:9])
yticks([0:0.2:1])

subplot(1,2,2)
db = t1_3;
db = db(db(:,2)==1,:);
hold on

% horizontal line
plot([1 9],[1 1],':k');
% pr_correct and pr_evidence_found
x = [1 3 5 7 9];
y_accused_correct = x*0;
y_found = x*0;
for i_y=1:5
    db_condition = db(db(:,5)==x(i_y),:);
    y_accused_correct(i_y) = mean(db_condition(:,38));
    y_found(i_y) = mean(db_condition(:,40));
end
plot(x,y_accused_correct,'k','LineWidth',2);
plot(x,y_found,':k','LineWidth',1);
% pr_accuse, as a function of prior
prior_prob = [1 3 5 7 9]/10;
for i_prob=1:5
    db_round = db(db(:,6)==prior_prob(i_prob),:);
    y_accused_correct = x*0;
    y_found = x*0;
    for i_y=1:5
        db_condition = db_round(db_round(:,5)==x(i_y),:);
        y_accused_correct(i_y) = mean(db_condition(:,38));
        y_found(i_y) = mean(db_condition(:,40));
    end
    plot(x,y_accused_correct,'Color',v_colors(i_prob,:),'LineWidth',2);
    plot(x,y_found,'Color',v_colors(i_prob,:),'LineWidth',0.5);
end
% cosmetics
axis([0 10 0 1.05])
xlabel('Number of rounds available','Interpreter','Latex')
ylabel('Prob. correct accusation','Interpreter','Latex')
xticks([1:2:9])
yticks([0:0.2:1])

scale = 1;
set(gcf, 'Position',  [0, 0, 2*360*scale, 300*scale])
set(gcf,'PaperSize',[14 7]);            %set the paper size
print(gcf,figureNAME,'-dpdf')          % then print it

