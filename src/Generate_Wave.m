% fs = 48000; %采样率
% T = 1/fs;   %采样点间隔
% time = 5;   %时间
% t = 0:T:time;
% y = sin(2*pi*12000*t)+sin(2*pi*12350*t)+sin(2*pi*12700*t)+sin(2*pi*13050*t)+sin(2*pi*13400*t)+sin(2*pi*13750*t)+sin(2*pi*14100*t)+sin(2*pi*14450*t)+sin(2*pi*14800*t)+sin(2*pi*15150*t)+sin(2*pi*15500*t)+sin(2*pi*15850*t)+sin(2*pi*16200*t)+sin(2*pi*16550*t)+sin(2*pi*16900*t)+sin(2*pi*17250*t);
% x = 0:T:time;
% subplot(2,1,1)
% plot(x,y)
% subplot(2,1,2)
% Y = fft(y);
% x1 = x*fs/5;
% plot(x1,abs(Y))
% %sound(y,fs) %可以播放声音的函数 sound()
% %存储.wav音频文件
% filename = ('test.wav'); %给文件取名
% audiowrite(filename,y,fs) %存储.wav音频文件，在这里文件名为test.wav

Fs = 48000;
t = 0:1/Fs:600-(1/Fs);
y = 1/16*(sin(2*pi*12000*t)+sin(2*pi*12350*t)+sin(2*pi*12700*t)+sin(2*pi*13050*t)+sin(2*pi*13400*t)+sin(2*pi*13750*t)+sin(2*pi*14100*t)+sin(2*pi*14450*t)+sin(2*pi*14800*t)+sin(2*pi*15150*t)+sin(2*pi*15500*t)+sin(2*pi*15850*t)+sin(2*pi*16200*t)+sin(2*pi*16550*t)+sin(2*pi*16900*t)+sin(2*pi*17250*t));
% write the signal x to a .wav file
% subplot(2,1,1)
% plot(y)
% subplot(2,1,2)
% Y = fft(y);
% plot(abs(Y))
wavwrite(y,Fs,16,'test.wav');