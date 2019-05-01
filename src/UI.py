import Tkinter as tk
import time
import threading
import inspect
import ctypes
import recording
import Playsound
import Signal_Processing

import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft

class ui(tk.Frame):
	wait_time=100
	def __init__(self, parent=None, **kw):
		tk.Frame.__init__(self, parent, kw)
		self.time_str=tk.StringVar()
		tk.Label(self, textvariable = self.time_str).pack()
		self.t0 = 0
		self.endflag = 0
		self.thread = []
	
	#kinda useless
	def _update(self):
		t1 = time.time()
		t = t1-self.t0
		#self.time_str.set(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
		self.time_str.set('Has passed: '+str(t)+'s')
		self.timer = self.after(self.wait_time, self._update)
	
	#stop the thread
	def _async_raise(self,tid, exctype):
		"""raises the exception, performs cleanup if needed"""
		tid = ctypes.c_long(tid)
		if not inspect.isclass(exctype):
			exctype = type(exctype)
		res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
		if res == 0:
			raise ValueError("invalid thread id")
		elif res != 1:
			# """if it returns a number greater than one, you're in trouble,
			# and you should call it again with exc=NULL to revert the effect"""
			ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
			raise SystemError("PyThreadState_SetAsyncExc failed")
	
	#when click the play button
	def start(self):
		self.t0 = time.time()
		th1 = threading.Thread(target=self.playCW)
		th2 = threading.Thread(target=self.recordCW)
		self.thread.append(th1)
		self.thread.append(th2)
		for i in self.thread:
			i.setDaemon(True)
			i.start()
			#print i.ident
		#self._update()
		self.pack(side = tk.TOP)
	
	#when click the stop button
	def stop(self):
		#print self.thread[0].ident
		#print self.thread[1].ident
		self._async_raise(self.thread[0].ident, SystemExit)
		#time.sleep(30)
		self._async_raise(self.thread[1].ident, SystemExit)
		self.thread = []
	
	def playCW(self):
		while(1):
			Playsound.playsong()
			print 'one cycle.'
	
	def recordCW(self):
		#i = 0
		#while(1):
		#i = i+1
		#start counter for signal processing
		t1 = time.time()
		t = t1-self.t0
		self.time_str.set('Distance: '+str(t)+'cm')
		#recording tiny slice of CW wave and do signal processing
		a = recording.record() #get the recorded data
		#del a[0:20]
		#d = .GetDistanceChange(a,t)
		path = 'test.txt'
		a = [str(x) for x in a]
		fil = open(path,'w')
		fil.write(a)
		print a
		#x,y = Signal_Processing.GetBaseband(a,t)
		#x,y = Signal_Processing.RemoveDC(x,y)
		#d = Signal_Processing.CalculateDistance(x,y)
		#plt.subplot(211)
		#plt.plot(a)
		#plt.xlabel('I component')
		#plt.ylabel('Q component')
		#plt.subplot(212)
		#x,y = Signal_Processing.RemoveDC(x,y)
		#plt.plot(y[3])
		#plt.xlabel('I component')
		#plt.ylabel('Q component')
		#plt.show()
		#print d
		#signal processing staff
		#and then update the distance display here
		print 'recording ongoing.'
		#if i > 100:
			#break
		
	
	
        
def main():
	root = tk.Tk()
	mw = ui(root)
	mystart = tk.Button(root, text = 'Play', command = mw.start)
	mystop = tk.Button(root,text='Stop', command = mw.stop)
	mystart.pack()
	mystop.pack()
	root.mainloop()
main()
