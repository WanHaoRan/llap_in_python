import pyaudio
import wave
import numpy as np
import get_audio_index as gi

RESPEAKER_RATE = 48000
RESPEAKER_CHANNELS = 8
RESPEAKER_WIDTH = 2
# run get_indexs to get index
RESPEAKER_INDEX = gi.get_indexs()  # get input device id
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            input_device_index=RESPEAKER_INDEX,)

print("* recording")

frames = [] 

#for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
data = stream.read(100)
# extract channel 0 data from 8 channels, if you want to extract channel 1, please change to [1::8]
a = np.fromstring(data,dtype=np.int16)[0::8]
frames.append(a.tostring())

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()


print frames

'''
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(p.get_format_from_width(RESPEAKER_WIDTH)))
wf.setframerate(RESPEAKER_RATE)
wf.writeframes(b''.join(frames))
wf.close()
'''
