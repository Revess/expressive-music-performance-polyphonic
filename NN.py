import numpy as np
import os
import math
import pandas as pd
import csv
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn import datasets
import matplotlib
import matplotlib.pyplot as plt

SPEC_PATH = os.path.join('Data','Csv','spectrum.csv')
MIDI_SCORE = os.path.join('Data','Csv','ScoreMidi.csv')
MIDI_EDITED = os.path.join('Data','Csv','EditedScore.csv')
spectral_data = pd.read_csv(SPEC_PATH)
midi_score_data = pd.read_csv(MIDI_SCORE)
midi_edit_data = pd.read_csv(MIDI_EDITED)
def find_and_write_labels(spec,midi):
    midiSlices = []
    midiRow = []
    timeslice = 0
    #let's just test with 10 values instead of the full list
    for i in range(int(spec.shape[0])):
        timeslice = float(spec.loc[i,"time in seconds"])
        #print(timeslice)
        a = midi.loc[(midi["Onset_s"] >= timeslice) & (midi["Onset_s"]+midi["Duration_s"] <= timeslice),["Pitch_MIDI"]]
        if(a.size != 0):
            print(a)

    return 0

find_and_write_labels(spectral_data,midi_edit_data)
# model = svm.SVC()
# model.fit(spectraldata,midiscoredata["Pitch_MIDI"])

# test = mode
# l.predict()
# print(test)