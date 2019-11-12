#Python module that generates a csv file with the frequency response of an audio file.
#Using the Librosa sound manipulation library
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
import time as t
import frame_timer as ft

start = 0
elapsed = 0

def audio_to_spectroCSV(audio_path,csv_path,nfft,overlap,remove_silence,Show_Graph,Write_File):
    data, sr = lb.core.load(audio_path)
    #If needed you can remove the starting silence of the audio file
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
    
    #Place where the spectral data gets calculated
    print("Start calulating spectrum")
    start = t.time()
    overlap = int(nfft*(((sr/1000)*overlap)/sr))
    spectrum = lb.core.stft(data,n_fft=nfft,hop_length=overlap)
    spectrum = np.abs(spectrum)
    frequency = lb.core.fft_frequencies(sr=sr, n_fft=nfft)
    times = ft.frame_timer(int(data.shape[0]),int(spectrum.shape[1]),sr)
    elapsed = t.time() - start
    print("Done calculating spectrum in: " + "{0:.2f}".format(elapsed) + "s")
    print("The spectrum is a matrix with: " + str(int(spectrum.shape[0])) + " frequency bins & " + str(int(spectrum.shape[1])) + " time slices")
    print("Each time frame is: ~" + "{0:.2f}".format((times[2]-times[1])*1000) + "ms")
    print("The frequency interval is: ~" + "{0:.2f}".format(frequency[2] - frequency[1]) + "Hz")

    #If desired a mathplot can be created if Show_Graph=True
    if(Show_Graph):
        #Plot test
        librosa.display.specshow(librosa.amplitude_to_db(spectrum,ref=np.max),y_axis='log', x_axis='time')
        plt.title('Power spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()

    #If Write_File=True, the Spectral data gets written to csv file
    if(Write_File):
        #Write to csv file
        print("Start writing csv file")
        start = t.time()
        header = "time in seconds"
        for data in frequency:
            header += "," + str(data)
        header += "\n"
        spectrum = np.rot90(spectrum)
        spectrum = np.flip(spectrum,0)
        tempspec = np.zeros((spectrum.shape[0],spectrum.shape[1]+1,3),dtype=object)
        for i in range(int(tempspec.shape[0])):
            for j in range(int(tempspec.shape[1])):
                if(j == 0):
                    tempspec[i,j] = [times[i],0,0]
                else:
                    for k in range(int(tempspec.shape[2])):
                        if(i == 1 and k == 0):
                            tempspec[i,j,k] = 0
                        elif(i >= int(tempspec.shape[0])-2 and k == 2):
                            tempspec[i,j,k] = 0
                        elif(k == 0):
                            tempspec[i,j,k] = spectrum[i-1,j-1]
                        elif(k == 1):
                            tempspec[i,j,k] = spectrum[i,j-1]
                        elif(k == 2):
                            tempspec[i,j,k] = spectrum[i+1,j-1]
        spectrum = tempspec
        with open(csv_path, "w", newline='') as spectrum_csv:
            spectrum_csv.write(header)
            wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(spectrum)
            spectrum_csv.close()
        
        elapsed = t.time() - start
        print("Finished writing spectral csv file in: " + "{0:.2f}".format(elapsed) + "s")