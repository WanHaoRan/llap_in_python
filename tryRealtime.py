import Tkinter as tk
import time


class clock(tk.Frame):
	wait_time=100
	def __init__(self, parent=None, **kw):
		tk.Frame.__init__(self, parent, kw)
		self.time_str=tk.StringVar()
		tk.Label(self, textvariable = self.time_str).pack()
		self.t0 = 0
	def _update(self):
		t1 = time.time()
		t = t1-self.t0
		#self.time_str.set(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
		self.time_str.set('Has passed: '+str(t)+'s')
		self.timer = self.after(self.wait_time, self._update)
	def start(self):
		self.t0 = time.time()
		self._update()
		self.pack(side = tk.TOP)
        
def main():
	root = tk.Tk()
	mw = clock(root)
	mywatch = tk.Button(root, text = 'watch', command = mw.start)
	mywatch.pack(side = tk.LEFT)
	root.mainloop()
main()
