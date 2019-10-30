import os
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc
import slice_onsets_to_csv as sotc

midi=False
spectral = False
labels = True

#Paths
MIDI_CSV = os.path.join('Data','Csv')
MIDI_SCORE = os.path.join('Data','Csv','ScoreMidi.csv')
MIDI_EDITED = os.path.join('Data','Csv','EditedScore.csv')
MIDI_PATH = os.path.join('Data','Midi')
SPEC_PATH = os.path.join('Data','Csv','spectrum.csv')
AUDIO_PATH = os.path.join('Data','Audio','S01-AT.wav')
LABELS_PATH = os.path.join('Data','Csv','labels.csv')

#Write MIDI CSV
if(midi):
    cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)

#Write SPECTRAL CSV
if(spectral):
    asc.audio_to_spectroCSV(AUDIO_PATH,SPEC_PATH,8192,0.075,remove_silence=False,Show_Graph=False,Write_File=True)

#Writing LABELS CSV
if(labels):
    sotc.find_and_write_labels(SPEC_PATH,MIDI_EDITED,LABELS_PATH)