#Python module that generates a csv file with the frequency response of an audio file.
import numpy as np
import pandas as pd
import os
import csv
from scipy import signal
import soundfile as sf

def audio_to_spectroCSV(audio_path,csv_path,window_length,overlap):
    data, sr = sf.read(audio_path)                                      #Read audio file, works with any bitdepth
    window = signal.get_window(window=('tukey',0.25),Nx=window_length)
    noverlap = len(window)/overlap

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
    with open(os.path.join('Output','spectrum.csv'), "w", newline='') as spectrum_csv:
        spectrum_csv.write(header)
        wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
        wr.writerows(spectrum)
        spectrum_csv.close()
    print("finished writing spectral csv file")