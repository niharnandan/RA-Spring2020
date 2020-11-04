def c_statistic(file):

    from pandas import read_csv
    from numpy import mean
    # read dataset
    temp1 = read_csv(file)
    # isolate accuse rounds and investigation rounds
    t2_accuse = temp1.loc[temp1['action_type'] == 1]
    t2_investigate = temp1.loc[temp1['action_type'] == 0]
    # select accuse and investigation rounds WITHOUT evidence found
    t2_accuse_clean = t2_accuse.loc[t2_accuse['evidence_found'] == 0]
    t2_investigate_clean = t2_investigate.loc[t2_investigate['evidence_found'] == 0]  
    # select accuse rounds WITH evidence found
    t2_accuse_certain = t2_accuse.loc[t2_accuse['evidence_found'] == 1]

    
    # number of collected samples at the accusation round (= round ID - 1)
    distr_stop_time = t2_accuse['current_rounds'].to_list()
    distr_stop_time = [x - 1 for x in distr_stop_time]
    distr_stop_time_average = mean(distr_stop_time)
    #print(distr_stop_time_average)  
    # equivalent method (same result)
    t2_totsamples = t2_accuse.iloc[:,10]+t2_accuse.iloc[:,11]
    t2_avg_samples = mean(t2_totsamples)
    #print(t2_avg_samples)

    
    # distribution of beliefs at the accusation round
    distr_stop_belief = t2_accuse['posterior'].to_list()
    
    # percentage correct accusation
    t2_accuse_correct = t2_accuse.iloc[:,15]==t2_accuse.iloc[:,16]
    t2_perc_correct = mean(t2_accuse_correct)
    #print(t2_perc_correct)
    
    # percentage evidence found
    t2_perc_evidence_found = mean(t2_accuse.iloc[:,12])
    #print(t2_perc_evidence_found)

    # FIRST ROUND CONFIRMATORY BEHAVIOR (investigate only)
    select_rounds = t2_investigate
    select_rounds = select_rounds.loc[select_rounds.iloc[:,7]==1,:]
    # pr(blue) when blue is more likely
    select_rounds_low = select_rounds.loc[select_rounds.iloc[:,6]<0.5,:]
    avg_rounds_low = mean(select_rounds_low.iloc[:,9])
    # pr(red) when red is more likely
    select_rounds_high = select_rounds.loc[select_rounds.iloc[:,6]>0.5,:]
    avg_rounds_high = 1-mean(select_rounds_high.iloc[:,9])
    # confirmatory behavior in round 1
    t2_perc_confirmatory_round1 = mean([avg_rounds_low, avg_rounds_high])
    #print(t2_perc_confirmatory_round1)

    # ALL ROUNDS CONFIRMATORY BEHAVIOR (investigate only)
    select_rounds = t2_investigate_clean
    # pr(blue) when blue is more likely
    select_rounds_low = select_rounds.loc[select_rounds.iloc[:,14]<0.5,:]
    avg_rounds_low = mean(select_rounds_low.iloc[:,9])
    # pr(red) when red is more likely
    select_rounds_high = select_rounds.loc[select_rounds.iloc[:,14]>0.5,:]
    avg_rounds_high = 1-mean(select_rounds_high.iloc[:,9])
    no_part = select_rounds['participant_ID'].max()
    t2_perc_confirmatory_allrounds = mean([avg_rounds_low, avg_rounds_high])
    #print(t2_perc_confirmatory_allrounds)
    
    # score (good for tasks 2 and 3)
    t2_unitcostred  = t2_accuse.iloc[:,4]
    t2_unitcostblue = t2_accuse.iloc[:,5]
    t2_round_score = 500 + t2_accuse_correct*1000  -t2_unitcostred*t2_accuse.iloc[:,10] -t2_unitcostblue*t2_accuse.iloc[:,11]
    t2_avg_score = mean(t2_round_score)    
    #print(t2_avg_score)    
    
    
    # RETURN OUTPUT
    return t2_avg_score,t2_avg_samples,t2_perc_confirmatory_allrounds,t2_perc_confirmatory_round1
    
def statistic_part(file):
    from pandas import read_csv
    from numpy import mean
    from numpy import array
    # read dataset
    temp1 = read_csv(file)
    t2_accuse = temp1.loc[temp1['action_type'] == 1]
    t2_totsamples = t2_accuse.iloc[:,10]+t2_accuse.iloc[:,11]
    avg_samples = mean(t2_totsamples)
    
    t2_investigate = temp1.loc[temp1['action_type'] == 0]
    select_rounds = t2_investigate.loc[t2_investigate['evidence_found'] == 0]
    high = select_rounds.loc[select_rounds.iloc[:,14]>0.5,:]
    low = select_rounds.loc[select_rounds.iloc[:,14]<0.5,:]
    
    no_parts = low['participant_ID'].max()
    avg_rounds_low = []
    for i in range(1,int(no_parts+1)):
        avg_rounds_low.append(1-mean(low.loc[low['participant_ID'] == i].iloc[:,9]))
    avg_rounds_high = []
    for i in range(1,int(no_parts+1)):
        avg_rounds_high.append(1-mean(high.loc[high['participant_ID'] == i].iloc[:,9]))
    avg_samples = []
    for i in range(1,int(no_parts+1)):
        avg_samples.append(mean(t2_accuse.loc[t2_accuse['participant_ID'] == i].iloc[:,10] +t2_accuse.loc[t2_accuse['participant_ID'] == i].iloc[:,11]))

    return (array(avg_rounds_low)+array(avg_rounds_high))/2,avg_samples