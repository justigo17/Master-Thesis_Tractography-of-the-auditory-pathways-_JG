# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 16:19:19 2023

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 11:03:23 2023

@author: joujo
"""

#correlation matrix 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly as py
import plotly.express as px
import seaborn as sns
import plotly.graph_objs as go
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from plotly.offline import init_notebook_mode, iplot
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from scipy import stats
import seaborn as sns
from scipy.stats import pearsonr


#data = pd.read_excel ('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/PatientCorrel.xlsx')

data2=pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/Correlation2emepart.xlsx')

data = pd.read_excel("C:/Users/joujo/Documents/Master_Thesis/Prediction/Correlation_sansPatient.xlsx")
print(data2)

data3=pd.read_excel("C:/Users/joujo/Documents/Master_Thesis/Prediction/Correlation_Test.xlsx")

#-----------------------------------------
df = pd.DataFrame(data)
print(df)

col_means = df.mean()
col_median=df.median()

print(col_means)
# fill NaN values with the mean of their respective column
df = df.fillna(value=col_means)

df=df.fillna(value=col_median)
print(df)

#On considère, en général, que X et Y sont corrélées lorsque la valeur
# de leur Pearson r est supérieur à 0.5 ou inférieur à -0.5


col1=df.iloc[:,0:12]
col2=df.iloc[:,12:53]




for i in col1:
    for j in col2:
        if i != j:
            corr_coef = df[i].corr(df[j])
            #print(corr_coef)
    
            if (corr_coef>0.5 or corr_coef<-0.5):
                print("correlation de : ")
                print(corr_coef)
                print("entre")
                print(i)
                print(j)





            


#--------------------------------------------------------
print(df['M6_AC_0.5'])
corr_matrix = df.corr(method='spearman')
corr_coeff = df['TrackCount_CC_GENU'].corr(df['M6_AC_0.5'])

plt.figure(figsize=(12, 12))
sns.heatmap(corr_matrix, annot=False)
plt.show()



df["TrackCount_CC_GENU"].corr(df["M6_AC_0.5"])

corrM2["TrackCount_CC_GENU"].corr(corrM2["M6_AC_0.5"])

df["M6_AC_0.5"].corr(df["M6_AC_0.5"])


print(df["TrackCount_CC_GENU"])

x=df['M6_AWRS_CI']
y=df["mean_FA_CC_GENU"]
coeff_pearson= pearsonr(x,y)
print("coefficient de Pearson = {}".format(coeff_pearson))

corrM2 = df.corr()
print(corrM2)
plt.figure(figsize=(12, 12))
sns.heatmap(corrM2, annot=False)
plt.show()
#-------------------------------------







