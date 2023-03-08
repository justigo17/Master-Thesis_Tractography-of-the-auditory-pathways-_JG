# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:15:48 2023

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:58:06 2023

@author: joujo
"""

from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram
import nibabel as nib
import numpy as np
import csv 

#tract_file="C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/CorpsCalleux.trk"
tract_file="C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/CorpsCalleux2.trk"
#tract_file="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/occipital_to_superioTemporaGyrus_C1.trk"
ROI=tract_to_ROI(tract_file)



image=nib.load("C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/C_1_FA.nii.gz")


FA=image.get_fdata()

mean=np.mean(FA[ROI>0]*ROI[ROI>0])

std=np.std(FA[ROI>0]*ROI[ROI>0]))

maximum=np.max(FA[ROI>0]*ROI[ROI>0])
minimum =np.min(FA[ROI>0]*ROI[ROI>0]))

tract_file= "C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/_whole_brain2.trk "

trk=load_tractogram(tract_file,'same')
trk.to_vox()
trk.to_corner()

track_count= len(trk.streamlines._offsets)


#write

patientList=["V_2","V_3","V_4","V_5","V_6","V_7","V_8","V_9","V_10","V_11","V_13",
             "V_14","V_15","V_16","V_17","V_18","V_19","V_20","V_21","V_22","V_23",
             "V_24","V_25","V_26","V_27","V_28","V_29","V_30","V_31","V_32","V_33",
             "V_34","V_35","V_36","V_37","V_38","V_39","V_40","V_41","V_42","V_43",
             "V_44","V_45","V_46","V_47","V_48","V_49","V_50","V_51","V_52","V_53",
             "C_0","C_1","C_2","C_3","C_4","C_5","C_6","C_7","C_8","C_9","C_10",
             "C_11","C_12","H_0","H_1","H_2","H_3","H_4","H_5","H_6"]


writing=[]
#f = open('C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/test.csv', 'w')
root="C:/Users/joujo/Documents/Master_Thesis/Patients/"

for i in range (len(patientList)):
    
    
    tract_file= root+patientList[i]+"/CorpsCalleux/CorpsCalleux2.trk"
    #"C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/CorpsCalleux2.trk"
    ROI=tract_to_ROI(tract_file)

    image=nib.load(root+patientList[i]+"/"+patientList[i]+"_FA.nii.gz")

    FA=image.get_fdata()

    mean=np.mean(FA[ROI>0]*ROI[ROI>0])
    std=np.std(FA[ROI>0]*ROI[ROI>0])
    maximum=np.max(FA[ROI>0]*ROI[ROI>0])
    minimum =np.min(FA[ROI>0]*ROI[ROI>0])

    trk=load_tractogram(tract_file,'same')
    trk.to_vox()
    trk.to_corner()

    track_count= len(trk.streamlines._offsets)
    

    data=np.array([mean , std , maximum , minimum ,track_count])
    writing.append([patientList[i],data])
    

    
    with open('C:/Users/joujo/Documents/Master_Thesis/Patients/C_1/CorpsCalleux/test.csv', 'w') as f:
        
        writer = csv.writer(f)
        # nos headers/en-têtes
        headers = ["patient","mean", "std", "max", "min","track_count"]
        
        writer.writerow(headers)
        # On utilise writerows() et pas writerow()
        writer.writerows(writing)


print(len(trk.streamlines._offsets)) #track count 




C:/Users/joujo/Documents/Master_Thesis/Patients/V_2/CorpsCaleux/CorpsCalleux2.trk
C:/Users/joujo/Documents/Master_Thesis/Patients/V_2/CorpsCalleux/CorpsCalleux2.trk'


