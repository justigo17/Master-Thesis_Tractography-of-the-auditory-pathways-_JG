# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 17:00:23 2023

@author: joujo
"""

# -*- coding: utf-8 -*-


#correlation matrix 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

#18 NAN CAP ET 6 CAP=6 --> 61 -24 = 37 (19 GOOD ET 18 BAD )-6 qui beug =31 (14 GOOD et 17BAD)

file_path1="C:/Users/joujo/Documents/Master_Thesis/Prediction/Arcuate_Fac_Left_V1.xlsx"
file_path2="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Body.xlsx"
file_path3="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Genu.xlsx"
file_path4="C:/Users/joujo/Documents/Master_Thesis/Prediction/CC_Splenium.xlsx"
file_path5="C:/Users/joujo/Documents/Master_Thesis/Prediction/Uncinate_Fasciculus_L.xlsx"
file_path6="C:/Users/joujo/Documents/Master_Thesis/Prediction/Uncinate_Fasciculus_R.xlsx"

file_path7="C:/Users/joujo/Documents/Master_Thesis/Prediction/IFOF_L.xlsx"
file_path8="C:/Users/joujo/Documents/Master_Thesis/Prediction/IFOF_R.xlsx"
#data = pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/PatientDeaf/bestPatientEvol.xlsx')
#data=pd.read_excel('C:/Users/joujo/Documents/Master_Thesis/Prediction/prediction_patients.xlsx')

data=pd.read_excel(file_path3)

#print(data)
df = pd.DataFrame(data)

patientList=df['patient']
meanList=df['mean_FA']
maxList=df["max_FA"]
minList=df["min_FA"]
stdList=df["std"]
tractCountList=df["TrackCount"]
#print(patientList)

print(df.columns)

print(df["M6_CAP"])
 
cap=df["M6_CAP"]
print(type(cap[2]))

CAP_good=[]
patient_good=[]
mean_good=[]
min_good=[]
max_good=[]
std_good=[]
tractCount_good=[]

CAP_bad=[]
patient_bad=[]
mean_bad=[]
min_bad=[]
max_bad=[]
std_bad=[]
tractCount_bad=[]


print(patientList)

for i in range (len(cap)):
    print(cap[i])
    #print(Ac_evol[i])
    if (np.isnan(cap[i])!=True ):
        if (cap[i]>6):
            CAP_good.append(cap[i])
            patient_good.append(patientList[i])
            mean_good.append(meanList[i])
            max_good.append(maxList[i])
            min_good.append(minList[i])
            std_good.append(stdList[i])
            tractCount_good.append(tractCountList[i])
        elif (cap[i]<6 and cap[i]>0):
            CAP_bad.append(cap[i])
            patient_bad.append(patientList[i])
            mean_bad.append(meanList[i])
            max_bad.append(maxList[i])
            min_bad.append(minList[i])
            std_bad.append(stdList[i])
            tractCount_bad.append(tractCountList[i])

print(len(CAP_good))
print(len(CAP_bad))
print(patient_good)
print(patient_bad)

print(CAP_good)

print(tractCount_good)
#6 ou CAP =6
#18 OU PAS DE VAL DE CAP


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

#---------------------STATS------------------------------------------




print(np.var(max_good), np.var(max_bad))


stats.ttest_ind(a=tractCount_good, b=tractCount_bad, equal_var=True)
#Ttest_indResult(statistic=0.4799733207398626, pvalue=0.6348468714892954)
#Here, since the p-value (0.6348468714892954) is greater than alpha = 0.05 
#so we cannot reject the null hypothesis of the test. 
#We do not have sufficient evidence to say that the mean height 
#of students between the two data groups is different. (cf example)
#fillna([value, method, axis, inplace, ...]) 

stats.ttest_ind(a=mean_good, b=mean_bad, equal_var=True)
#Ttest_indResult(statistic=-1.1969318381376752, pvalue=0.24102646576746756)

stats.ttest_ind(a=min_good, b=min_bad, equal_var=True)
#Ttest_indResult(statistic=0.5239964575414716, pvalue=0.6042631167591591)

stats.ttest_ind(a=max_good, b=max_bad, equal_var=True)
#Ttest_indResult(statistic=-2.015141124016517, pvalue=0.053242887738199976)


fig, ax = plt.subplots()
#ax.plot(patientList.dropna(), Ac_evol,'.')
plt.bar(patient_good, max_good, align='center', alpha=0.5)
#plt.axhline(y=np.nanmedian(Ac_evol))
plt.xticks(rotation=90)
#print(AcmaxListPatient)

plt.bar(patient_bad,max_bad, align='center', alpha=0.5, color="orange")
#plt.axhline(y=np.nanmedian(Ac_evol))
plt.xticks(rotation=90)
#print(AcminListPatient)

print(np.mean(max_bad))
print(np.mean(max_good))

#------------------BOX PLOT --------------------------------
#plt.boxplot([mean_good, mean_bad])
#pyplot.ylim(0, 14)
plt.title("Max FA value")

labels = ['CAP>6', 'CAP<6']
data=[max_good, max_bad]

bp = plt.boxplot(data, patch_artist = True,labels=labels)


colors = ['pink', 'lightgreen']#, 'lightblue','lemonchiffon']
for bplot in (bp):
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

plt.title("Max FA value Splenium CC")
#plt.xlabel("two groups")
plt.ylabel("max FA value")

#plt.savefig("5-Boite à moustache+ Déphasaga_CD_AxeX_4cas")

