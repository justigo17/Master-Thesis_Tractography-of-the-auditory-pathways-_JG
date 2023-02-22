# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 14:55:26 2023

@author: joujo
"""

import nibabel as nib
from registration import get_transform, apply_transform


static_file="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/C_1_FA.nii.gz"
moving_file = "C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/Atlas_Maps/FSL_HCP1065_FA_1mm.nii.gz"

mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)

apply_transform(moving_file, mapping,static_file,output_path="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/test21fev.nii.gz")


ROI_file="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/Atlas_Maps/XTRACT/xtract_prob_Forceps_Major.nii.gz"
apply_transform(ROI_file, mapping,static_file,output_path="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/2test21fev.nii.gz"
                ,binary=True)



#from 2 zone 

atlas_root="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/Atlas_Maps"
ROI_list=[atlas_root +"/Lobes/mni_prob_Occipital_Lobe.nii.gz",
          atlas_root +"/Harvard_cortex/harvardoxford-cortical_prob_Superior_Temporal_Gyrus_posterior.nii.gz"]

for ROI in ROI_list :
    apply_transform(ROI, mapping,static_file,output_path=ROI[:-7]+"_natif.nii.gz",
                    binary=True)