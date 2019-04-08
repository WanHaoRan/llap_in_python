import pyaudio


def get_indexs():
	p = pyaudio.PyAudio()
	info = p.get_host_api_info_by_index(0)
	numdevices = info.get('deviceCount')

	for i in range(0,numdevices):
		if(p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')) > 0:
			if p.get_device_info_by_host_api_device_index(0,i).get('name') == 'seeed-8mic-voicecard: - (hw:1,0)':
				#print "Input Device id", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name')
				return i
		
