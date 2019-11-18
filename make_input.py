from audiospectrum_to_csv import audio_to_spectroCSV as a2c
from midi_edit import midi_edit

samplingrate = 4096
timeflame = a2c("audio/Cello_Suite_1007_mono.wav","doc/spec.csv",samplingrate,0.1 ,False,False,True)
midi_edit("doc/manual_mid.csv","doc/manual_mid_edit.csv",timeflame)

