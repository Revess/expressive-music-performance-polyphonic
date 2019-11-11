import numpy as np
import librosa
import scipy.io.wavfile
import csv

#音声ファイル読み込み
wav_filename = "audio/Cello_Suite_1007_mono.wav"
rate, data = scipy.io.wavfile.read(wav_filename)

data = data / 32768
fft_size = 512                
hop_length = int(256 / 4)  

# 短時間フーリエ変換実行
amplitude = np.abs(librosa.core.stft(data, n_fft=fft_size, hop_length=hop_length))
print(len(amplitude[0]))
print(len(amplitude))
with open("doc/spec_3.csv","w") as f:
    writer = csv.writer(f,lineterminator="\n")
    for fft in amplitude:
        writer.writerow(fft)