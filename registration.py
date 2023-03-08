# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 09:43:14 2021

@author: DELINTE Nicolas

The objective of this script is to provide functions that facilitate the
obtention registered ROIs from a hand drawn ROI to another subject space.
Ex: longitudinal registration of hand-drawn ROIs

Also, functions that allow to register metric maps to longitudinal maps of the
same patient.

"""

# Imports

import os
import numpy as np
import nibabel as nib
from dipy.viz import regtools
from dipy.io.image import load_nifti
from dipy.align.imaffine import (transform_centers_of_mass,
                                 AffineMap,
                                 MutualInformationMetric,
                                 AffineRegistration)
from dipy.align.transforms import (TranslationTransform3D,
                                   RigidTransform3D,
                                   AffineTransform3D)
from dipy.align.imwarp import SymmetricDiffeomorphicRegistration
from dipy.align.metrics import CCMetric

# Functions


def get_transform(static_volume_file: str, moving_volume_file: str,
                  onlyAffine: bool = False, diffeomorph: bool = True,
                  sanity_check: bool = False, normalize: bool = False):
    '''
    If volume are 4D+, only first 3D volume is taken into account.

    Parameters
    ----------
    static_volume_file : str
        3D array of static volume.
    moving_volume_file : str
        3D array of moving volume.
    onlyAffine : bool, optional
        DESCRIPTION. The default is False.
    diffeomorph : bool, optional
        If False then registration is only affine. The default is True.
    sanity_check : bool, optional
        If True then prints figures. The default is False.
    normalize : bool, optional
        If True, both volume are normalized before registration. This parameter
        improves robustness of registration. The default is False.

    Returns
    -------
    mapping : TYPE
        transform operation to send moving_volume to static_volume space.

    '''

    static, static_affine = load_nifti(static_volume_file)
    static_grid2world = static_affine
    if len(static.shape) > 3:
        static = static[:, :, :, 0]

    moving, moving_affine = load_nifti(moving_volume_file)
    moving_grid2world = moving_affine
    if len(moving.shape) > 3:
        moving = moving[:, :, :, 0]

    if normalize:
        static = static/np.max(static)
        moving = moving/np.max(moving)

    # Affine registration -----------------------------------------------------

    if sanity_check or onlyAffine:

        identity = np.eye(4)
        affine_map = AffineMap(identity,
                               static.shape, static_grid2world,
                               moving.shape, moving_grid2world)

        if sanity_check:
            resampled = affine_map.transform(moving)

            regtools.overlay_slices(static, resampled, None, 0,
                                    "Static", "Moving", "resampled_0.png")
            regtools.overlay_slices(static, resampled, None, 1,
                                    "Static", "Moving", "resampled_1.png")
            regtools.overlay_slices(static, resampled, None, 2,
                                    "Static", "Moving", "resampled_2.png")

        if onlyAffine:

            return affine_map

    c_of_mass = transform_centers_of_mass(static, static_grid2world,
                                          moving, moving_grid2world)

    nbins = 32
    sampling_prop = None
    metric = MutualInformationMetric(nbins, sampling_prop)

    # !!!
    level_iters = [10000, 1000, 100]
    # level_iters = [1000, 100, 10]
    sigmas = [3.0, 1.0, 0.0]
    factors = [4, 2, 1]
    affreg = AffineRegistration(metric=metric,
                                level_iters=level_iters,
                                sigmas=sigmas,
                                factors=factors)

    transform = TranslationTransform3D()
    params0 = None
    translation = affreg.optimize(static, moving, transform, params0,
                                  static_grid2world, moving_grid2world,
                                  starting_affine=c_of_mass.affine)

    transform = RigidTransform3D()
    rigid = affreg.optimize(static, moving, transform, params0,
                            static_grid2world, moving_grid2world,
                            starting_affine=translation.affine)

    transform = AffineTransform3D()
    affine = affreg.optimize(static, moving, transform, params0,
                             static_grid2world, moving_grid2world,
                             starting_affine=rigid.affine)

    # Diffeomorphic registration --------------------------

    if diffeomorph:

        metric = CCMetric(3)

        level_iters = [10000, 1000, 100]
        sdr = SymmetricDiffeomorphicRegistration(metric, level_iters)

        mapping = sdr.optimize(static, moving, static_affine, moving_affine,
                               affine.affine)

    else:

        mapping = affine

    if sanity_check:

        transformed = mapping.transform(moving)

        regtools.overlay_slices(static, transformed, None, 0,
                                "Static", "Transformed", "transformed.png")
        regtools.overlay_slices(static, transformed, None, 1,
                                "Static", "Transformed", "transformed.png")
        regtools.overlay_slices(static, transformed, None, 2,
                                "Static", "Transformed", "transformed.png")

    return mapping


def apply_transform(file_path: str, mapping, static_file: str = '',
                    output_path: str = '', binary: bool = False,
                    binary_thresh: float = 0.5, inverse: bool = False,
                    mask_file: str = ''):
    '''


    Parameters
    ----------
    file_path : str
        Moving file path.
    mapping : TYPE
        DESCRIPTION.
    static_file : str, optional
        Only necessary if output_path is specified. The default is ''.
    output_path : str, optional
        If entered, saves result at specified location. The default is ''.
    binary : bool, optional
        DESCRIPTION. The default is False.
    binary_thresh : float, optional
        DESCRIPTION. The default is 0.5.
    inverse : bool, optional
        If True, the inverse transformation is applied. The default is False.
    mask_file : str, optional
        If specified, applies a binary mask to moving file before mapping.

    Returns
    -------
    transformed : TYPE
        DESCRIPTION.

    '''

    moving = nib.load(file_path)
    moving_data = moving.get_fdata()

    if len(mask_file) > 0:
        mask = nib.load(mask_file).get_fdata()
        moving_data *= mask

    if inverse:
        transformed = mapping.transform_inverse(moving_data)
    else:
        transformed = mapping.transform(moving_data)

    if binary:
       # transformed[transformed > binary_thresh] = 1
        #transformed[transformed <= binary_thresh] = 0
  
        transformed=np.where(transformed>= binary_thresh,1,0)

    if len(output_path) > 0:

        static = nib.load(static_file)

        out = nib.Nifti1Image(transformed, static.affine, header=static.header)
        out.to_filename(output_path)

    else:

        return transformed


def apply_transformToAllROIsInFolder(Patient_static: str, Patient_moving: str,
                                     mapping, folder: str, static_file: str,
                                     filenameList: list = []):
    '''


    Parameters
    ----------
    Patient_static : str
        DESCRIPTION.
    Patient_moving : str
        DESCRIPTION.
    mapping : TYPE
        transform object.
    folder : str
        folder containing ROIs of Patient_static.
    static_file : str
        DESCRIPTION.
    filenameList : list, optional
        DESCRIPTION. The default is [].

    Returns
    -------
    None.

    '''

    if len(filenameList) == 0:
        filenameList = os.listdir(folder)

    for filename in filenameList:
        if Patient_moving in filename and '.nii' in filename:
            new_filename = filename.replace(Patient_moving, Patient_static)

            apply_transform(folder+filename, mapping, static_file,
                            folder+new_filename, binary=True)


def apply_transformToAllMapsInFolder(input_folder: str, output_folder: str,
                                     mapping, static_file: str,
                                     keywordList: list = [],
                                     inverse: bool = False):
    '''


    Parameters
    ----------
    input_folder : str
        DESCRIPTION.
    output_folder : str
        DESCRIPTION.
    mapping : TYPE
        transform object.
    static_file : str
        DESCRIPTION.
    keywordList : list, optional
        DESCRIPTION. The default is [].
    inverse : bool, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    '''

    for filename in os.listdir(input_folder):
        if all(keyword in filename for keyword in keywordList):

            try:
                apply_transform(input_folder+filename, mapping, static_file,
                                output_folder+filename, binary=False,
                                inverse=inverse)
            except TypeError:
                continue


def saveTTMaps(T0, T1, root: str, outputfolder: str, dirList: list):
    '''
    Saves a metric map registared on T0 containing the diff T1-T0

    Parameters
    ----------
    T0 : TYPE
        DESCRIPTION.
    T1 : TYPE
        DESCRIPTION.
    root : str
        DESCRIPTION.
    outputfolder : str
        DESCRIPTION.
    dirList : list
        DESCRIPTION.

    Returns
    -------
    None.

    '''

    Patient = T0
    metricsT0 = patientMetrics(Patient, dirList)

    Patient = T1
    metricsT1 = patientMetrics(Patient, dirList)

    Patient_static = T0
    Patient_moving = T1

    static_volume_file = root+'DKI/'+Patient_static+'_FA.nii.gz'
    moving_volume_file = root+'DKI/'+Patient_moving+'_FA.nii.gz'

    mapping = get_transform(static_volume_file, moving_volume_file,
                            diffeomorph=True, sanity_check=False)

    dmetrics = {}

    img = nib.load(static_volume_file)

    if not os.path.isdir(outputfolder):
        os.mkdir(outputfolder)

    for metric in list(metricsT0.keys()):

        dmetrics[metric] = (mapping.transform(
            metricsT1[metric])-metricsT0[metric])/metricsT0[metric]*100
        # dmetrics[metric]=(mapping.transform(metricsT1[metric])-metricsT0[metric])

        out = nib.Nifti1Image(dmetrics[metric], img.affine, header=img.header)
        out.to_filename(outputfolder+T0+T1+'_'+metric+'.nii.gz')


if __name__ == '__main__':
    # Script

    # Same patient, different time --------------------------------------

    # root = 'C:/Users/nicol/Documents/Doctorat/Data/Alcool/'
    # Patient_static = 'PAT1'
    # Patient_moving = 'PAT2'

    # static_volume_file = root+'DKI/'+Patient_static+'_FA.nii.gz'
    # moving_volume_file = root+'DKI/'+Patient_moving+'_FA.nii.gz'

    # mapping = get_transform(static_volume_file, moving_volume_file,
    #                        diffeomorph=False, sanity_check=False)

    # apply_transform(moving_volume_file, mapping, static_volume_file,
    #                output_path='C:/Users/nicol/Desktop/PAT2toPAT1_FA.nii.gz')

    # ------------------------

    static_volume_file = 'C:/Users/nicol/Documents/Doctorat/Data/ARC/lesion/10_01_01_E2_MSMT-CSD_WM_ODF.nii.gz'
    moving_volume_file = 'C:/Users/nicol/Documents/Doctorat/Data/ARC/lesion/10_01_01_E0_T1_bet.nii.gz'

    mapping = get_transform(static_volume_file, moving_volume_file,
                            diffeomorph=False, onlyAffine=False, normalize=True)

    lesion_file = 'C:/Users/nicol/Documents/Doctorat/Data/ARC/lesion/YB-04032021-01_2_VOI.nii'

    apply_transform(lesion_file, mapping, static_volume_file,
                    output_path='C:/Users/nicol/Documents/Doctorat/Data/ARC/lesion/lesion_diff_E2.nii.gz',
                    binary=True, binary_thresh=0)

    # Same patient, different time ROIs registration --------------------

    # root='C:/Users/nicol/Documents/Doctorat/Data/Alcool/'
    # Patient_static='PAT3'
    # Patient_moving='PAT1'

    # ROI_folder=root+'fROIs/'

    # static_volume_file=root+'DKI/'+Patient_static+'_FA.nii.gz'
    # moving_volume_file=root+'DKI/'+Patient_moving+'_FA.nii.gz'

    # mapping=get_transform(static_volume_file,moving_volume_file,
    #                       diffeomorph=True,sanity_check=False)

    # apply_transformToAllROIsInFolder(Patient_static,Patient_moving,mapping,
    #                                     ROI_folder,static_volume_file,
    #                                     ['PAT1_PG_Inv.nii.gz','PAT1_PD_Inv.nii.gz',
    #                                      'PAT1_MG_Inv.nii.gz','PAT1_MD_Inv.nii.gz'])

    # Same patient, same time different spaces ---------------------

    # static_volume_file = "C:/Users/nicol/Documents/Doctorat/Data/ARC/10_03_01_E1/dMRI/microstructure/dti/10_03_01_E1_FA.nii.gz"
    # moving_volume_file = "C:/Users/nicol/Documents/Doctorat/Data/ARC/10.03.01_E1_Sag_T1_MPRAGE_0.8_iso_20210325213749.nii.gz"
    # out = "C:/Users/nicol/Documents/Doctorat/Data/ARC/10.03.01_E1_T1_diffusion.nii.gz"

    # mapping = get_transform(static_volume_file, moving_volume_file,
    #                         onlyAffine=True,
    #                         diffeomorph=False, sanity_check=True)

    # apply_transform(moving_volume_file, mapping, static_volume_file,
    #                out,
    #                binary=False)

    # OR

    # root='C:/Users/nicol/Documents/Doctorat/Data/Rescan/'
    # Patient_static='NT1_FA'
    # Patient_moving='NT1_T1'

    # ROI_folder=root+'Raw/'

    # static_volume_file=root+'DKI_Processed/'+Patient_static+'.nii.gz'
    # moving_volume_file=root+'Raw/'+Patient_moving+'.nii.gz'

    # mapping=get_transform(static_volume_file,moving_volume_file,onlyAffine=True,
    #                       diffeomorph=False,sanity_check=True)

    # apply_transform(moving_volume_file,mapping,static_volume_file,
    #                 ROI_folder+Patient_moving+'_diffusion.nii.gz',
    #                 binary=False)

    # -----------------------------------------------------------

    # root = 'C:/Users/nicol/Documents/Doctorat/Data/Alcool/'

    # dti_dir = root+'DKI/'
    # dia_dir = root+'Diamond/'
    # mf_dir = root+'FingerCSD/'

    # saveTTMaps('PAT2', 'PAT3', root+'dMaps/', [dti_dir, dia_dir, mf_dir])

    # Save metric maps to MNI space -----------------------------

    # FA_MNI='C:/Users/nicol/Documents/Doctorat/Data/Atlas_Maps/FSL_HCP1065_FA_1mm.nii.gz'

    # PatientList=['P1B2','P1B3','P2B1','P2B2','P2B3','P2B4','P3B1','P3B2',
    #               'P3B3','P3B4','P1B1','C3B1','C3B2']

    # PatientList=['P2B4','P3B1','P3B2',
    #               'P3B3','P3B4','P1B1','C3B1','C3B2']
    # PatientList=['C3B3','C3B4']

    # root='C:/Users/nicol/Documents/Doctorat/Data/Vox/'
    # dti_folder=root+'DKI/'
    # dia_folder=root+'DIAMOND_SL/'
    # mf_folder=root+'FingerCSD/'

    # MetricList={'_FA':dti_folder,'RD':dti_folder,'AD':dti_folder,'MD':dti_folder,
    #             'wFA':dia_folder,'wRD':dia_folder,'wAD':dia_folder,'wMD':dia_folder,
    #             'fvf_tot':mf_folder}

    # input_folder=root+'DKI/'
    # output_folder='C:/Users/nicol/Desktop/Temp2/'

    # from tqdm import tqdm

    # for Patient in tqdm(PatientList):

    #     static_volume_file=FA_MNI
    #     moving_volume_file=root+'DKI/'+Patient+'_FA.nii.gz'

    #     mapping=get_transform(static_volume_file,moving_volume_file,onlyAffine=False,
    #                           diffeomorph=True,sanity_check=False)

    #     for Metric in MetricList:
    #         apply_transformToAllMapsInFolder(MetricList[Metric],output_folder,mapping,static_volume_file,
    #                                         keywordList=[Patient,Metric],inverse=False)

    import winsound
    winsound.Beep(400, 1500)
