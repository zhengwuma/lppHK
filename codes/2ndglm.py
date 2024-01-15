import os
import sys
import pandas as pd
import nibabel as nib
import numpy as np
import nilearn
import matplotlib.pyplot as plt
from nilearn import plotting
from nilearn.glm.second_level import SecondLevelModel
from nilearn.plotting import plot_design_matrix,plot_stat_map,plot_contrast_matrix,plot_glass_brain
from nilearn.glm import threshold_stats_img,cluster_level_inference

n_hk = 46
DIR = '/Users/zhengwuma/LAMB/lppHK/quality/glm'
os.chdir(DIR)

# perform word_rate
zmap2_wr=[]
for i in range(n_hk):
  subj = subjects_hk[i]
  zmap = nib.load(f'zmap1_%s_word_rate.nii' %subj)
  zmap2_wr.append(zmap)
design_matrix = pd.DataFrame([1]*len(zmap2_wr),columns=['intercept'])
second_level_model = SecondLevelModel()
second_level_model = second_level_model.fit(zmap2_wr,design_matrix=design_matrix)
z_map2 = second_level_model.compute_contrast(output_type='z_score')
stat_word = cluster_level_inference(z_map2,threshold=3,alpha=0.05)
nib.save(stat_word,'2nd_stat_word.nii')

display1 = plotting.plot_glass_brain(stat_word,colorbar=True,display_mode='lzry')
display1.savefig('2nd_wordrate_glass.png')
display2 = plotting.plot_stat_map(stat_word,display_mode='z',colorbar=True,vmax=0.03)
display2.savefig('2nd_wordrate_stat.png')

# perform f0
zmap2_f0=[]
for i in range(n_hk):
  subj = subjects_hk[i]
  zmap = nib.load(f'zmap1_%s_f0.nii' %subj)
  zmap2_f0.append(zmap)
design_matrix = pd.DataFrame([1]*len(zmap2_f0),columns=['intercept'])
second_level_model = SecondLevelModel()
second_level_model = second_level_model.fit(zmap2_f0,design_matrix=design_matrix)
z_map2f0 = second_level_model.compute_contrast(output_type='z_score')
stat_f0 = cluster_level_inference(z_map2f0,threshold=3,alpha=0.05)
nib.save(stat_f0,'2nd_stat_f0.nii')

display1 = plotting.plot_glass_brain(stat_f0,colorbar=True,display_mode='lzry')
display1.savefig('2nd_f01_glass.png')
display2 = plotting.plot_stat_map(stat_f0,display_mode='z',colorbar=True,vmax=0.03)
display2.savefig('2nd_f01_stat.png')

# perform int
zmap2_int=[]
for i in range(n_hk):
  subj = subjects_hk[i]
  zmap = nib.load(f'zmap1_%s_int.nii' %subj)
  zmap2_int.append(zmap)
design_matrix = pd.DataFrame([1]*len(zmap2_int),columns=['intercept'])
second_level_model = SecondLevelModel()
second_level_model = second_level_model.fit(zmap2_int,design_matrix=design_matrix)
z_map2int = second_level_model.compute_contrast(output_type='z_score')
stat_int = cluster_level_inference(z_map2int,threshold=3,alpha=0.05)
nib.save(stat_int,'2nd_stat_int.nii')

display1 = plotting.plot_glass_brain(stat_int,colorbar=True,plot_abs=False,display_mode='lzry')
display1.savefig('2nd_int_glass.png')
display2 = plotting.plot_stat_map(stat_int,display_mode='z',colorbar=True,vmax=0.03)
display2.savefig('2nd_int_stat.png')
