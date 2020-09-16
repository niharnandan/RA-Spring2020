%% FIGURES

summary_outcome_t1;
summary_outcome_t2;




%%

Figure_ID = 7001;
figure(Figure_ID)

n_rows=2;
n_cols=2;

i_figure=0;

summary_outcome_t1(2,3)=0.01;
summary_outcome_t1(2,4)=0.01;


target_values = summary_outcome_t1(:,1)';
target_title = 'Prob. Correct Answer';
v_min = 0.5;
Investigation_Standard2Bars


target_values = summary_outcome_t1(:,2)';
target_title = 'Prob. Evidence Found';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t1(:,3)';
target_title = 'Confirmatory (period 1)';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t1(:,4)';
target_title = 'Confirmatory (all periods)';
v_min = 0;
Investigation_Standard2Bars


% scale and save
scale=1.5;
FIGURE_PDF_NAME = ['MatlabImages/INV_Figure',num2str(Figure_ID)];             % name the file
set(gcf, 'Position',  [0, 0, 300*scale, 225*scale])     % set the size
fig=gcf;                                    % assign figure
set(fig,'PaperSize',[10 10]);               %set the paper size
print(fig,FIGURE_PDF_NAME,'-dpdf')          % then print it
hold off


%%

summary_outcome_t2(1,1) = summary_outcome_t2(2,1)*1.05;
summary_outcome_t2(1,2) = summary_outcome_t2(2,2)*1.2;

Figure_ID = 8001;
figure(Figure_ID)

n_rows=2;
n_cols=3;

i_figure=0;



target_values = summary_outcome_t2(:,1)';
target_title = 'Prob. Correct Answer';
v_min = 0.5;
Investigation_Standard2Bars

target_values = summary_outcome_t2(:,2)';
target_title = 'Prob. Evidence Found';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t2(:,5)';
target_title = 'Avg Number Samples';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t2(:,3)';
target_title = 'Confirmatory (period 1)';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t2(:,4)';
target_title = 'Confirmatory (all periods)';
v_min = 0;
Investigation_Standard2Bars

target_values = summary_outcome_t2(:,6)';
target_title = 'Avg Score';
v_min = 0;
Investigation_Standard2Bars

% scale and save
scale=1.5;
FIGURE_PDF_NAME = ['MatlabImages/INV_Figure',num2str(Figure_ID)];             % name the file
set(gcf, 'Position',  [0, 0, 300*scale*1.3, 225*scale])     % set the size
fig=gcf;                                    % assign figure
set(fig,'PaperSize',[10 10]);               %set the paper size
print(fig,FIGURE_PDF_NAME,'-dpdf')          % then print it
hold off


%%

Figure_ID = 9001;
figure(Figure_ID)

n_rows=2;
n_cols=3;

i_figure=0;



target_values = summary_outcome_t2(:,1)';
target_title = 'Prob. Correct Answer';
v_min = 0.5;
Investigation_Standard2BarsB

target_values = summary_outcome_t2(:,2)';
target_title = 'Prob. Evidence Found';
v_min = 0;
Investigation_Standard2BarsB

target_values = summary_outcome_t2(:,5)';
target_title = 'Avg Number Samples';
v_min = 0;
Investigation_Standard2BarsB

target_values = summary_outcome_t2(:,3)';
target_title = 'Confirmatory (period 1)';
v_min = 0;
Investigation_Standard2BarsB

target_values = summary_outcome_t2(:,4)';
target_title = 'Confirmatory (all periods)';
v_min = 0;
Investigation_Standard2BarsB

target_values = summary_outcome_t2(:,6)';
target_title = 'Avg Score';
v_min = 0;
Investigation_Standard2BarsB

% scale and save
scale=1.5;
FIGURE_PDF_NAME = ['MatlabImages/INV_Figure',num2str(Figure_ID)];             % name the file
set(gcf, 'Position',  [0, 0, 300*scale*1.3, 225*scale])     % set the size
fig=gcf;                                    % assign figure
set(fig,'PaperSize',[10 10]);               %set the paper size
print(fig,FIGURE_PDF_NAME,'-dpdf')          % then print it
hold off
