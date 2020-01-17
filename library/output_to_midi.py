import numpy as np
import pandas as pd
from midiutil.MidiFile import MIDIFile
import time as t
import os
from matplotlib import pyplot as plt
from dtw import dtw,warp

MIDISCORE_PATH = os.path.join("Data","Csv","Scores","ScoreMidi.csv")

def labels_to_notes(labels):
    y_labels = np.array([],dtype=int)
    labels = labels.drop(["time in seconds"],1)
    notes = labels.columns.values.astype(dtype=int)
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
    return y_labels

def stretch(predictions,score,timeslices):
    midiSlices = []
    scalingFactor = predictions.loc[int(predictions.shape[0])-1,"time in seconds"]/score.loc[int(score.shape[0])-1,"Onset_s"]
    for j in range(int(predictions.shape[0])):
        midiRow = [0] * 128
        timeslice = float(predictions.loc[j,"time in seconds"])
        for i in range(int(score.shape[0])):
            if((score.loc[i,"Onset_s"] * scalingFactor) <= timeslice):
                if(((score.loc[i,"Onset_s"] + score.loc[i,"Duration_s"]) * scalingFactor) >= timeslice):
                    midiRow[int(score.loc[i,"Pitch_MIDI"])] = 1
        midiRow.insert(0,timeslice)
        midiSlices.append(midiRow)
    midiSlices = np.array(midiSlices)
    return midiSlices

def dtwtransform(predictions,score,plot=False):
    #Predict the DTW
    timeslices = predictions["time in seconds"].to_numpy(dtype=float)
    score = stretch(predictions,score,timeslices)
    predictions = predictions.to_numpy()
    alignment = dtw(predictions,score)
    warped = warp(alignment,index_reference=False)
    #Plot outcome if nescesarry
    if(plot):
        plt.plot(alignment.index1,alignment.index2) 
        plt.plot(predictions[warped])
        plt.show()
        np.savetxt(("Data/bak/output.txt"),predictions[warped])
    return predictions[warped]

def output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH,DynTW=True):
    print("reading csv file...")
    predmidi = pd.read_csv(PRED_MIDI_PATH)
    scoremidi = pd.read_csv(MIDISCORE_PATH)
    #Do a DTW transformation
    if(DynTW):
        columns = predmidi.columns.values
        predmidi = dtwtransform(predmidi,scoremidi,plot=False)
        predmidi = pd.DataFrame(predmidi,columns=columns)
    timeslice = predmidi["time in seconds"]
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
                duration = abs((((mididata.iloc[j,3] - mididata.iloc[j,2])* 1000)/60000) * tempo)
                pitch = mididata.iloc[j,0]
                numnotes+=1
                mf.addNote(track, channel, pitch, time, duration, volume)
                if(duration < 0 or time < 0):
                    print(duration,time)
                    print(mididata.iloc[j,2],mididata.iloc[j,3])
                mididata.iloc[j,2] = 0
                mididata.iloc[j,3] = 0
    print("number of generated notes: " + str(numnotes))
    print("Writing midi file...")
    # write it to disk
    with open(OUTPUT_PATH, 'wb') as outf:
        mf.writeFile(outf)
    print("Done!...")