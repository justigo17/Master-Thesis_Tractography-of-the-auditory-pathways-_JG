# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 09:48:01 2023

@author: joujo
"""

#fonction qui crée les ROI

import nibabel as nib
from registration import get_transform, apply_transform


#function pour cluster, si local changer les liens d'accces


def create_ROI(patientList,root,ROI_list,name_list):
    for i in patientList:
        folder=i+"/"
        filename=i
        
        #static_file=root+folder+"/dMRI/microstructure/dti/"+filename+'_FA.nii.gz'
        #moving_file="/home/users/j/g/jgoosse/FSL_HCP1065_FA_1mm.nii.gz"
        
        static_file=root+folder+filename+'_FA.nii.gz'

        moving_file=root+"FSL_HCP1065_FA_1mm.nii.gz"
        
        mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)
        apply_transform(moving_file, mapping,static_file,output_path=root+folder+"/transform.nii.gz")
         
         
         
        for i in range(len(ROI_list)):
            apply_transform(ROI_list[i], mapping, static_file, output_path=root+folder+name_list[i]+"_TEST2natif.nii.gz", binary = True,
                   binary_thresh = 90)
        
        
    return 
    
    






patientList=["H_3"]


root_home="C:/Users/joujo/Documents/Master_Thesis/Patients/"


atlas_root_home="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps"


ROI_list=[atlas_root_home +"/Harvard/harvardoxford-subcortical_prob_Right Cerebral White Matter.nii.gz",
          atlas_root_home +"/Harvard/harvardoxford-subcortical_prob_Left Cerebral White Matter.nii.gz",
          atlas_root_home+"/Harvard/harvardoxford-subcortical_prob_Brain-Stem.nii.gz"]

name_list=["WM_R","WM_L","TRONC_CER"]

create_ROI(patientList, root_home, ROI_list, name_list)
    
    