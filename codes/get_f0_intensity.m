>> % This script returns the f0, RMS intensity and time stamps for the wav file
% Make sure the wav file and the voicebox folder is in your matlab path

% dir = '/Users/zhengwuma/LAMB/lppHK/annotation';

[wav,Fs] = audioread('task-lppHK.wav');

% over 10 ms interval, calculate rms intensity
wavb = buffer(wav,round(0.02*Fs),round(0.01*Fs),'nodelay');
intensity = [0,sqrt(mean(wavb.^2))];

time = 1:0.01:1170.001995 % overall length of the wav file in seconds

% pitchtracking using voicebox function fxrapt, default time frame: 10ms
[f0,tt] = fxrapt(wav,Fs,'u');

% take the middle point in the time frame for the f0 value (5, 15, 25 ms...)
time_f0 = mean(tt(:,1:2),2)/Fs;

% linear interpolate the time points at the 0, 10, 20 ms ...
f0_1 = interp1(time_f0,f0,time,'linear');
f0_1 = f0_1';
% replace nans with 0
f0_1(isnan(f0_1))= 0;
f0 = f0_1';

% save('wav_acoustic.mat','time','f0','f0_1','intensity')
header = {'time', 'f0', 'intensity'};
txt = strjoin(header, ',');
time_intensity = linspace(time(1), time(end), length(intensity));  % Resample time for intensity
intensity_resampled = interp1(time_intensity, intensity, time, 'linear');  % Interpolate intensity to match time
prosody = [time',f0_1,intensity_resampled'];  % Now all arrays have the same number of rows
dlmwrite('wav_acoustic.csv', txt, '');
dlmwrite('wav_acoustic.csv', prosody, '-append', 'delimiter', ',', 'precision', '%.8f');

