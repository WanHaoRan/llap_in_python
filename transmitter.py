import numpy as np
import pygame
import socket
import random
import os
#os.putenv('SDL_AUDIODRIVER', '')

fs = 15000.
sampleRate = 48000.
new_phase = 0
last_phase = 0

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
port = 1060
s.bind(('',port))

deviceid = '1'

is_playing = 0

#pygame.mixer.pre_init(48000,-16,2,4096)
pygame.mixer.init(48000,-16,1,4096)

t = np.arange(0,1024)
t = t/sampleRate
seq = 0.5*np.sin(2*np.pi*fs*t)
seq = (seq*32768).astype(np.int16)

best_phase = []
all_phase = []

sound = pygame.sndarray.make_sound(seq)
#sound.play(-1)

#phase shift
def PhaseShift(data, phase):
	new_phase = phase + 30*(random.random()-0.5)*np.pi/180
	data = 0.5*np.sin(2*np.pi*fs*t+new_phase)
	data = (data*32768).astype(np.int16)
	return data, new_phase

def Listen():
	data, address = s.recvfrom(65535)
	return data

def main():
	global sound
	global new_phase
	global last_phase
	global best_phase
	global all_phase
	global seq, deviceid, s
	sound.set_volume(1)
	sound.play(-1)
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
			seq, new_phase = PhaseShift(seq, last_phase)
			sound = pygame.sndarray.make_sound(seq)
			sound.play(-1)
			print('Best phase:',best_phase[-1])
		# last phase change is bad
		if(buff[0] == '0'):
			all_phase.append(new_phase)
			best_phase.append(last_phase)
			sound.stop()
			seq, new_phase = PhaseShift(seq, last_phase)
			sound = pygame.sndarray.make_sound(seq)
			sound.play(-1)
			print('Best phase:',best_phase[-1])
		# after phase is changed to the best point, receiver do not feedback anything and transmitters
		# keep playing

main()
