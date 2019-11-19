import numpy as np
import pandas as pd
from midiutil.MidiFile import MIDIFile
import time as t
from dtw import *
import os

MIDIDATACSV = os.path.join('Data','Csv','ScoreMidi.csv')

def rescale_midi(midiDataCsv,midiLabels):
    score = pd.read_csv(midiDataCsv)
    labels = midiLabels
    x_score = np.array([],dtype=int)
    y_labels = np.array([],dtype=int)
    start_silence = np.array([])
    timeslice = labels["time in seconds"].to_numpy(dtype=float)
    labels = labels.drop(["time in seconds"],1)
    notes = labels.columns.values.astype(dtype=int)
    scaling_factor = timeslice[int(timeslice.shape[0])-1]/score.loc[int(score.shape[0])-1,"Onset_s"]

    #transform score data into an array of same length midinotes
    #stretch the length of the data to match labels length
    if(int(timeslice.shape[0]) != int(score.shape[0])):
        x_score = np.append(x_score,score.loc[0,"Pitch_MIDI"])
        for i in range(int(labels.shape[0])):
            for j in range(int(score.shape[0])):
                if((score.loc[j,"Onset_s"]*scaling_factor) <= timeslice[i] and ((score.loc[j,"Onset_s"] + score.loc[j,"Duration_s"])*scaling_factor) >= timeslice[i]):
                    x_score = np.append(x_score,score.loc[j,"Pitch_MIDI"])
    #transform labels into an array of midi notes
    for i in range(int(labels.shape[0])):
        stepcounter = 0
        for j in range(int(labels.shape[1])):
            value = labels.iloc[i,j]
            if(value != 0):
                y_labels = np.append(y_labels,notes[j])
            else:
                stepcounter += 1
        if(stepcounter == 128):
            y_labels = np.append(y_labels,128)
    # x_score = x_score.reshape(-1,1)
    # y_labels = y_labels.reshape(-1,1)
    print(x_score,y_labels)
    euclidean_norm = lambda x, y: np.abs(x_score - y_labels)
    d, cost_matrix, acc_cost_matrix, path = dtw(x_score, y_labels, dist=euclidean_norm)
    import matplotlib.pyplot as plt

    plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
    plt.plot(path[0], path[1], 'w')
    plt.show()
    return 0

def output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH):
    print("reading csv file...")
    predmidi = pd.read_csv(PRED_MIDI_PATH)
    rescale_midi(MIDIDATACSV,predmidi)

    timeslice = predmidi["time in seconds"].to_numpy(dtype=float)
    predmidi = predmidi.drop(["time in seconds"],1)
    mididata = [[i for i in range(128)]]
    mididata.append([0]*128)
    print("Transforming data...")
    for i in range(2):
        mididata.append([float(0)]*128)
    mididata = np.array(mididata, dtype=object)
    mididata = pd.DataFrame({'pitch': mididata[0,:], 'bool': mididata[1,:], 'onset_s': mididata[2,:],'offset_s': mididata[3,:]})
    mididata.astype(object)
    numnotes = 0

    #Midi Settings
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track
    time = 0    # start at the beginning
    tempo = 120
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, tempo)

    # add some notes
    channel = 0
    volume = 100
    for i in range(int(predmidi.shape[0])):
        for j in range(int(predmidi.shape[1])):
            x = predmidi.iloc[i,j]
            if(x == 0):
                if(mididata.iloc[j,1] != x):
                    mididata.iloc[j,1] = x
                    mididata.iloc[j,3] = timeslice[i]
            else:
                if(mididata.iloc[j,1] != x):
                    mididata.iloc[j,1] = x
                    mididata.iloc[j,2] = timeslice[i]
        for j in range(int(mididata.shape[0])):
            if(mididata.iloc[j,2] != 0 and mididata.iloc[j,3] != 0):
                time = ((mididata.iloc[j,2] * 1000)/60000) * tempo
                duration = (((mididata.iloc[j,3] - mididata.iloc[j,2])* 1000)/60000) * tempo
                pitch = mididata.iloc[j,0]
                numnotes+=1
                mf.addNote(track, channel, pitch, time, duration, volume)
                mididata.iloc[j,2] = 0
                mididata.iloc[j,3] = 0
    print("number of generated notes: " + str(numnotes))
    print("Writing midi file...")
    # write it to disk
    with open(OUTPUT_PATH, 'wb') as outf:
        mf.writeFile(outf)
    print("Done!...")