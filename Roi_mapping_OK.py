# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:48:40 2023

@author: joujo
"""



import nibabel as nib
from registration import get_transform, apply_transform



root="C:/Users/joujo/Documents/Master_Thesis/Patients/"
folder="C_1/"
filename="C_1"
#root+folder+filename+'_FA.nii.gz'

#static_file="C:/Users/joujo/Documents/Master_Thesis/Patients/V_2_FA.nii.gz"
static_file=root+folder+filename+'_FA.nii.gz'
#moving_file = "C:/Users/joujo/Documents/Master_Thesis/Patients/FSL_HCP1065_FA_1mm.nii.gz"
moving_file=root+"FSL_HCP1065_FA_1mm.nii.gz"

mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)

apply_transform(moving_file, mapping,static_file,output_path=root+folder+"/transform.nii.gz")



#for 1 zone 

#ROI_file="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/Atlas_Maps/XTRACT/xtract_prob_Forceps_Major.nii.gz"
#apply_transform(ROI_file, mapping,static_file,output_path="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/2test21fev.nii.gz"
              #  ,binary=True)

#ROI_file="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps/Harvard/harvardoxford-subcortical_prob_Brain-Stem.nii.gz"
ROI_file="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps/Harvard/harvardoxford-subcortical_prob_Brain-Stem.nii.gz"


apply_transform(ROI_file, mapping,static_file,output_path=root+folder+"/tronc_cereb_test.nii.gz",binary = True)



#from 2 zone 
#/Harvard/harvardoxford-subcortical_prob_Left Cerebral White Matter.nii.gz


atlas_root="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps"
ROI_list=[atlas_root +"/Harvard_cortex/harvardoxford-cortical_prob_Occipital_Pole.nii.gz",
          atlas_root +"/Harvard_cortex/harvardoxford-cortical_prob_Heschl_Gyrus.nii.gz"]


name_list=["Pole_Occipitale","New_Gyrus_Hesch"]

  
for i in range(len(ROI_list)):
    apply_transform(ROI_list[i], mapping, static_file, output_path=root+folder+name_list[i]+"_natif.nii.gz" ,binary = True)#,
    #               binary_thresh = 90)
    






root="C:/Users/joujo/Documents/Master_Thesis/Patients/"
folder="H_3/"
filename="H_3"

static_file=root+folder+filename+'_FA.nii.gz'

moving_file=root+"FSL_HCP1065_FA_1mm.nii.gz"

mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)

apply_transform(moving_file, mapping,static_file,output_path=root+folder+"/transform.nii.gz")



atlas_root="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps"
ROI_list=[atlas_root +"/Harvard/harvardoxford-subcortical_prob_Right Cerebral White Matter.nii.gz",
          atlas_root +"/Harvard/harvardoxford-subcortical_prob_Left Cerebral White Matter.nii.gz",
          atlas_root+"/Harvard/harvardoxford-subcortical_prob_Brain-Stem.nii.gz"]


name_list=["rigth_wm_test","left_wm_test","tronc_cereb_test"]

  
for i in range(len(ROI_list)):
    apply_transform(ROI_list[i], mapping, static_file, output_path=root+folder+name_list[i]+"_natif.nii.gz" ,binary = True,
              binary_thresh = 90)
    

