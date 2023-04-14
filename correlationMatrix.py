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


#data = pd.read_excel ('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/PatientCorrel.xlsx')

data2=pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/Correlation2emepart.xlsx')

data = pd.read_excel("C:/Users/joujo/Documents/Master_Thesis/Prediction/Correlation.xlsx")
print(data2)
df = pd.DataFrame(data2)
print(df)

df.drop([12,13,14,15,16,17], axis=0, inplace=True)
print(df)

correaltion=df.corr()

corrM2 = df.corr()
print(corrM2)
plt.figure(figsize=(12, 12))
sns.heatmap(corrM2, annot=True)
plt.show()



print(data)

print(data.tail(3))
print(data.iloc[:,21:33]  )

data_drop_it_all = data.dropna()

print(data_drop_it_all.shape)
print(data_drop_it_all)

df = pd.DataFrame(data_drop_it_all)
print(df)

df2=pd.DataFrame(data)

df2.drop([5], axis=0, inplace=True)
print(df2)
print(df2.shape)



corrM2=df2.corr()
print(corrM2)










orrM = df.corr()
print(corrM)



plt.figure(figsize=(35, 35))
sns.heatmap(corrM2, annot=True)
plt.show()


print(data.shape)
print(data.head(2))

print(data.info)
data.info()
print(data.columns)
print(data.shape)

 data = pd.read_csv('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/adults_1.csv',usecols=[10,11,12,13])