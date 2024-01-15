%of the electrodes based on EGI cap
EEG = pop_chanedit(EEG, 'lookup','/Users/best/Documents/EEG_lpp/scripts/channel_loc_ns.ced');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_chaninfo'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_chaninfo.set'], 'gui', 'off');


% remove noisy channels
EEG = pop_select(EEG, 'rmchannel',{'HEO','VEO','TRIGGER','EKG', 'EMG'});
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'savenew',['sub-' SUB{i} '_task-lppHK_eeg_rmchans'],'gui','off']); 


%Apply Parks-McClellan notch filter at 50 Hz to reduce power line noise
EEG  = pop_basicfilter( EEG,  1:64 , 'Boundary', 'boundary', 'Cutoff',  50, 'Design', 'notch', 'Filter', 'PMnotch', 'Order',  180 );
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 3, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt.set'], 'gui', 'off');
    

%Remove DC offsets and apply a band-pass filter (non-causal Butterworth impulse response function, 0.1 Hz high pass and 40.0 low pass half-amplitude cut-off, 12 dB/oct roll-off)
EEG  = pop_basicfilter( EEG,  1:64 , 'Boundary', 'boundary', 'Cutoff',  [0.1 40], 'Design', 'butter', 'Filter', 'bandpass', 'Order',  2, 'RemoveDC', 'on' );
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 4, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt.set'], 'gui', 'off');       


%Apply automatic bad channel rejection Pre-ICA using kurtosis measure
[EEG, V_Channels_Excluded] = pop_rejchan(EEG, 'elec', 1:64,'threshold',5,'norm','on','measure','kurt'); % pop_rejchan(EEG,'threshold',5,'norm','on','measure','kurt');
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 5, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem.set'], 'gui', 'off');


%Save information about Bad Channels excluded Pre-ICA
V_BadChannelsFile = fullfile(['sub-' SUB{i} '_task-lppHK_eeg_Bad_Channel_Indices.txt']);
dlmwrite(V_BadChannelsFile, V_Channels_Excluded, 'delimiter', ',');


% saved the bad channels information from last step
% Interpolate channel(s) specified in Excel file Interpolate_Channels.xls; any channel without channel locations (e.g., EOGS) should not be included in the interpolation process and are listed in ignored channels      
DimensionsOfFile1 = size(alldata1);
for j = 1:DimensionsOfFile1(1);
    if isequal([SUB{i}],num2str(alldata1{j,1}));
        badchans = (alldata1{j,2});
        if ~isequal(badchans,'none') | ~isempty(badchans)
           	if ~isnumeric(badchans)
              badchans = str2num(badchans);
          end      

          EEG  = pop_erplabInterpolateElectrodes( EEG, 'displayEEG',  0, 'ignoreChannels',  ignored_channels, 'interpolationMethod',  'spherical', 'replaceChannels', badchans);
           
        end
        [ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 6, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp.set'], 'gui', 'off'); 
    end
end


%Compute ICA weights with runICA 
EEG = pop_runica(EEG,'extended',1,'icatype', ['runica']); 
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 7, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted'], 'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted.set'], 'gui', 'off');


%Load the EEG data file with ICA weights outputted
EEG = pop_loadset( 'filename', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted.set'], 'filepath', Subject_Path);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 8, 'setname', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted'], 'gui', 'off'); 
         

%Automatic IC weight rejection using ADJUST
EEG = interface_ADJ (EEG,['sub-' SUB{i} 'report.txt']);


%Load list of ICA component(s) corresponding to ocular and muscle artifacts from Excel file ICA_Components.xlsx
[ndata, text, alldata] = xlsread([{your folder path to the file} '/ICA_Components_lppHK.xlsx']); 
MaxNumComponents = size(alldata, 2);
    
    for j = 2:length(alldata(:,1))
        if isequal([SUB{i}], num2str(alldata{j,1}))
            NumComponents = 0;
            for k = 1:MaxNumComponents
                if ~isnan(alldata{j,k})
                    NumComponents = NumComponents+1;
                end
                Components = [alldata{j,(2:(NumComponents+1))}];
            end
        end
    end

%removing the ICA component(s)
EEG = pop_subcomp( EEG, [Components], 0);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 9,'setname',['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted_ica_corr'],'savenew', ['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_interp_ica_weighted_ica_corr.set'],'gui','off'); 


% re-referencing 
EEG = pop_loadset('filename',['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_ica_weighted_ica_corr_interp.set'],'filepath','/Users/best/Documents/EEG_lpp/data_epoch_new/');
[ALLEEG, EEG, CURRENTSET] = eeg_store( ALLEEG, EEG, 0 );
EEG = pop_reref( EEG, [44 45]);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 1,'savenew',['sub-' SUB{i} '_task-lppHK_eeg_rmchans_nhfilt_bpfilt_badchanrem_ica_weighted_ica_corr_interp_ref'],'gui','off'); 


% down-sampling
EEG = pop_resample( EEG, 250);
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'savenew',['sub-' SUB{i} '_task-lppHK_eeg_preprocessed'],'gui','off'); 
eeglab redraw;


