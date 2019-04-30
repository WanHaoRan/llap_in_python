from pydub import AudioSegment
from pydub.playback import play

def playsong():
	song = AudioSegment.from_wav("test.wav")
	play(song)
	print 'finished...'
