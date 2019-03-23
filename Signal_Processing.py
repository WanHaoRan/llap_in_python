import numpy as np
import audiolazy as al
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
from scipy.signal import hilbert,chirp
from scipy import signal
import math as ma

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
WaveLength = np.zeros(NumFreq,dtype = float)

for i in range(0,NumFreq):
	Freqs[i] = 17000+i*400
	WaveLength[i] = SPEED/Freqs[i]



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
	#get I and Q from databuffer, and this step should be redesigned for the time shift.
	Ibuffer = databuffer * cosbuffer
	Qbuffer = -1 * databuffer * cosbuffer
	
	#applying CIC filter to I/Q buffer and get the baseband signal
	#and return the real part(I) and image part(Q) of baseband signal
	#use the sine and cosine to multiply the recorded signal(16 different frequencies component) and use the same CIC filter to cut the useful part 
	#since the same frequency multiplication get the phase information (less than 100Hz), other frequency will make the multiplication result higher,
	#which is higher than 400Hz(the frequency interval is 400Hz). So the same low pass CIC filter will get each frequency part's phase information and 
	#split the signal into 16x2 parts(I/Q and 16frequencies component). Then, we remove the DC component and use linear regression to get the distance change.
	#So the return value of this function is the two NumFreq x n array, which are the BaseBandReal and BaseBandImage.
	
	
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
	tempcomplexr = np.zeros(4096,dtype=float)
	tempcomplexi = np.zeros(4096,dtype=float)	#this two arrays represent the real and image part of the baseband signal
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
	
	#process in every frequency component
	for f in range(0,NumFreq):
		ignorefreq[f] = 0
		#get complex number
		tempcomplexr = BaseBandReal[f]
		tempcomplexi = BaseBandImage[f]
		
		#get magnitude
		tempdata = BaseBandReal[f] * BaseBandReal[f] + BaseBandImage[f] * BaseBandImage[f]
		temp_val = sum(tempdata)
		
		if temp_val/column1>POWER_THR:
			for n in range(0,column1):
				phasedata[f][n] = ma.atan2(tempcomplexi[n],tempcomplexr[n])
			#phase unwarp
			for i in range(1,column1):
				while phasedata[f][i]-phasedata[f][i-1]>np.pi:
					phasedata[f][i]=phasedata[f][i]-2*np.pi
				while phasedata[f][i]-phasedata[f][i-1]<-np.pi:
					phasedata[f][i]=phasedata[f][i]+2*np.pi
			
			if abs(phasedata[f][column1-1]-phasedata[f][0]>np.pi/4):
				for i in range(0,2):
					DCValue[i][f]=(1-DC_TREND*2)*DCValue[i][f]+(MinValue[i][f]+MaxValue[i][f])/2*DC_TREND*2
			
			#prepare linear regression
			#remove start phase
			temp_val=-phasedata[f][0]
			tempdata = phasedata[f]+temp_val
			#divide the constants
			temp_val=2*np.pi/WaveLength[f]
			phasedata[f]=tempdata/temp_val
		else:	#ignore the low power vector
			ignorefreq[f]=1
		
	#linear regression
	for i in range(0,column1):
		tempdata2[i] = i
	sumxy=0
	sumy=0
	numfreqused=0
	for f in range(0,NumFreq):
		if ignorefreq[f]==1:
			continue
		
		numfreqused = numfreqused+1
		
		tempdata = phasedata[f]*tempdata2
		temp_val = sum(tempdata)
		sumxy = temp_val+sumxy
		temp_val = sum(phasedata[f])
		sumy = sumy+temp_val
		
	if numfreqused==0:
		distance = 0
		return distance
	
	deltax=NumFreq*((column1-1)*column1*(2*column-1)/6-(column1-1)*column1*(column1-1)/4)
	delta=(sumxy-sumy*(column1-1)/2.0)/deltax*NumFreq/numfreqused
	
	varsum=0
	var_val = np.zeros(NumFreq,dtype=float)
	for i in range(0,column1):
		tempdata2[i]=i*delta
	
	#get variance of each freq
	for f in range(0,NumFreq):
		var_val[f]=0
		if(ignorefreq[f]==1):
			continue
		tempdata = phasedata[f]-tempdata2
		tempdata3 = tempdata*tempdata
		var_val[f] = sum(tempdata3)
	varsum=varsum/numfreqused
	for f in range(0,NumFreq):
		if ignorefreq[f]==1:
			continue
		if var_val[f]>varsum:
			ignorefreq[f]=1
	
	for i in range(0,column1):
		tempdata2[i] = i
	
	#linear regression
	sumxy=0
	sumy=0
	numfreqused=0
	for f in range(0,NumFreq):
		if ignorefreq[f]==1:
			continue
		numfreqused=numfreqused+1
		
		tempdata = tempdata2*phasedata[f]
		temp_val = sum(tempdata)
		sumxy = sumxy+temp_val
		temp_val = sum(phasedata[f])
		sumy = sumy+temp_val
		
	if numfreqused == 0:
		distance = 0
		return distance
	
	delta=(sumxy-sumy*(column1-1)/2.0)/deltax*NumFreq/numfreqused
	
	distance = -delta*column1/2
	return distance
	
def GetDistanceChange(databuffer):		#feed the recorded data into our signal processing function
	distancechange = 0
	BaseBandReal,BaseBandImage = GetBaseband(databuffer)
	BaseBandReal,BaseBandImage = RemoveDC(BaseBandReal,BaseBandImage)
	distancechange = CalculateDistance(BaseBandReal,BaseBandImage)
	return 	distancechange
			



		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
