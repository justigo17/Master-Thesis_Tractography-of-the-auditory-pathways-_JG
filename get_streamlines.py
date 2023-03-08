# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:34:22 2023

@author: joujo
"""


from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram, save_trk
import nibabel as nib
import numpy as np
import csv 
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.image import load_nifti, load_nifti_data
from dipy.tracking.utils import target





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
    