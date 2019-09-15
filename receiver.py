#coding:utf-8
import socket
import pyaudio
import wave as we
import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.signal import hilbert, chirp
from scipy import signal
import get_index as gi

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
PORT = 1060
network = '192.168.1.255'
#path = "123.wav"
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
RESPEAKER_INDEX = gi.get_indexs()
RESPEAKER_RATE = 48000

def record(number):
	frames = []
	p = pyaudio.PyAudio()
	stream = p.open(
				rate=RESPEAKER_RATE,
				format=p.get_format_from_width(RESPEAKER_WIDTH),
				channels=RESPEAKER_CHANNELS,
				input=True,
				input_device_index=RESPEAKER_INDEX,)
	print("* recording")
	
	#500 is number of samples extracted, should be manually adjusted in phase beamforming.
	data = stream.read(number)
	# extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
	a = np.fromstring(data,dtype = np.int16)[0::8]
	for i in range(0,number):
		frames.append(a[i])

	print("* done recording")

	stream.stop_stream()
	stream.close()
	p.terminate()
	return  frames
	
	
def CalculateRSS(wavdata):
	return (np.sqrt(sum(wavdata**2)/len(wavdata)))
	
def GetAveAmplitude(wavdata):
	z = hilbert(wavdata)
	inst_amplitude = np.abs(z)
	a = np.mean(inst_amplitude)
	return a
	
def BroadCast(content):
	s.sendto(content.encode('utf-8'),(network, PORT))
	

def main():
	RSS = []
	data = []
	RSS.append(0)
	data.append(0)
	RECORD_SECOND = 0.1

	count = 0

	content = "F1"
	BroadCast(content)
	time.sleep(1)
	a1 = record(1920)

	content = "F2"
	BroadCast(content)
	time.sleep(1)
	a2 = record(1920)

	'''
	#use butterworth filter to focus on the desired frequency band
	f1,f2=signal.butter(5,[0.5,0.99],btype='bandpass',analog=False,output='ba')
	m1 = a1[1]
	m2 = a2[1]
	m1 = signal.filtfilt(f1,f2,m1)
	m2 = signal.filtfilt(f1,f2,m2)
	'''
	z1 = GetAveAmplitude(a1)
	z2 = GetAveAmplitude(a2)
	suma = z1+z2
	print z1
	print z2
	print suma
	sb = input("press enter to continue")
	while True:
		wavdata = record(1920)
		'''
		#use filter to focus on the desired frequency band
		f1,f2=signal.butter(5,[0.5,0.99],btype='bandpass',analog=False,output='ba')
		d = signal.filtfilt(f1,f2,wavdata[1])
		'''
		a = GetAveAmplitude(wavdata)
		if (a > RSS[-1]):
			RSS.append(a)
			print("The best amplitude till now is %d" % (RSS[-1]))
			content = "1"#+str(time.time()+1)
			BroadCast(content)
			data.append(a)
		elif(a < RSS[-1]):
			RSS.append(RSS[-1])
			print("The best amplitude till now is %d" % (RSS[-1]))
			content = "0"
			BroadCast(content)
			data.append(a)
			
		if (a >=0.9*(suma-14)):
			print("The final amplitude is %d" % (RSS[-1]))
			break;
	plt.subplot(211)
	plt.title("every phase change caused")
	plt.plot(data)
	plt.subplot(212)
	plt.title("best till now")
	plt.plot(RSS)
	plt.show()


	
main()
