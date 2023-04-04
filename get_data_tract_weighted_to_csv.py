import nibabel as nib
import numpy as np
import csv

# Define the input and output file paths
#input_path = "C:/Users/joujo/Documents/Master_Thesis/Patients/V_18/Arcuate_Fasciculus/Arcuate_Fac_Left_tresh19_V_18_.trk"
output_path= "C:/Users/joujo/Documents/Master_Thesis/Patients/V_18/Arcuate_Fasciculus/Arcuate_Fac_Left2.csv"
#fa_path = "C:/Users/joujo/Documents/Master_Thesis/Patients/V_18/V_18_FA.nii.gz"



patientList=["V_18","H_3"]
root="C:/Users/joujo/Documents/Master_Thesis/Patients/"

all_stats = []

for i in range (len(patientList)):
    fa_path=root+patientList[i]+"/"+patientList[i]+"_FA.nii.gz"
    input_path=root+patientList[i]+"/Arcuate_Fasciculus/Arcuate_Fac_Left_tresh19_"+patientList[i]+"_.trk"

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
    
    # Compute the FA-weighted statistics
    weights = np.zeros(len(fa_values))
    for fv in range(len(fa_values)):
        weights[fv] = fa_values[fv] * streamline_lengths[fv]
    mean_fa = np.average(fa_values, weights=weights)
    max_fa = np.max(fa_values)
    min_fa = np.min(fa_values)
    std_fa = np.sqrt(np.average((fa_values - mean_fa)**2, weights=weights))
    num_streamlines = len(streamlines)
    
    all_stats.append([patientList[i], mean_fa, max_fa, min_fa, std_fa, num_streamlines])
    
    # Write the statistics to a CSV file
with open(output_path, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['patient', 'mean_FA', 'max_FA', 'min_FA', 'std', 'TrackCount'])
    for stats in all_stats:
        writer.writerow(stats)

print('Statistics exported to', output_path)
