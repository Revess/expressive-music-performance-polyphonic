import pysynth as ps
import csv
import wave 
import pyaudio
import math


with open("result_segment.csv","r",encoding="UTF-8") as f:
    data = [r for r in csv.reader(f)]

cut = [[d[0],round(float(d[1]),1)] for d in data[125:]]                     #cut "first 0" section
time = float(data[1][0])                                                    #sampling time

note = [round(69.0 + 12.0 * math.log2(float(c[1]) / 440.0)) for c in cut]   #translate frequancy to MIDI note


test = (('g1', 8), ('d2', 8), ('e2', 8), ('d2', 8), ('e2', 8), ('d2', 8), ('e2', 8), ('d2', 8))
ps.make_wav(test, fn = "test.wav")



try:
    wf = wave.open("test.wav", "r")
except FileNotFoundError: #ファイルが存在しなかった場合
    print("[Error 404] No such file or directory: " + "test.wav")
  
# ストリームを開く
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

# 音声を再生
chunk = 1024
data = wf.readframes(chunk)
while data != '':
    stream.write(data)
    data = wf.readframes(chunk)
stream.close()
p.close()
