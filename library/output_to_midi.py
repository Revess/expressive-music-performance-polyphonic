import numpy as np
import pandas as pd
from midiutil.MidiFile import MIDIFile
import time as t

def output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH):
    print("reading csv file...")
    predmidi = pd.read_csv(PRED_MIDI_PATH)
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