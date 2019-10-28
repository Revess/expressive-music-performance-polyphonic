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
spectraldata = pd.read_csv(SPEC_PATH)
midiscoredata = pd.read_csv(MIDI_SCORE)
midieditdata = pd.read_csv(MIDI_EDITED)

# model = svm.SVC()
# model.fit(spectraldata,midiscoredata["Pitch_MIDI"])

# test = mode
# l.predict()
# print(test)