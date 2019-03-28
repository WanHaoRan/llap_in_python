import Tkinter as tk
import tkMessageBox
import Signal_Processing

#there are several UI components, which are 
#"play button": click this button will start playing the CW acoustic signal and recording the reflected signal, and start counter
#"1D distance display": this window display the distance of current object
#and then the mic array can be used, there are four static microphone, whose position could be easily confirmed
#so we can infer the reference position of the object from the static microphone position.

top = tk.Tk()

def playTheSignal():
	tkMessageBox.showinfo("Start!","Start playing audio and recording...")
	#PlayAudio()		#play the CW signal
	#RecordAudio()		#record the CW signal
	
def stopTheSignal():
	tkMessageBox.showinfo("Stop!","Stop playing audio and recording...")
	#StopAudio()		#stop the CW signal
	#StopRecord()		#stop recording
		
B1 = tk.Button(top,text = "PLAY", command = playTheSignal)

B2 = tk.Button(top,text = "STOP", command = stopTheSignal)


B1.pack()
B2.pack()
top.mainloop()
