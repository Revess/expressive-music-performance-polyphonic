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

def audio_to_spectroCSV(audio_path,csv_path,resolution,overlap,remove_silence,Show_Graph,Write_File):
    """
    audio_path: String
    Give path to Audio file

    csv_path: String
    Give path to .csv file

    resolution: Int
    Give resolution, must be a percentage between 0 and 100

    overlap: Int
    Give overlap amount in MS

    remove_silence: Bool
    Trim silence at start of an audio file

    Show_Graph: Bool
    Plot spectral graph

    Write_File: Bool
    Write data to audio file
    """
    spectrum = 0
    frequency = 0
    n = 0

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

    if(resolution <= 1 and overlap >= 0 and overlap < sr):
        #Place where the spectral data gets calculated
        print("Start calulating spectrum")
        start = t.time()
        print("Creating frequency scale...")
        overlap = int(((sr*resolution)/1000)*overlap)
        nfftL = int(sr*resolution)
        nfftM = int((sr/10)*resolution)
        nfftH = int((sr/100)*resolution)
        print("Generating 10-100Hz...")
        spectrumL = lb.core.stft(data,n_fft=nfftL,hop_length=overlap)
        spectrumL = np.abs(spectrumL)
        print("Generating 100-1000Hz...")
        spectrumM = lb.core.stft(data,n_fft=nfftM,hop_length=overlap)
        spectrumM = np.abs(spectrumM)
        print("Generating 1000-10kHz...")
        spectrumH = lb.core.stft(data,n_fft=nfftH,hop_length=overlap)
        spectrumH = np.abs(spectrumH)
        frequencyL = lb.core.fft_frequencies(sr=sr, n_fft=nfftL)
        frequencyM = lb.core.fft_frequencies(sr=sr, n_fft=nfftM)
        frequencyH = lb.core.fft_frequencies(sr=sr, n_fft=nfftH)
        print("Stitching FFT's together...")
        for frequency in frequencyL:
            if(frequency > 100):
                spectrumL = spectrumL[:-(frequencyL.shape[0]-n), :]
                frequencyL = frequencyL[:-(frequencyL.shape[0]-n)]
                n = 0
                for frequency in frequencyM:
                    if(frequency > 1000):
                        spectrumM = spectrumM[:n, :]
                        frequencyM = frequencyM[:n]
                        n = 0
                        for frequency in frequencyM:
                            if(frequency > 100):
                                spectrumM = spectrumM[n:, :]
                                frequencyM = frequencyM[n:] 
                                break   
                            else:
                                n+=1
                        n = 0
                        for frequency in frequencyH:
                            if(frequency > 1000):
                                spectrumH = spectrumH[n:, :]
                                frequencyH = frequencyH[n:]
                                break
                            else:
                                n+=1
                        break
                    else:
                        n+=1
                break
            else:
                n+=1
        print(spectrumL.shape,spectrumM.shape,spectrumH.shape)
        spectrum = np.concatenate((spectrumL,spectrumM,spectrumH),axis=0)
        frequency = np.concatenate((frequencyL,frequencyM,frequencyH),axis=0)
        times = ft.frame_timer(int(data.shape[0]),int(spectrum.shape[1]),sr)
        elapsed = t.time() - start
        print("Done calculating spectrum in: " + "{0:.2f}".format(elapsed) + "s")
        print("The spectrum is a matrix with: " + str(int(spectrum.shape[0])) + " frequency bins & " + str(int(spectrum.shape[1])) + " time slices")
        print("Each time frame is: ~" + "{0:.2f}".format((times[2]-times[1])*1000) + "ms")
        print("The lowest frequency interval is: ~" + "{0:.2f}".format(frequencyL[2] - frequencyL[1]) + "Hz")
        print("The middle frequency interval is: ~" + "{0:.2f}".format(frequencyM[2] - frequencyM[1]) + "Hz")
        print("The highest frequency interval is: ~" + "{0:.2f}".format(frequencyH[2] - frequencyH[1]) + "Hz")

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
        spectrum = np.insert(spectrum,0,times,1)

        with open(csv_path, "w", newline='') as spectrum_csv:
            spectrum_csv.write(header)
            wr = csv.writer(spectrum_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(spectrum)
            spectrum_csv.close()
        
        elapsed = t.time() - start
        print("Finished writing spectral csv file in: " + "{0:.2f}".format(elapsed) + "s")