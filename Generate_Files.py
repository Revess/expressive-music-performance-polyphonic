import numpy as np
import os
import math
import pandas as pd
import csv
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc

AUDIO_PATH=os.path.join('Data','Audio','S01-AT.wav')
MIDI_PATH = os.path.join('Data','Midi')
MIDI_CSV=os.path.join('Data','Csv')
SPEC_PATH = os.path.join('Data','Csv','spectrum.csv')

#cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)
asc.audio_to_spectroCSV(AUDIO_PATH,SPEC_PATH,16384,0.01,remove_silence=False,Show_Graph=False,Write_File=False)