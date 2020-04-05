%% Investigation_MAIN_Images

% Initialize
clear
close all
clc

% Load Folders
addpath('MatlabCode')       % code to run analysis
addpath('MatlabImages')     % folder to store images

% Load CSVs
% remove the first line of the CSV file (headers)
t1_3 = csvread('Task1_step3.csv',1,0);  % task1, step3
t1_4 = csvread('Task1_step4.csv',1,0);  % task1, step4

% Run files to generate images
Investigation_TASK1_Step3_QuickTest
Investigation_TASK1_Step4_QuickTest

% close images
close all


