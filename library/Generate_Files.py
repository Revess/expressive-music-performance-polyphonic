import os
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc
import slice_onsets_to_csv as sotc
import output_to_midi as otm

def generate_files(GenerateMidi = False, GenerateSpec = False, GenerateLabels = False, GenerateOutput = False, removeSilence = False, ShowGraph = False, WriteFile = False, passthrough = False,window=8192,overlapping=0.0175):
    #Alter bools to generate new files
    midi = GenerateMidi
    spectral = GenerateSpec
    labels = GenerateLabels
    output = GenerateOutput

    #Paths
    MIDI_CSV = os.path.join('.','Data','Csv')
    MIDI_SCORE = os.path.join('.','Data','Csv','ScoreMidi.csv')
    MIDI_EDITED = os.path.join('.','Data','Csv','EditedScore1CT.csv')
    MIDI2_EDITED = os.path.join('.','Data','Csv','EditedScore2AT.csv')
    MIDI_PATH = os.path.join('.','Data','Midi')
    OUTPUT_PATH = os.path.join('.','Data','Output','pred_midi.mid')
    PRED_MIDI_PATH = os.path.join('.','Data','Output','research.csv')
    SPEC_PATH = os.path.join('.','Data','Csv','spectrum.csv')
    SPEC2_PATH = os.path.join('.','Data','Csv','spectrum2.csv')
    SPEC3_PATH = os.path.join('.','Data','Csv','spectrum3.csv')
    AUDIO_PATH = os.path.join('.','Data','Audio','S01-CT.wav')
    AUDIO2_PATH = os.path.join('.','Data','Audio','S01-BT.wav')
    AUDIO3_PATH = os.path.join('.','Data','Audio','S01-AT.wav')
    LABELS_PATH = os.path.join('.','Data','Csv','labels.csv')
    LABELS2_PATH = os.path.join('.','Data','Csv','labels2.csv')

    #Write MIDI CSV
    if(midi):
        print("~~~~Midi to CSV~~~~")
        cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)
        print("\n")

    #Write SPECTRAL CSV
    if(spectral):
        print("~~~~Spectral to CSV~~~~")
        print("Transforming: " + str(AUDIO_PATH))
        asc.audio_to_spectroCSV(AUDIO_PATH,SPEC_PATH,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")
        print("Transforming: " + str(AUDIO2_PATH))
        asc.audio_to_spectroCSV(AUDIO2_PATH,SPEC2_PATH,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")
        print("Transforming: " + str(AUDIO3_PATH))
        asc.audio_to_spectroCSV(AUDIO3_PATH,SPEC3_PATH,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")

    #Writing LABELS CSV
    if(labels):
        print("~~~~Labels to CSV~~~~")
        print("Transforming: " + str(LABELS_PATH))
        sotc.find_and_write_labels(SPEC_PATH,MIDI_EDITED,LABELS_PATH)
        print("\n")
        print("~~~~Labels to CSV~~~~")
        print("Transforming: " + str(LABELS2_PATH))
        sotc.find_and_write_labels(SPEC3_PATH,MIDI2_EDITED,LABELS2_PATH)
        print("\n")

    if(output and not labels and not spectral):
        print("~~~~Labels to MIDI~~~~")
        otm.output_to_midi(OUTPUT_PATH,PRED_MIDI_PATH)

    if(passthrough):
        otm.output_to_midi(OUTPUT_PATH,LABELS_PATH)