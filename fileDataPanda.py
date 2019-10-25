import numpy as np
import os
import math
import pandas as pd
import csv
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc

AUDIO_PATH=os.path.join('..','Analysis','Audios (Conditions A-B-C)','S01-AT.wav')
CSV_OUTPUT_PATH=os.path.join('Data','Csv','Audio.csv')
MIDI_PATH=os.path.join('Data','Csv','Score','Miniature1.csv')
SPEC_PATH = os.path.join('Output','spectrum.csv')

def detect_onsets(specdata,mididata):
    list_of_frequencies = list(specdata.columns.values)
    list_of_frequencies.pop(0)
    min_pitch = math.pow(2,(mididata[3].min()-69)/12)*440
    max_pitch = math.pow(2,(mididata[3].max()-69)/12)*440
    for cols in specdata:
        if(cols != "time in samples"):
            if((float(cols) <= min_pitch or float(cols) >= max_pitch) and float(cols) != 0):
                specdata = specdata.drop(columns=cols)

    for cols in specdata:
        if(cols != "time in samples"):
            specdata['is larger than'] = np.where(specdata[cols] > 0.000000001, True, False)

    print(np.where(specdata['is larger than'] == True))
    return 0 #temporary measure

#TODO: fix data search method on how to find polyphonic data



def main():
    #cmc.convert_midi_to_csv()
    #asc.audio_to_spectroCSV(AUDIO_PATH,CSV_OUTPUT_PATH,256,0.75)
    mididata = pd.read_csv(MIDI_PATH,skiprows=1, header=None) #readmidiFile
    spectraldata = pd.read_csv(SPEC_PATH)
    compared_midi = detect_onsets(spectraldata,mididata)
    
    return 0

main()