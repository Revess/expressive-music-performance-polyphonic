#Python module that generates a csv file with the frequency response of an audio file.
import numpy as np
import pandas as pd
import os
import csv
from scipy import signal
import soundfile as sf
import librosa as lb

def audio_to_spectroCSV(audio_path,csv_path,window_length,overlap,remove_silence):
    data, sr = sf.read(audio_path)                      #Read audio file, works with any bitdepth
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

    print("Converting audio to spectral data")
    window = signal.get_window(window=('tukey',0.25),Nx=window_length)
    noverlap = len(window)*overlap
    #spectrotransform
    frequency, times, spectrum = signal.spectrogram(x=data,fs=sr,window=window,noverlap=noverlap)
    #Put all the spectral information in one big array, but 90 degrees flipped to put the frequencies on top and timings on the left, 
    #for easier time tracking
    #Create header in string
    header = "time in samples"
    for data in frequency:
        header += "," + str(data)
    header += "\n"
    spectrum = np.rot90(spectrum)
    spectrum = np.insert(spectrum,0,times,1)

    #Write to csv file
    with open(csv_path, "w", newline='') as spectrum_csv:
        spectrum_csv.write(header)
        wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
        wr.writerows(spectrum)
        spectrum_csv.close()
    print("Finished writing spectral csv file")