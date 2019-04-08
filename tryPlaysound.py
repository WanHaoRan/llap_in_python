from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_wav("RedHighHeels.wav")
play(song)
print 'finished...'
