import Tkinter as tk
import tkMessageBox
import Signal_Processing
import time
import threading

#there are several UI components, which are 
#"play button": click this button will start playing the CW acoustic signal and recording the reflected signal, and start counter
#"1D distance display": this window display the distance of current object
#and then the mic array can be used, there are four static microphone, whose position could be easily confirmed
#so we can infer the reference position of the object from the static microphone position.
counter = 0
top = tk.Tk()

def playTheSignal():
	#tkMessageBox.showinfo("Start!","Start playing audio and recording...")
	#PlayAudio()		#play the CW signal
	#RecordAudio()		#record the CW signal
	t0 = time.time()
	while(1):
		t1 = time.time()
		t = t1-t0
		b = 'Running Time:'+str(t)+'ms'
		text.insert(1.0,b)
	
def stopTheSignal():
	tkMessageBox.showinfo("Stop!","Stop playing audio and recording...")
	#StopAudio()		#stop the CW signal
	#StopRecord()		#stop recording
		
B1 = tk.Button(top,text = "PLAY", command = playTheSignal)

B2 = tk.Button(top,text = "STOP", command = stopTheSignal)

text = tk.Text(top,width = 30,height = 2)
text.pack()
text.insert(1.0,'Distance:  cm')

B1.pack()
B2.pack()

top.mainloop()
