# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:47:46 2023

@author: joujo
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import *#ttest_ind

# Set the paths to the input files and output file
file_path1="C:/Users/joujo/Documents/Master_Thesis/Prediction/Arcuate_Fac_Left_V1.xlsx"
file_path2="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Body.xlsx"
file_path3="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Genu.xlsx"
file_path4="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Splenium.xlsx"
file_path5="C:/Users/joujo/Documents/Master_Thesis/Prediction/Uncinate_Fasciculus_L.xlsx"
file_path6="C:/Users/joujo/Documents/Master_Thesis/Prediction/Uncinate_Fasciculus_R.xlsx"

file_path7="C:/Users/joujo/Documents/Master_Thesis/Prediction/IFOF_L.xlsx"
file_path8="C:/Users/joujo/Documents/Master_Thesis/Prediction/IFOF_R.xlsx"


name ="IFOF_R"
file_path=file_path8

output_file = "C:/Users/joujo/Documents/Master_Thesis/Prediction/summary_stats_"+name+".xlsx"

# Define the columns to extract from each input file
data_cols = ['patient', 'mean_FA', 'max_FA', 'min_FA', 'std', 'TrackCount', 'M6_CAP']

# Initialize empty lists to hold the extracted data
cap_good = []
patient_good = []
mean_good = []
min_good = []
max_good = []
std_good = []
tract_count_good = []

cap_bad = []
patient_bad = []
mean_bad = []
min_bad = []
max_bad = []
std_bad = []
tract_count_bad = []


df = pd.read_excel(file_path, usecols=data_cols)
cap = df["M6_CAP"]
mean = df["mean_FA"]
max_ = df["max_FA"]
min_ = df["min_FA"]
std = df["std"]
tract_count = df["TrackCount"]
        
# Loop over the data and separate into "good" and "bad" groups based on CAP score
for i in range(len(cap)):
    if not np.isnan(cap[i]):
        if cap[i] > 6:
            cap_good.append(cap[i])
            patient_good.append(df.loc[i, "patient"])
            mean_good.append(mean[i])
            max_good.append(max_[i])
            min_good.append(min_[i])
            std_good.append(std[i])
            tract_count_good.append(tract_count[i])
        elif 0 < cap[i] < 6:
            cap_bad.append(cap[i])
            patient_bad.append(df.loc[i, "patient"])
            mean_bad.append(mean[i])
            max_bad.append(max_[i])
            min_bad.append(min_[i])
            std_bad.append(std[i])
            tract_count_bad.append(tract_count[i])

# Calculate summary statistics for the "good" and "bad" groups
stats_good = pd.DataFrame({
    "Mean_FA": mean_good,
    "Max_FA": max_good,
    "Min_FA": min_good,
    "Std_FA": std_good,
    "TrackCount": tract_count_good
}).describe()

stats_bad = pd.DataFrame({
    "Mean_FA": mean_bad,
    "Max_FA": max_bad,
    "Min_FA": min_bad,
    "Std_FA": std_bad,
    "TrackCount": tract_count_bad
}).describe()


t_test_results = {
    "Variable1": ["TrackCount_Good", "Mean_FA_Good", "Min_FA_Good", "Max_FA_Good"],
    "Variable2": ["TrackCount_Bad", "Mean_FA_Bad", "Min_FA_Bad", "Max_FA_Bad"],
    "T-statistic": [stats.ttest_ind(a=tract_count_good, b=tract_count_bad, equal_var=True).statistic,
                    stats.ttest_ind(a=mean_good, b=mean_bad, equal_var=True).statistic,
                    stats.ttest_ind(a=min_good, b=min_bad, equal_var=True).statistic,
                    stats.ttest_ind(a=max_good, b=max_bad, equal_var=True).statistic],
    "P-value": [stats.ttest_ind(a=tract_count_good, b=tract_count_bad, equal_var=True).pvalue,
                stats.ttest_ind(a=mean_good, b=mean_bad, equal_var=True).pvalue,
                stats.ttest_ind(a=min_good, b=min_bad, equal_var=True).pvalue,
                stats.ttest_ind(a=max_good, b=max_bad, equal_var=True).pvalue]
}

# Create a DataFrame from the t-test results
t_test_results_df = pd.DataFrame(t_test_results)


###############
# Conduct two sample t-test on the mean FA values for the "good" and "bad" groups
#t_stat, p_val = ttest_ind(mean_good, mean_bad, equal_var=True)
#t_test=pd.DataFrame({"T-statistic": [t_stat], "P-value": [p_val]})

# Write the summary statistics and t-test results to a new Excel file
with pd.ExcelWriter(output_file) as writer:
    stats_good.to_excel(writer, sheet_name="CAP > 6")
    stats_bad.to_excel(writer, sheet_name="0 < CAP < 6")
    t_test_results_df.to_excel(writer, sheet_name="Pairwise T-tests")
    
    #pd.DataFrame({"T-statistic": [t_stat], "P-value": [p_val]}).to_excel(writer, sheet_name="T-test")
