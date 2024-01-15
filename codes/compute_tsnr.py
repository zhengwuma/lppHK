import sys
import os
from nipype.algorithms.confounds import TSNR

subj_id = int(sys.argv[1])
subj = subj_id - 1

tsnr = TSNR()

os.chdir('/scratch/ResearchGroups/lt_jixingli/lppHK/Data/derivatives/%s/func/' %subj)
output =('/scratch/ResearchGroups/lt_jixingli/lppHK/Results/%s/func/tsnr' %subj)
if not os.path.exists(output):
	os.makedirs(output)
	
for i in range(1,5):
	print('Processing preprocessed %s, run_%d' %(subj,i))
	f = '%s_task-lppHK_run-%d_bold.nii.gz' %(subj,i)
	tsnr.inputs.in_file = f
	tsnr.inputs.tsnr_file = os.path.join(output,'%s_task-lppHK_run-%d_tsnr.nii.gz' %(subj,i))
	tsnr.inputs.mean_file = os.path.join(output,'%s_task-lppHK_run-%d_mean.nii.gz' %(subj,i))
	tsnr.inputs.stddev_file = os.path.join(output,'%s_task-lppHK_run-%d_stddev.nii.gz' %(subj,i))
	tsnr.inputs.detrended_file = os.path.join(output,'%s_task-lppHK_run-%d_detrended.nii.gz' %(subj,i))
	tsnr.inputs.regress_poly = 4
	tsnr.run()

os.chdir('/scratch/ResearchGroups/lt_jixingli/lppHK/Data/%s/func/' %(lang,subj))
for i in range(1,5):
	print('Processing raw %s, run_%d' %(subj,i))
	f = '%s_task-lppHK_run-%d_bold.nii.gz' %(subj,i)
	tsnr.inputs.in_file = f
	tsnr.inputs.tsnr_file = os.path.join(output,'%s_raw_task-lppHK_run-%d_tsnr.nii.gz' %(subj,i))
	tsnr.inputs.mean_file = os.path.join(output,'%s_raw_task-lppHK_run-%d_mean.nii.gz' %(subj,i))
	tsnr.inputs.stddev_file = os.path.join(output,'%s_raw_task-lppHK_run-%d_stddev.nii.gz' %(subj,i))
	tsnr.inputs.detrended_file = os.path.join(output,'%s_raw_task-lppHK_run-%d_detrended.nii.gz' %(subj,i))
	tsnr.inputs.regress_poly = 4
	tsnr.run()
