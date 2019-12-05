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
    MIDI_PATH = os.path.join('.','Data','Midi')

    #Original Score
    SCORELABELS_PATH = os.path.join('.','Data','Csv','scorelabels.csv')
    MIDI_SCORE = os.path.join('.','Data','Csv','ScoreMidi.csv')

    #Translations for reference audio
    REFERENCE_LABELS = os.path.join('.','Data','Csv','reflabels.csv')
    REFERENCE_AUDIO = os.path.join('.','Data','Audio','S01-CT.wav')
    REFERENCE_SPEC = os.path.join('.','Data','Csv','refspec.csv')
    REFERENCE_MIDI = os.path.join('.','Data','Csv','EditedScore1CT.csv')

    #Translations for comparision data
    COMPARISON_LABELS = os.path.join('.','Data','Csv','complabels.csv')
    COMPARISON_AUDIO = os.path.join('.','Data','Audio','S02-AT.wav')
    COMPARISON_SPEC = os.path.join('.','Data','Csv','compspec.csv')
    COMPARISON_MIDI = os.path.join('.','Data','Csv','EditedScore2AT.csv')

    #Translations for Predictions data
    PREDICTION_LABELS = os.path.join('.','Data','Output','prediction.csv')
    PREDICTION_SPEC = os.path.join('.','Data','Csv','predspec.csv')
    PREDICTION_AUDIO = os.path.join('.','Data','Audio','S02-AT.wav')
    PREDICTION_MIDI = os.path.join('.','Data','Output','predmidi.mid')


    #Write MIDI CSV
    if(midi):
        print("~~~~Midi to CSV~~~~")
        cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)
        print("\n")

    #Write SPECTRAL CSV
    if(spectral):
        print("~~~~Spectral to CSV~~~~")
        print("Transforming: " + str(REFERENCE_AUDIO))
        asc.audio_to_spectroCSV(REFERENCE_AUDIO,REFERENCE_SPEC,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")
        print("Transforming: " + str(COMPARISON_AUDIO))
        asc.audio_to_spectroCSV(COMPARISON_AUDIO,COMPARISON_SPEC,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")
        print("Transforming: " + str(PREDICTION_AUDIO))
        asc.audio_to_spectroCSV(PREDICTION_AUDIO,PREDICTION_SPEC,window,overlapping,remove_silence=removeSilence,Show_Graph=ShowGraph,Write_File=WriteFile)
        print("\n")

    #Writing LABELS CSV
    if(labels):
        print("~~~~Labels to CSV~~~~")
        print("Transforming: " + str(REFERENCE_LABELS))
        sotc.find_and_write_labels(REFERENCE_SPEC,REFERENCE_MIDI,REFERENCE_LABELS)
        print("\n")
        print("Transforming: " + str(COMPARISON_LABELS))
        sotc.find_and_write_labels(COMPARISON_SPEC,COMPARISON_MIDI,COMPARISON_LABELS)
        print("\n")
        # print("Transforming: " + str(SCORELABELS_PATH))
        # sotc.find_and_write_labels(REFERENCE_SPEC,MIDI_SCORE,SCORELABELS_PATH)
        # print("\n")

    if(output and not labels and not spectral):
        print("~~~~Labels to MIDI~~~~")
        otm.output_to_midi(PREDICTION_MIDI,PREDICTION_LABELS,DynTW=True)

    if(passthrough):
        otm.output_to_midi(PREDICTION_MIDI,REFERENCE_LABELS)