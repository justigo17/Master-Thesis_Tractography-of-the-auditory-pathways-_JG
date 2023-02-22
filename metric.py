# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:58:06 2023

@author: joujo
"""

from TIME.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram
import nibabel as nib
import numpy as np


tract_file="C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/occipital_to_superioTemporaGyrus_C1.trk"
ROI=tract_to_ROI(tract_file)

image=nib.load("C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/C_1_FA.nii.gz")

out=nib.Nifti1Image(ROI, affine=image.affine,header=image.header)

out.to_filename("C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/occipital_to_superioTemporaGyrus_C1.nii.gz")

FA=image.get_fdata()

print(np.mean(FA[ROI>0]*ROI[ROI>0]),np.std(FA[ROI>0]*ROI[ROI>0]))

trk=load_tractogram(tract_file,'same')
trk.to_vox()
trk.to_corner()

density= get_streamline_density(trk)

out=nib.Nifti1Image(density, affine=image.affine,header=image.header)

out.to_filename("C:/Users/joujo/Documents/UCL - INGE CIVIL MASTER 2 2022-2023/Q10/Master thesis/occipital_to_superioTemporaGyrus_C1_density.nii.gz")


print(len(trk.streamlines._offsets)) #track count 


