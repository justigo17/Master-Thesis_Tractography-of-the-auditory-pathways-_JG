# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:39:47 2023

@author: joujo
"""

#fonction qui crée utilise la tracto du whole brain et ajoute des ROI d'exclusion/d'inclusion


from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram, save_trk
import nibabel as nib
import numpy as np
import csv 
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.image import load_nifti, load_nifti_data
from dipy.tracking.utils import target




def match_tracto(patientList,root,include_list,exclude_list ):#          ,dilate):
    for i in patientList:
        folder=i+"/"
        filename=i
        pathway=root+folder+"raw/"+filename
        data, affine, img = load_nifti(pathway+"_raw_dmri.nii.gz", return_img=True)
        
        tract_file=root+folder+"_whole_brain_"+filename+".trk"
        trk=load_tractogram(tract_file,'same')
        
        streamlines=trk.streamlines
        
        
        #white_mat_l=nib.load(include_list[0]).get_fdata()
        #streamlines=target(streamlines,affine,white_mat_l,include=True)
        
        
        for roi_in in include_list:
            zone=nib.load(roi_in).get_fdata()
            streamlines=target(streamlines,affine,zone,include=True)
            
        for roi_out in exclude_list:
            zone=nib.load(roi_out).get_fdata()
            streamlines=target(streamlines,affine,zone,include=False)
        

        tract=StatefulTractogram(streamlines, img,Space.RASMM)
        save_trk(tract, root+folder+"Test2_"+filename+"_.trk")
               
    
    return     
        


patientList=["H_3","V_2"]#,"C_1"]


root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"



for patient in patientList:


    exclude_list=["/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/tronc_cerebral.nii.gz"]

    include_list=["/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/Left_wm_natif.nii.gz",
              "/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"+patient+"/Right_wm_natif.nii.gz"
              ]

    match_tracto(patientList, root_cluster, include_list, exclude_list)




