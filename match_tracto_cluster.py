# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:39:47 2023

@author: joujo
"""

#fonction qui crée utilise la tracto du whole brain et ajoute des ROI d'exclusion/d'inclusion


#from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram, save_trk
import nibabel as nib
import numpy as np
import csv 
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.image import load_nifti, load_nifti_data
from dipy.tracking.utils import target




def match_tracto(patientList,root,include_list,exclude_list ):#          ,dilate):
    for i in patientList:
        print(i)
        folder=i+"/"
        filename=i
        pathway=root+folder+"dMRI/raw/"+filename
        data, affine, img = load_nifti(pathway+"_raw_dmri.nii.gz", return_img=True)
        
        
        tract_file=root+folder+"_whole_brain_"+filename+".trk"
        trk=load_tractogram(tract_file,'same')
        
        streamlines=trk.streamlines
        
        
        for roi_in in include_list:
            zone=nib.load(roi_in).get_fdata()
            streamlines=target(streamlines,affine,zone,include=True)
            
        for roi_out in exclude_list:
            zone=nib.load(roi_out).get_fdata()
            streamlines=target(streamlines,affine,zone,include=False)
        

        tract=StatefulTractogram(streamlines, img,Space.RASMM)
        save_trk(tract, root+folder+"Test2_"+filename+"_.trk")
               
    
    return     
        


patientList=["V_3","V_4","V_5","V_6","V_7","V_8","V_9","V_10","V_11",
             "V_13","V_14","V_15","V_16","V_17","V_18","V_19","V_20",
             "V_21","V_22","V_23","V_24","V_25","V_26","V_27","V_28",
             "V_29","V_30","V_31","V_32","V_33","V_34","V_35","V_36",
             "V_37","V_38","V_39","V_40","V_41","V_42","V_43","V_44",
             "V_45","V_46","V_47","V_48","V_49","V_50","V_51","V_52",
             "V_53","C_0","C_2","C_3","C_4","C_5","C_6","C_7","C_8",
             "C_9","C_10","C_11","C_12","H_0","H_1","H_2","H_3","H_4","H_5","H_6"]



root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"




for patient in patientList:


    exclude_list=["/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/tronc_cerebral.nii.gz"]

    include_list=["/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/Left_wm_natif.nii.gz",
              "/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/Right_wm_natif.nii.gz"
              ]

    match_tracto(patientList, root_cluster, include_list, exclude_list)




