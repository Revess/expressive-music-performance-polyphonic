#Python module that generates a csv file with the frequency response of an audio file.
import numpy as np
import pandas as pd
import os
import csv
from scipy import signal
import librosa as lb
import librosa.display
import matplotlib.pyplot as plt

def audio_to_spectroCSV(audio_path,csv_path,nfft,overlap,remove_silence):
    data, sr = lb.load(audio_path) #Read audio file, works with any bitdepth
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
    
    Spectrum = lb.core.stft(data,n_fft=nfft,hop_length=overlap)
    Spectrum=np.abs(Spectrum)
    pitches, magnitudes = lb.core.piptrack(sr=sr,S=Spectrum,n_fft=nfft,hop_length=overlap,fmax=10000)
    print(pitches[1],magnitudes)

    # header = "time in samples"
    # for data in frequency:
    #     header += "," + str(data)
    # header += "\n"
    # spectrum = np.rot90(spectrum)
    # spectrum = np.insert(spectrum,0,times,1)

#     #Write to csv file
#     with open(csv_path, "w", newline='') as spectrum_csv:
# #        spectrum_csv.write(header)
#         wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
#         wr.writerows(Spectrum)
#         spectrum_csv.close()
#     print("Finished writing spectral csv file")