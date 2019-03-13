import numpy as np
import audiolazy as al
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
from scipy.signal import hilbert,chirp
from scipy import signal

#17~23Khz, and 16 subfrequencies which is 17, 17.400, 17.800, 18.200, 18.600, 19.000, 19.400, 19.800, 20.200, 20.600, 21.000, 21.400, 21.800, 22.200, 22.600, 23.000

AUDIO_SAMPLE_RATE = 48000	#sampling rate of microphone
SPEED = 331.6 + 0.606*20	#sound speed
NumFreq = 16	#number of frequencies
RecordSecond = 0.1
Freqs = np.zeros(NumFreq,dtype=float)
FreqPower = np.zeros(NumFreq,dtype=float)
POWER_THR = 15000	#a empirical threshold of DC power estimation, needs calibrate when deployed in different platform
PEAK_THR = 220		#empirical and needs calibrating.
DC_TREND = 0.25		#DC_TREND threshold, may need calibrating
MaxValue = np.zeros([2,NumFreq],dtype = float)
MinValue = np.zeros([2,NumFreq],dtype = float)		#this two arrays store the max and min value of real and image baseband signal
DCValue = np.zeros([2,NumFreq],dtype = float)		#store the DC value estimation result
for i in range(0,NumFreq):
	Freqs[i] = 17000+i*400


def GetBaseband(databuffer):	#databuffer is a 16*n array, where n is the number of sampling point in each frequencies.
	(row,column) = databuffer.shape
	#the sin and cos buffer afterward will be predifined to achieve faster running time
	sinbuffer = np.zeros([NumFreq,column],dtype = float)
	cosbuffer = np.zeros([NumFreq,column],dtype = float)
	for i in range(0,NumFreq):
		for j in range(0,column):
			sinbuffer[i][j] = np.sin(2*np.pi*j/AUDIO_SAMPLE_RATE*Freqs[i])
			cosbuffer[i][j] = np.cos(2*np.pi*j/AUDIO_SAMPLE_RATE*Freqs[i])
	#CIC filter also needs initializing
	
	
	
	
	#turn the databuffer from int to float
	databuffer = databuffer.astype(np.float)
	#get I and Q from databuffer
	Ibuffer = databuffer * cosbuffer
	Qbuffer = -1 * databuffer * cosbuffer
	
	#applying CIC filter to I/Q buffer and get the baseband signal
	#and return the real part(I) and image part(Q) of baseband signal
	
	
	#input should be the format of NumFreq*n array
def RemoveDC(BaseBandReal,BaseBandImage):		#use LEVD algorithm to calculate the DC value
	tempdata = np.zeros(4096,dtype = float)
	tempdata2 = np.zeros(4096,dtype = float)
	temp_val = 0
	row1,column1 = BaseBandReal.shape
	row2,column2 = BaseBandImage.shape
	if column1 > 4096 or row1 != row2 or column1 != column2:
		return
	
	for f in range(0,NumFreq):
		vsum = 0
		dsum = 0
		#real part
		max_valr = max(BaseBandReal[f])
		min_valr = min(BaseBandReal[f])
		#get variance, first remove the first value
		temp_val = -BaseBandReal[f][0]
		tempdata = BaseBandReal[f] + temp_val
		temp_val = sum(tempdata)
		dsum = dsum+abs(temp_val)/column1
		tempdata2 = tempdata * tempdata
		temp_val = sum(tempdata2)
		vsum = vsum+abs(temp_val)/column1
		
		#image part
		max_vali = max(BaseBandImage[f])
		min_vali = min(BaseBandImage[f])
		#get variance, first remove the first value
		temp_val = -BaseBandImage[f][0]
		tempdata = BaseBandImage[f] + temp_val
		temp_val = sum(tempdata)
		dsum = dsum+abs(temp_val)/column2
		tempdata2 = tempdata * tempdata
		temp_val = sum(tempdata2)
		vsum = vsum+abs(temp_val)/column2
		
		FreqPower[f] = vsum+dsum*dsum
		
		#get DC estimation
		if FreqPower[f] > POWER_THR:
			if max_valr > MaxValue[0][f] or (max_valr > MinValue[0][f] + PEAK_THR and (MaxValue[0][f]-MinValue[0][f]) > PEAK_THR*4):
				MaxValue[0][f] = max_valr
			if min_valr < Minvalue[0][f] or (min_valr < MaxValue[0][f] - PEAK_THR and (MaxValue[0][f]-MinValue[0][f]) > PEAK_THR*4):
				MinValue[0][f] = min_valr
			if max_vali > MaxValue[1][f] or (max_vali > MinValue[1][f] + PEAK_THR and (MaxValue[1][f]-MinValue[1][f]) > PEAK_THR*4):
				MaxValue[1][f] = max_vali
			if min_vali < Minvalue[1][f] or (min_vali < MaxValue[1][f] - PEAK_THR and (MaxValue[1][f]-MinValue[1][f]) > PEAK_THR*4):
				MinValue[1][f] = min_vali
			
			if (MaxValue[0][f]-MinValue[0][f]) > PEAK_THR and (MaxValue[1][f]-MinValue[1][f]) > PEAK_THR:
				for i in range(0,2):
					DCValue[i][f] = (1-DC_TREND)*DCValue[i][f]+(MinValue[i][f]+MaxValue[i][f])/2*DC_TREND
		
		#remove DC
		BaseBandReal[f] = BaseBandReal[f] - DCValue[0][f]
		BaseBandImage[f] = BaseBandImage[f] - DCValue[1][f]
		
		return BaseBandReal,BaseBandImage
		
def CalculateDistance(BaseBandReal,BaseBandImage):
	distance = 0
	tempcomplex = 0+0j
	tempdata = np.zeros(4096,dtype = float)
	tempdata2 = np.zeros(4096,dtype = float)
	tempdata3 = np.zeros(4096,dtype = float)
	temp_val = 0
	phasedata = np.zeros([NumFreq,4096],dtype = float)
	ignorefreq = np.zeros(NumFreq,dtype = int)
	
	row1,column1 = BaseBandReal.shape
	row2,column2 = BaseBandImage.shape
	if column1 > 4096 or row1 != row2 or column1 != column2:
		return
	
	for f in range(0,NumFreq):
		ignorefreq[f] = 0
		#get complex number
		tempcomplex.real = 
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
