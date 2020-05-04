%% Investigation_MAIN

clear
clc
close all

%% read files and store in a database

if (0)
t1_s3 = csvread('Task1_step3.csv', 1, 0);
t1_s4 = csvread('Task1_step4.csv', 1, 0);
t2_s3 = csvread('Task2_step3.csv', 1, 0);
t2_s4 = csvread('Task2_step4.csv', 1, 0);
t3_s3 = csvread('Task3_step3.csv', 1, 0);
t3_s4 = csvread('Task3_step4.csv', 1, 0);

Investigation_Database = [];
Investigation_Database.t1_s3=t1_s3;
Investigation_Database.t1_s4=t1_s4;
Investigation_Database.t2_s3=t2_s3;
Investigation_Database.t2_s4=t2_s4;
Investigation_Database.t3_s3=t3_s3;
Investigation_Database.t3_s4=t3_s4;

save('Investigation_Database.mat','Investigation_Database')

else
    
load('Investigation_Database.mat')

t1_s3 = Investigation_Database.t1_s3;
t1_s4 = Investigation_Database.t1_s4;
t1_s4 = t1_s4(:,[1:5,5,6:17]);

t2_s3 = Investigation_Database.t2_s3;
t2_s4 = Investigation_Database.t2_s4;

t3_s3 = Investigation_Database.t3_s3;
t3_s4 = Investigation_Database.t3_s4;
    
end

%% create datasets

Investigate_ProcessData

%% create images

Investigate_Figures

