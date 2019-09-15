import numpy as np
import pygame
import socket
import random

fs = 16000
sampleRate = 48000
new_phase = 0
last_phase = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 1060
s.bind(('',port))

deviceid = 1

is_playing = 0

pygame.mixer.init(frequency=48000,size=-16,channels=1,buffer=4096,devicename='ac101')

s = np.zeros(4096)

for i in range(0,len(s)):
	s = np.sin(2*np.pi*fs*i/sampleRate + phase)

best_phase = []
all_phase = []

sound = pygame.mixer.sound(a)
#sound.play(-1)

#phase shift
def PhaseShift(data, phase):
	new_phase = phase + 30*(random.random()-0.5)*180/np.pi
	for i in range(0,len(data)):
		data[i] = np.sin(2*np.pi*fs*i/sampleRate + new_phase)
	return data, new_phase

def Listen():
	data, address = s.recvfrom(65535)
	return data

def main():
	while True:
		buff = Listen()
		if(buff[0] == 'F'):
			if(buff[1]==deviceid):
				sound.play(-1)
			else:
				sound.stop()
		# last phase change is good
		if(buff[0] == '1'):
			all_phase.append(new_phase)
			best_phase.append(new_phase)
			last_phase = new_phase
			sound.stop()
			s, new_phase = PhaseShift(s, last_phase)
			sound = pygame.mixer.sound(s)
			sound.play(-1)
		# last phase change is bad
		if(buff[0] == '0'):
			all_phase.append(new_phase)
			best_phase.append(last_phase)
			sound.stop()
			s, new_phase = PhaseShift(s, last_phase)
			sound = pygame.mixer.sound(s)
			sound.play(-1)
		# after phase is changed to the best point, receiver do not feedback anything and transmitters
		# keep playing
