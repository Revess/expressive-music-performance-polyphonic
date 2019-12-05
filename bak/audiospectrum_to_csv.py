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
    """
    A audio spectrum analyizing tool that converts the input file to a .csv file

    audio_path (string): audio file path
    csv_path (string): csv file path
    nfft (int): give fft window size in samples
    overlap (float): give percentage (in decimalpoint) the amount of overlap to be given
    remove_silence (bool): trim start silence of piece of audio
    Show_Graph (bool): show a spectrogram graph of the analysis
    Write_File (bool): Write output to file if true
    """
    data, sr = lb.core.load(audio_path)
    data = lb.util.normalize(data)
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
    overlap = int(nfft*overlap)
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
        spectrum = np.rot90(spectrum)
        spectrum = np.flip(spectrum,0)
        tempspec = np.zeros((spectrum.shape[0],spectrum.shape[1]*4))
        for timeindex in range(int(tempspec.shape[0])):
            for freqindex in range(int(tempspec.shape[1])):
                modfreq = int(freqindex/4)
                modindex = freqindex % 4
                if(timeindex == 0):
                    if(modindex == 0):
                        tempspec[timeindex,freqindex] = 0
                    elif(modindex == 1):
                        tempspec[timeindex,freqindex] = spectrum[timeindex,modfreq]
                    elif(modindex == 2):
                        tempspec[timeindex,freqindex] = spectrum[timeindex+1,modfreq]
                    elif(modindex == 3):
                        tempspec[timeindex,freqindex] = spectrum[timeindex+2,modfreq]
                elif(timeindex >= int(tempspec.shape[0])-1):
                    if(modindex == 0):
                        tempspec[timeindex,freqindex] = spectrum[timeindex-1,modfreq]
                    elif(modindex == 1):
                        tempspec[timeindex,freqindex] = spectrum[timeindex,modfreq]
                    elif(modindex == 2):
                        tempspec[timeindex,freqindex] = 0
                    elif(modindex == 3):
                        tempspec[timeindex,freqindex] = 0
                elif(timeindex == int(tempspec.shape[0])-2):
                    if(modindex == 0):
                        tempspec[timeindex,freqindex] = spectrum[timeindex-1,modfreq]
                    elif(modindex == 1):
                        tempspec[timeindex,freqindex] = spectrum[timeindex,modfreq]
                    elif(modindex == 2):
                        tempspec[timeindex,freqindex] = spectrum[timeindex+1,modfreq]
                    elif(modindex == 3):
                        tempspec[timeindex,freqindex] = 0
                elif(timeindex != 0):
                    if(modindex == 0):
                        tempspec[timeindex,freqindex] = spectrum[timeindex-1,modfreq]
                    elif(modindex == 1):
                        tempspec[timeindex,freqindex] = spectrum[timeindex,modfreq]
                    elif(modindex == 2):
                        tempspec[timeindex,freqindex] = spectrum[timeindex+1,modfreq]
                    elif(modindex == 3):
                        tempspec[timeindex,freqindex] = spectrum[timeindex+2,modfreq]

        spectrum = tempspec
        spectrum = np.insert(spectrum,0,times,1)
        header = "time in seconds"
        for freqindex in range(int(spectrum.shape[1])-1):
            mod = freqindex % 4
            if(mod == 0):
                header += "," + str(frequency[round(freqindex/4)])
            else:
                header += "," + " "
        header += "\n"

        with open(csv_path, "w", newline='') as spectrum_csv:
            spectrum_csv.write(header)
            wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(spectrum)
            spectrum_csv.close()
        
        elapsed = t.time() - start
        print("Finished writing spectral csv file in: " + "{0:.2f}".format(elapsed) + "s")