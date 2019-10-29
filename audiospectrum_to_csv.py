#Python module that generates a csv file with the frequency response of an audio file.
import numpy as np
import pandas as pd
import os
import csv
import math
from scipy import signal
# import soundfile as sf
import librosa as lb
import librosa.display
import matplotlib.pyplot as plt
import time

start = 0
end = 0
elapsed = 0

#Find timestamps of the spectral data and calulate them
def frame_timer(num_samps,spectrum_width,sr=22050):
    print("Finding timestamps...", end="")
    s = time.time()
    times = np.array(0)
    sound_length = (1/sr)*num_samps
    offset = sound_length / spectrum_width
    times = [0]
    for i in range(spectrum_width):
        times.append(times[i] + offset)
    times = np.array(times)
    e = time.time()
    elapsed = e-s
    print("Done in: " + "{0:.4f}".format(elapsed) + "s")
    return times

def audio_to_spectroCSV(audio_path,csv_path,nfft,overlap,remove_silence,Show_Graph,Write_File):
    data, sr = lb.core.load(audio_path) #Read audio file, works with any bitdepth
    if(remove_silence):
        print("Starting to remove start silence")
        i = 0
        for sample in data:
            if(sample < 0.005):
                i+=1
            elif(sample > 0.005):
                data = data[i:]
                break
        print("Finished removing silence, start time trimmed:" + str(i/sr))
    
    print("Start calulating Spectrum")
    start = time.time()
    overlap = int(nfft*overlap)
    Spectrum = lb.core.stft(data,n_fft=nfft,hop_length=overlap)
    Spectrum=np.abs(Spectrum)
    frequency = lb.core.fft_frequencies(sr=sr, n_fft=nfft)
    times = frame_timer(int(data.shape[0]),int(Spectrum.shape[1]),sr)
    end = time.time()
    elapsed = end-start
    print("Done Calculating Spectrum in: " + "{0:.4f}".format(elapsed) + "s")

    if(Show_Graph):
        #Plot test
        librosa.display.specshow(librosa.amplitude_to_db(Spectrum,ref=np.max),y_axis='log', x_axis='time')
        plt.title('Power spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()

    if(Write_File):
        #Write to csv file
        print("Started writing csv file")
        start = time.time()
        header = "time in samples"
        for data in frequency:
            header += "," + str(data)
        header += "\n"
        Spectrum = np.rot90(Spectrum)
        Spectrum = np.insert(Spectrum,0,times,1)

        with open(csv_path, "w", newline='') as spectrum_csv:
            #spectrum_csv.write(header)
            wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(Spectrum)
            spectrum_csv.close()
        end = time.time()
        elapsed = end - start
        print("Finished writing spectral csv file in: " + "{0:.4f}".format(elapsed) + "s")