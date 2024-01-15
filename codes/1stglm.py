import os
import sys
import nibabel as nib
import numpy as np
import pandas as pd
import nilearn
import matplotlib.pyplot as plt
from nilearn.glm.first_level import FirstLevelModel,make_first_level_design_matrix
from nilearn.image import concat_imgs, resample_to_img
from nilearn.plotting import plot_stat_map
from nilearn.datasets import load_mni152_gm_mask
from nilearn.glm import threshold_stats_img
from nilearn.glm.contrasts import compute_contrast

DIR = '/scratch/ResearchGroups/lt_jixingli/lppHK'
os.chdir(DIR)

subj_id = int(sys.argv[1])
subj = subj_id - 1

img1 = nib.load('Data/derivatives/%s/func/%s_task-lppHK_run-1_bold.nii.gz' %(subj,subj))
img2 = nib.load('Data/derivatives/%s/func/%s_task-lppHK_run-2_bold.nii.gz' %(subj,subj))
img3 = nib.load('Data/derivatives/%s/func/%s_task-lppHK_run-3_bold.nii.gz' %(subj,subj))
img4 = nib.load('Data/derivatives/%s/func/%s_task-lppHK_run-4_bold.nii.gz' %(subj,subj))
fmri_img = nib.concat_images([img1,img2,img3,img4],axis=3)

gray_matter_mask = load_mni152_gm_mask()
resampled_mask = resample_to_img(gray_matter_mask, fmri_img)

# Define event-related regressors
f0 = pd.read_csv('GLM/wav_acoustic.csv')
f0.rename(columns={'f0':'onset'},inplace=True)
f0.insert(1,'duration',0)
f0.insert(2,'trial_type',1)
f0_events = f0[['onset','duration','trial_type']]

intensity = pd.read_csv('GLM/wav_acoustic.csv')
intensity.rename(columns={'intensity':'onset'},inplace=True)
intensity.insert(1,'duration',0)
intensity.insert(2,'trial_type',1)
int_events = intensity[['onset','duration','trial_type']]

word_rate_events = pd.read_csv(f'GLM/word_rate/%s.csv' %subj, names=['onset','trial_type'])
word_rate_events.insert(1,'duration',0)

regs = ['f0','int','word_rate']
event_dict = {'f0':f0_events,'int':int_events,'word_rate':word_rate_events}

for reg in regs:
    events = event_dict[reg]
    first_level_model = FirstLevelModel(t_r=2,hrf_model='spm',mask_img=resampled_mask).fit(fmri_img, events)
    design_matrix = first_level_model.design_matrices_[0]
    contrast = np.zeros(design_matrix.shape[1])
    contrast[0] = 1
    z_map1 = first_level_model.compute_contrast(contrast, output_type='z_score')
    nib.save(z_map1,'/scratch/zhengwuma2/lpphk/glm/zmap1_%s_%s.nii' %(subj,reg))
    display_reg1 = plot_stat_map(z_map1, display_mode='z', threshold=3.0, colorbar=True)
    display_reg1.savefig('/scratch/zhengwuma2/lpphk/glm/plot_%s_%s.png'%(subj,reg))
