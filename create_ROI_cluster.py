# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:06:02 2023

@author: joujo
"""

#meme chose que create_ROI mais pour les clusters




import nibabel as nib
from registration import get_transform, apply_transform




def create_ROI(patientList,root,ROI_list,name_list):
    for i in patientList:
        folder=i+"/"
        filename=i
        
        static_file=root+folder+"/dMRI/microstructure/dti/"+filename+'_FA.nii.gz'
        moving_file="/home/users/j/g/jgoosse/FSL_HCP1065_FA_1mm.nii.gz"
        
        mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)
        apply_transform(moving_file, mapping,static_file,output_path=root+folder+"/transform.nii.gz")
         
         
         
        for i in range(len(ROI_list)):
            apply_transform(ROI_list[i], mapping, static_file, output_path=root+folder+name_list[i]+"_TESTnatif.nii.gz", binary = True,
                   binary_thresh = 90)
        
        
    return 
    
    






patientList=["H_3"]

root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"


atlas_root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/Atlas_Maps"



ROI_list_cluster=[atlas_root_cluster +"/mni_prob_Occipital_Lobe.nii.gz",
          atlas_root_cluster +"/harvardoxford-cortical_prob_Heschl_Gyrus.nii.gz"]


name_list=["WM_R","WM_L","TRONC_CER"]

create_ROI(patientList, root_home, ROI_list, name_list)
    
    