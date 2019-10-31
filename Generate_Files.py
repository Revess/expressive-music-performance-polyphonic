import os
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc
import slice_onsets_to_csv as sotc
import output_to_midi as otm

#Alter bools to generate new files
midi=False
spectral = False
labels = False
output = True

#Paths
MIDI_CSV = os.path.join('Data','Csv')
MIDI_SCORE = os.path.join('Data','Csv','ScoreMidi.csv')
MIDI_EDITED = os.path.join('Data','Csv','EditedScore.csv')
MIDI_PATH = os.path.join('Data','Midi')
OUTPUT_PATH = os.path.join('Data','Output','pred_midi.mid')
PRED_MIDI_PATH = os.path.join('Data','Output','Research.csv')
SPEC_PATH = os.path.join('Data','Csv','spectrum.csv')
AUDIO_PATH = os.path.join('Data','Audio','S01-AT.wav')
LABELS_PATH = os.path.join('Data','Csv','labels.csv')

#Write MIDI CSV
if(midi):
    print("~~~~Midi to CSV~~~~")
    cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)
    print("\n")

#Write SPECTRAL CSV
if(spectral):
    print("~~~~Spectral to CSV~~~~")
    asc.audio_to_spectroCSV(AUDIO_PATH,SPEC_PATH,8192*2,0.025,remove_silence=False,Show_Graph=False,Write_File=True)
    print("\n")

#Writing LABELS CSV
if(labels):
    print("~~~~Labels to CSV~~~~")
    sotc.find_and_write_labels(SPEC_PATH,MIDI_EDITED,LABELS_PATH)

if(output):
    print("~~~~Labels to MIDI~~~~")
    otm.output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH)