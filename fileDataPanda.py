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

def main():
    cmc.convert_midi_to_csv()
    asc.audio_to_spectroCSV(AUDIO_PATH,CSV_OUTPUT_PATH,128,2)
    mididata = pd.read_csv(MIDI_PATH, header=None) #readmidiFile
    spectraldata = pd.read_csv(SPEC_PATH)

    
    return 0

main()