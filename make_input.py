from func import midi_edit, audiospectrum_to_csv

samplingrate = 4096
timeflame = audiospectrum_to_csv.audio_to_spectroCSV("audio/Cello_Suite_1007_mono.wav","doc/spec.csv",samplingrate,0.1 ,False,False,True)
midi_edit.midi_edit("manual_mid.csv","doc/manual_mid_edit.csv",timeflame)

