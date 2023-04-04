# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 18:06:46 2023

@author: joujo
"""

from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram, load_trk
import nibabel as nib
import numpy as np
import csv 
import pandas as pd
from TIME.core import tract_to_streamlines, compute_subsegments

df1 = pd.DataFrame(columns=['patient','TrackCount','mean_FA','min_FA','max_FA',"std"])

patientList2= ["C_0","C_1","C_10","C_11","C_12","C_12","C_3","C_4","C_6","C_7",
              "C_8","C_9","H_0","H_1","H_2","H_3","H_5","V_0","V_10","V_11","V_12",
              "V_15","V_16","V_17","V_2","V_20","V_23","V_24","V_25","V_26","V_27",
              "V_28","V_29","V_3","V_30","V_31","V_33","V_35","V_36","V_37","V_38",
              "V_39","V_4","V_40","V_42","V_43","V_44","V_45","V_46","V_47","V_48",
              "V_49","V_5","V_50","V_51","V_52","V_53","V_6","V_7","V_8","V_9"]




patientList=["V_18"]#,"V_2","H_3"]V_18"

print(len(patientList))

patient=pd.Series(0, index = range(len(patientList)))
TrackCount=pd.Series(0, index = range(len(patientList)))
mean_FA=pd.Series(0, index = range(len(patientList)))
minFA=pd.Series(0, index = range(len(patientList)))
maxFA=pd.Series(0, index = range(len(patientList)))
STD=pd.Series(0, index = range(len(patientList)))

root="C:/Users/joujo/Documents/Master_Thesis/Patients/"

#V_15/CorpsCalleux/Test2_V_15_.trk


for i in range (len(patientList)):
   
    
   
    tract_file=root+patientList[i]+"/Arcuate_Fasciculus/Arcuate_Fac_Left_tresh19_"+patientList[i]+"_.trk"
    
    #print(tract_file)
    #/Arcuate_Fasciculus/Arcuate_Fac_Left_tresh19_V_18_.trk
    #tract_file= root+patientList[i]+"/CorpsCalleux/Test2_"+patientList[i]+"_.trk"
    #tract_file= root+patientList[i]+"/CorpsCalleux/CorpsCalleux2.trk"
    #"C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/CorpsCalleux2.trk"
    ROI=tract_to_ROI(tract_file)
    
    


    image=nib.load(root+patientList[i]+"/"+patientList[i]+"_FA.nii.gz")

    FA=image.get_fdata()
    print(len(FA))
    

   

    mean=np.mean(FA[ROI>0]*ROI[ROI>0])
    print(mean)
    
    std=np.std(FA[ROI>0]*ROI[ROI>0])
    maximum=np.max(FA[ROI>0]*ROI[ROI>0])
    minimum =np.min(FA[ROI>0]*ROI[ROI>0])
    print(std)


    trk=load_tractogram(tract_file,'same')
    trk.to_vox()
    trk.to_corner()
    
    dens=get_streamline_density(trk)    
    print(dens)
    
    new_mean=np.mean((FA[ROI*dens>0]*ROI[ROI*dens>0]))#*dens[ROI>0])
    

    track_count= len(trk.streamlines._offsets)
#######-------------------------------------------------------
    
    
    testmean=(np.mean(FA[ROI>0]*ROI[ROI>0]))*(dens)
    testt=(FA[ROI*dens>0]*ROI[ROI*dens>0])
    pp=(ROI[ROI>0]*FA[ROI>0])
    np.mean(FA[ROI>0]*ROI[ROI>0])
    
    new_mean=np.mean((FA[ROI*dens>0]*ROI[ROI*dens>0]))#*dens[ROI>0])
    
    pt=pt[0.25<pt]
    pt=pt[pt<0.75]
    np.mean(pt)
    
    pp=pp[pp!=0]
    
    np.mean(pp)
    
 ###################################---------------------------
    STD[i]=std
    TrackCount[i]=track_count
    mean_FA[i]=mean
    #print(meanFA[i])
    minFA[i]=minimum
    maxFA[i]=maximum
    patient[i]=patientList[i]
    
    
    
    out=nib.Nifti1Image(dens, affine=image.affine,header=image.header)
    #print(out)
    
    out.to_filename("C:/Users/joujo/Documents/Master_Thesis/Patients/V_18/Arcuate_Fasciculus/Arcuate_Fac_density_Av.nii.gz")

  
   # data=np.array([mean , std , maximum , minimum ,track_count])
    #writing.append([patientList[i],data])

df1['TrackCount']=TrackCount
df1['patient']=patient
df1['mean_FA']=mean_FA
df1['min_FA']=minFA
df1['max_FA']=maxFA
df1['std']=STD


print(df1)
#changer
file_name = 'C:/Users/joujo/Documents/Master_Thesis/Prediction/test8.xlsx'

#df1.to_excel(file_name)