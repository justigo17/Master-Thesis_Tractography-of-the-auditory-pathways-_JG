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


root_home="C:/Users/joujo/Documents/Master_Thesis/Patients/"


atlas_root_home="C:/Users/joujo/Documents/Master_Thesis/Atlas_Maps"


exclude_list=["C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/TRONC_CER_TEST2natif.nii.gz"]

include_list=["C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/WM_L_TEST2natif.nii.gz",
              "C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/WM_R_TEST2natif.nii.gz",
              ]

match_tracto(patientList, root_home, include_list, exclude_list)











root="C:/Users/joujo/Documents/Master_Thesis/Patients/"
folder="H_3/"
filename="H_3"
#root+folder+"/raw/"+filename+"_raw_dmri.nii.gz"
pathway=root+folder+"raw/"+filename
data, affine, img = load_nifti(pathway+"_raw_dmri.nii.gz" , return_img=True)


white_mat_l=nib.load("C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/left_wm_test_natif.nii.gz").get_fdata()

white_mat_r=nib.load("C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/rigth_wm_test_natif.nii.gz").get_fdata()

tronc_cereb=nib.load("C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/tronc_cereb_test_natif.nii.gz").get_fdata()

tract_file= "C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/_whole_brain_H_3.trk"

trk=load_tractogram(tract_file,'same')
#trk.to_vox()
#trk.to_corner()

streamlines=trk.streamlines

test_ones=np.ones(tronc_cereb.shape)

streamlines=target(streamlines,affine,white_mat_l,include=True)
streamlines=target(streamlines,affine,white_mat_r,include=True)

streamlines=target(streamlines,affine,tronc_cereb,include=False)


tract=StatefulTractogram(streamlines, img,Space.RASMM)


save_trk(tract, "C:/Users/joujo/Documents/Master_Thesis/Patients/H_3/TEST/test_full.trk")


#track_count= len(trk.streamlines._offsets)
     