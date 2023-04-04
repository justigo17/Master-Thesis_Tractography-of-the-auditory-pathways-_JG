# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 17:00:23 2023

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 12:15:15 2023

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:09:03 2023

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


#data = pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/bestPatientEvol.xlsx')
data=pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/Prediction/prediction_patients.xlsx')

#print(data)
df = pd.DataFrame(data)

patientList=df['patient_id']
#print(patientList)

print(df.columns)

print(df["M6_CAP"])
 
cap=df["M6_CAP"]
print(type(cap[2]))

CAP_good=[]
patient_good=[]
CAP_bad=[]
patient_bad=[]


print(patientList)

for i in range (len(cap)):
    print(cap[i])
    #print(Ac_evol[i])
    if (np.isnan(cap[i])!=True ):
        if (cap[i]>6):
            CAP_good.append(cap[i])
            patient_good.append(patientList[i])
        elif (cap[i]<6):
            CAP_bad.append(cap[i])
            patient_bad.append(patientList[i])

print(len(CAP_good))
print(len(CAP_bad))
print(patient_good)
print(patient_bad)


fig, ax = plt.subplots()
#ax.plot(patientList.dropna(), Ac_evol,'.')
plt.bar(patient_good, CAP_good, align='center', alpha=0.5)
#plt.axhline(y=np.nanmedian(Ac_evol))
plt.xticks(rotation=90)
#print(AcmaxListPatient)

plt.bar(patient_bad,CAP_bad, align='center', alpha=0.5, color="orange")
#plt.axhline(y=np.nanmedian(Ac_evol))
plt.xticks(rotation=90)
#print(AcminListPatient)



#fillna([value, method, axis, inplace, ...]) 



#18 NAN CAP ET 6 CAP=6 --> 61 -24 = 37 (19 GOOD ET 18 BAD )
