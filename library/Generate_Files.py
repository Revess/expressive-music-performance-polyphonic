import os
import audiospectrum_to_csv as asc
import convert_midi_to_csv as cmc
import slice_onsets_to_csv as sotc
import output_to_midi as otm

def generate_files(GenerateOutput=False,GenerateInput=False,window=4056,overlapping=0.125):
    #Paths
    MIDI_CSV = os.path.join('.','Data','Csv','Scores')
    MIDI_PATH = os.path.join('.','Data','Midi','Original')
    MIDI_EDIT1 = os.path.join('.','Data','Csv','Scores','EditedSCore1CT.csv')
    LABELS_PATH = os.path.join('.','Data','Csv','Labels')
    SPECTRUM_PATH = os.path.join('.','Data','Csv','Spectrum')
    SPECTRUM_DIR = os.listdir(SPECTRUM_PATH)
    AUDIO_PATH = os.path.join('.','Data','Audio')
    AUDIO_DIR = os.listdir(AUDIO_PATH)
    PREDICTIONS_PATH = os.path.join('.','Data','Csv','Predictions')
    PREDICTIONS_DIR = os.listdir(PREDICTIONS_PATH)
    OUTPUT_PATH = os.path.join('.','Data','Midi','Output')
 

    #Generating inputs
    if(GenerateInput):
        print("~~~~Midi to CSV~~~~")
        cmc.convert_midi_to_csv(MIDI_PATH,MIDI_CSV)
        print("\n")
        # print("~~~~Spectral to CSV~~~~")
        # for fileName in AUDIO_DIR:
        #     if fileName[-3:] == 'wav':
        #         SPECTRUM_FILE_PATH = os.path.join(SPECTRUM_PATH, fileName[:-3]+"csv")
        #         AUDIO_FILE_PATH = os.path.join(AUDIO_PATH, fileName)
        #         print("Transforming: " + str(fileName))
        #         asc.audio_to_spectroCSV(AUDIO_FILE_PATH,SPECTRUM_FILE_PATH,window,overlapping)
        #         print("\n")
        print("~~~~Labels to CSV~~~~")
        for fileName in SPECTRUM_DIR:
            if fileName[-3:] == 'csv':
                LABLE_FILE_PATH = os.path.join(LABELS_PATH, fileName[:-3]+"csv")
                SPECTRUM_FILE_PATH = os.path.join(SPECTRUM_PATH, fileName)
                print("Transforming: " + str(fileName))
                sotc.find_and_write_labels(SPECTRUM_FILE_PATH,MIDI_EDIT1,LABLE_FILE_PATH)
                print("\n")
    
    #Generate Output
    if(GenerateOutput):
        print("~~~~Labels to MIDI~~~~")
        for fileName in PREDICTIONS_DIR:
            if fileName[-3:] == 'csv':
                OUTPUT_FILE_PATH = os.path.join(OUTPUT_PATH, fileName[:-3]+"mid")
                PREDICTION_FILE_PATH = os.path.join(PREDICTIONS_PATH, fileName)
                otm.output_to_midi(OUTPUT_FILE_PATH,PREDICTION_FILE_PATH,DynTW=True)