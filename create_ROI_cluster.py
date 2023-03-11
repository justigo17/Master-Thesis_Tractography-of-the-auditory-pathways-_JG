# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 10:06:02 2023

@author: joujo
"""

#meme chose que create_ROI mais pour les clusters




import nibabel as nib
from registration import get_transform, apply_transform




def create_ROI(patientList,root,ROI_list,name_list,threshold):
    for i in patientList:
        print(i)
        folder=i+"/"
        filename=i
        
        static_file=root+folder+"/dMRI/microstructure/dti/"+filename+'_FA.nii.gz'
        moving_file="/home/users/j/g/jgoosse/FSL_HCP1065_FA_1mm.nii.gz"
        
        mapping=get_transform(static_file, moving_file,diffeomorph=False,sanity_check=True)
        apply_transform(moving_file, mapping,static_file,output_path=root+folder+"/transform.nii.gz")
         
         
         
        for i in range(len(ROI_list)):
            apply_transform(ROI_list[i], mapping, static_file, output_path=root+folder+name_list[i]+"_TEST_natif.nii.gz", binary = True,
                   binary_thresh = threshold)
        
        
    return 
    
    



patientList=["V_2","V_3","V_4","V_5","V_6","V_7","V_8","V_9","V_10","V_11","V_13","V_14","V_15","V_16","V_17",
             "V_18","V_19","V_20","V_21","V_22","V_23","V_24","V_25","V_26","V_27","V_28","V_29","V_30","V_31",
             "V_32","V_33","V_34","V_35","V_36","V_37","V_38","V_39","V_40","V_41","V_42","V_43","V_44","V_45",
             "V_46","V_47","V_48","V_49","V_50","V_51","V_52","V_53","C_0","C_1","C_2","C_3","C_4","C_5","C_6","C_7",
             "C_8","C_9","C_10","C_11","C_12","H_0","H_1","H_2","H_3","H_4","H_5","H_6"]

root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"


atlas_root_cluster="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/Atlas_Maps"



ROI_list_cluster=[atlas_root_cluster +"/mni_prob_Occipital_Lobe.nii.gz",
          atlas_root_cluster +"/harvardoxford-cortical_prob_Planum_Temporale.nii.gz"]


name_list=["planum_temporale","pole_occipital"]
threshold=0.5

#0.5 value by default of threshold if 90 does not work
create_ROI(patientList, root_cluster, ROI_list_cluster, name_list,threshold)
    


    
