import numpy as np
import pandas as pd
from midiutil.MidiFile import MIDIFile

def output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH):
    predmidi = pd.read_csv(PRED_MIDI_PATH)
    print(predmidi.shape)
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100
    duration = 1
    for i in range(int(predmidi.shape[0])):
        for j in range(int(predmidi.shape[1])):
            x = predmidi.iloc[i,j]
            if(x == 1):
                pitch = j
                time = i
                mf.addNote(track, channel, pitch, time, duration, volume)

    # write it to disk
    with open(OUTPUT_PATH, 'wb') as outf:
        mf.writeFile(outf)
    return 0