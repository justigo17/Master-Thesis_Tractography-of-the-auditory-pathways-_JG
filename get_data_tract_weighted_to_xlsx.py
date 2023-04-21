# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 20:28:38 2023

@author: joujo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 20:00:39 2023

@author: joujo
"""

import nibabel as nib
import numpy as np
import openpyxl
import nibabel as nib
import numpy as np
import openpyxl
#from TIME.utils import tract_to_ROI, get_streamline_density
from unravel.utils import tract_to_ROI, get_streamline_density
from dipy.io.streamline import load_tractogram, load_trk

def get_data_to_xlsx(patientList,name_tract,output_name):

    # Create a new Excel workbook
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    # Write the header row
    sheet.append(['patient', 'mean_FA','std', 'TrackCount'])
    
    # Loop over all patients and calculate the statistics
    for i in range (len(patientList)):
        
        print(patientList[i])
        fa_path=root+patientList[i]+"/dMRI/microstructure/dti/"+patientList[i]+"_FA.nii.gz"
    
        input_path=root+patientList[i]+"/"+name_tract+"_"+patientList[i]+"_.trk"
    
        # Load the TrackVis file
        tractogram = nib.streamlines.load(input_path)
        streamlines = tractogram.streamlines
    
        # Load the associated FA volume
        fa_volume = nib.load(fa_path)
        affine = fa_volume.affine
        fa_data = fa_volume.get_fdata()
        
        # Compute the FA values and streamline lengths for each streamline
        fa_values = []
        streamline_lengths = []
        for streamline in streamlines:
            voxel_coords = nib.affines.apply_affine(np.linalg.inv(affine), streamline)
            voxel_coords = np.round(voxel_coords).astype(int)
            fa_value = np.mean(fa_data[tuple(voxel_coords.T)])
            if np.isnan(fa_value):
                continue
            fa_values.append(fa_value)
            streamline_lengths.append(np.linalg.norm(np.diff(streamline, axis=0), axis=1))
        fa_values = np.array(fa_values)
        streamline_lengths = np.concatenate(streamline_lengths)
        
        
        trk=load_tractogram(input_path,'same')
        trk.to_vox()
        trk.to_corner()
        dens=get_streamline_density(trk) 
        
        # Compute the FA-weighted statistics
        weights = np.zeros(len(fa_values))
        for fv in range(len(fa_values)):
            weights[fv] = fa_values[fv] * streamline_lengths[fv]
        #mean_fa = np.average(fa_values, weights=weights)
        #max_fa = np.max(fa_values)
        #min_fa = np.min(fa_values)
        
        mean_fa=np.sum(dens*fa_data)/(np.sum(dens)) 
        std_fa = np.sqrt(np.average((fa_values - mean_fa)**2, weights=weights))
        num_streamlines = len(streamlines)
        
        # Write the statistics to the Excel sheet
        sheet.append([patientList[i], mean_fa,std_fa, num_streamlines])
    
    # Save the workbook
    workbook.save(output_path+output_name+".xlsx")
    
    return 



output_path= "/CECI/proj/pilab/PermeableAccess/deaf_MK2aHgx8DTE/study/PatientDeaf_data/"

root="/CECI/proj/pilab/PermeableAccess/vertige_LEWuQhzYs9/Patients/"

patientList=["C_0","C_1","C_10","C_11","C_12","C_2","C_3","C_4","C_6","C_7",
            "C_8","C_9","H_0","H_1","H_2","H_3","H_5","V_10","V_11",
             "V_15","V_17","V_2","V_20","V_23","V_24","V_25","V_26","V_27",
            "V_28","V_29","V_30","V_31","V_33","V_35","V_36","V_37","V_38",
              "V_39","V_4","V_40","V_42","V_43","V_44","V_45","V_47",
              "V_49","V_5","V_50","V_51","V_52","V_53","V_6","V_7","V_8"]
              


name_track="AF_Left2"
output_name="Arcuate_Fac_Left_V2"
#ok

name_trackB="CC_Body"
output_nameB="CC_BodyV2"
#OK 

name_trackG="CC_Genu"
output_nameG="CC_GenuV2"
#OK

name_trackS="CC_Splenium"
output_nameS="CC_SpleniumV2"
#OK


get_data_to_xlsx(patientList,name_trackS,output_nameS)





