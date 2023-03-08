# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:40:52 2022

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 11:31:30 2022

@author: joujo
"""

#root='C:/Users/nicol/Desktop/Dyslexic_Sample/'

#root = "C:/Users/joujo/Documents/"
#root='/CECI/proj/pilab/dyslexia_delilab/data_final/subjects/'

pre_dir='/dMRI/preproc/'
tra_dir='/dMRI/tracking/'

import os
import json
import numpy as np
import nibabel as nib
from dipy.io import read_bvals_bvecs
from dipy.core.gradients import gradient_table
from dipy.io.image import load_nifti, load_nifti_data
from dipy.reconst.csdeconv import (ConstrainedSphericalDeconvModel,auto_response_ssst)
from dipy.tracking import utils
from dipy.tracking.local_tracking import LocalTracking
from dipy.tracking.utils import target
from dipy.tracking.streamline import Streamlines
from dipy.tracking.stopping_criterion import ThresholdStoppingCriterion
from dipy.segment.mask import median_otsu

#f=open(root+'subj_list.json', "r")
#f=open(root, "r")
#PatientList=json.load(f)



#params={'fa_thr':.7,'gfa_thresh':.35,'max_angle':15,'step_size':1}
params={'fa_thr':.6,'gfa_thresh':.35,'max_angle':15,'step_size':.5}

root="C:/Users/joujo/Documents/Master_Thesis/Patients/"
folder="H_3/"
filename="H_3"
#root+folder+"/raw/"+filename+"_raw_dmri.nii.gz"
pathway=root+folder+"raw/"+filename

data, affine, img = load_nifti(pathway+"_raw_dmri.nii.gz" , return_img=True)
bvals, bvecs = read_bvals_bvecs(pathway+"_raw_dmri.bval", pathway+"_raw_dmri.bvec")
gtab = gradient_table(bvals, bvecs,atol=1)
    
mask_data, white_matter = median_otsu(data, vol_idx=[0, 1], median_radius=4, numpass=2,
                                 autocrop=False, dilate=1)
seeds = utils.seeds_from_mask(white_matter, affine, density=1)
    
    #default fa_thr =0.7
response, ratio = auto_response_ssst(gtab, data, roi_radii=10, fa_thr=params['fa_thr'])
csd_model = ConstrainedSphericalDeconvModel(gtab, response, sh_order=6)
csd_fit = csd_model.fit(data, mask=white_matter)
    
from dipy.reconst.shm import CsaOdfModel
    
csa_model = CsaOdfModel(gtab, sh_order=6)
gfa = csa_model.fit(data, mask=white_matter).gfa
stopping_criterion = ThresholdStoppingCriterion(gfa, params['gfa_thresh'])
    
from dipy.direction import ProbabilisticDirectionGetter
from dipy.io.stateful_tractogram import Space, StatefulTractogram
from dipy.io.streamline import save_trk
    
    # SH
from dipy.data import default_sphere
    
prob_dg = ProbabilisticDirectionGetter.from_shcoeff(csd_fit.shm_coeff,
                                                        max_angle=params['max_angle'],
                                                        sphere=default_sphere)
    
streamline_generator = LocalTracking(prob_dg, stopping_criterion, seeds,
                                         affine, step_size=params['step_size'])
streamlines = Streamlines(streamline_generator)
    
sft = StatefulTractogram(streamlines, img, Space.RASMM)
    
#if not os.path.isdir(root+PatientList+tra_dir):
 #   os.mkdir(root+PatientList+tra_dir)
    
save_filename='_whole_brain2_'
#name="V_2"
    
save_trk(sft, root+folder+save_filename+filename+'.trk')
    
with open(root+filename+'.txt', 'w') as outfile:
    json.dump(params, outfile)
