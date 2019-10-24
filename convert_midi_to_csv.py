import numpy as np
import os
import math
import py_midicsv
import pandas as pd
import csv
import random
import audiospectrum_to_csv

MIDI_PATH = os.path.join("Data","Midi")
CSV_PATH = os.path.join("Data", "Csv")
DATA_PATH = os.path.join("Data")
SEMITONES_IN_OCTAVE = 12
QUARTER_NOTE = 4
NOTE_NUM = {"C"    :0,
            "C#"   :1,
            "Db"   :1,
            "D"    :2,
            "D#"   :3,
            "Eb"   :3,
            "E"    :4,
            "F"    :5,
            "F#"   :6,
            "Gb"   :6,
            "G"    :7,
            "G#"   :8,
            "Ab"   :8,
            "A"    :9,
            "A#"   :10,
            "Bb"   :10,
            "B"    :11}

CIRCLE_OF_5THS = ["C","G","D","A","E","B","F#","C#","Db","Gb","Db" ,"Ab","Eb","Bb","F"]

def convert_midi_to_csv(midi_path=MIDI_PATH, csv_path=CSV_PATH, folder="Score",write_midi_cvs_to_file=False):
    # convert_midi_to_csv: Retrieves MIDI files at a folder and creates the corresponding csv converted files.
    # It uses py_midicsv, to obtain a csv type MIDI event file. Then it uses the midi_to_nmat to obtain a note 
    # matrix representation of the notes. The note matrix representation is saved as a csv file. 

    files_list = os.listdir(os.path.join(midi_path,folder))
    
    for file_name in files_list:
        if file_name[-3:] == 'mid':
            print("Converting:" + file_name + "...", end="")
            midi_file_path = os.path.join(midi_path, folder, file_name)
            csv_file_path = os.path.join(csv_path, folder, file_name[:-3]+"csv")
            midi_csv_list = py_midicsv.midi_to_csv(midi_file_path)
            nmat = midi_to_nmat(midi_csv_list)# midi_csv to nmat_csv

            with open(csv_file_path, 'w', newline='') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_NONE)
                wr.writerows(nmat)
                myfile.close
                
            if write_midi_cvs_to_file:
                midi_csv_file_path = os.path.join(csv_path, folder, file_name[:-4] + "_MIDI.csv") 
                csvfile = open(midi_csv_file_path,'w')
                csvfile.writelines(midi_csv_list)
                csvfile.close()

            print("Done!")

def midi_to_nmat(midi_csv_list):
    #Returns a square list of lists
    #NOTE: works only for one channel MIDI files
    
    CH = 0
    TIME = 1
    CONTROL = 2
    CTL_VAL = 3
    PITCH = 4
    VEL = 5
    MICROSECS=10e5
    
    #initialize values
    tempo = float('nan')
    time_sig = float('nan')
    time_sig_num = float('nan')
    time_sig_den = float('nan')
    key = float('nan')
    mode = float('nan')
    
    nmat = []
    notes = []#to keep track of on/off note status, note onset, and index at the nmat structure, in order to obtain duration
    header = ["Onset_b",
              "Duration_b",
              "Channel_MIDI",
              "Pitch_MIDI",
              "Vel_MIDI",
              "Onset_s",
              "Duration_s",
              "Time_signature",
              "T_sig_num",
              "T_sig_den",
              "Key_5th_num",
              "Key_nominal",
              "Mode",
              "Tempo"]
    
    for i in range(127): notes.append({"status":"off", "onset":None, "note_idx_on_nmat":None }) #to store on off status of notes
    nmat_idx = 0
    for line in midi_csv_list:
        msg = line.split(', ')
                
        if (msg[CONTROL] == "Header"): #Header is always first message
            beat_grid = float(msg[CTL_VAL+2])# corresponds to VEL colum, but at Header control message refers to beat grid
        
        elif (msg[CONTROL] == "Tempo"):
            tempo = float(msg[CTL_VAL])
            
        elif (msg[CONTROL] == "Time_signature"):
            time_sig = msg[CTL_VAL]+"/"+ str(2**int(msg[CTL_VAL+1]))
            time_sig_num = int(msg[CTL_VAL])
            time_sig_den = 2**int(msg[CTL_VAL+1])
            
        elif (msg[CONTROL] == "Key_signature"):
            key = int(msg[CTL_VAL])
            mode = msg[CTL_VAL+1].replace('\n','').replace('"','')

        elif len(msg) == 6:
            
            if ((msg[CONTROL] == "Note_on_c") and (notes[int(msg[PITCH])]["status"] == "off") and (int(msg[VEL]) is not 0)):#is note on
                #create note row
                nmat_row = []
            
                #update notes array
                notes[int(msg[PITCH])]["status"] = "on"#set note status on
                notes[int(msg[PITCH])]["onset"] = float(msg[TIME])# store note onset
                notes[int(msg[PITCH])]["note_idx_on_nmat"] = nmat_idx# store note index at nmat
            
                #append Onset(beats)
                onset_b = float(msg[TIME])/beat_grid
                nmat_row.append(onset_b)
                #append MIDI Chanell
                nmat_row.append(float(msg[CH]))
                #append MIDI pitch
                nmat_row.append(float(msg[PITCH]))
                #append MIDI velocity
                nmat_row.append(float(msg[VEL]))
                #append Onset(sec)
                onset_s = tempo*onset_b/MICROSECS
                nmat_row.append(onset_s)
                #append row to nmat
                nmat.append(nmat_row)
                nmat_idx += 1
                #append time signature
                nmat_row.append(time_sig)
                nmat_row.append(time_sig_num)
                nmat_row.append(time_sig_den)
                
                #append key
                nmat_row.append(key)
                #append key nominal
                if not math.isnan(key): 
                    nmat_row.append(CIRCLE_OF_5THS[int(key)])
                else:
                    nmat_row.append(key)
                #append_mode
                nmat_row.append(mode)
                #append_tempo
                nmat_row.append(60*MICROSECS/tempo)
            
              
            elif ((msg[CONTROL] == "Note_on_c" and int(msg[VEL]) == 0) or (msg[CONTROL],"Note_off_c")) and (notes[int(msg[PITCH])]["status"] == "on"):#note off
            
                #insert Duration(Beats) at the second position at note index in nmat
                dur_b = (float(msg[TIME]) - notes[int(msg[PITCH])]["onset"])/beat_grid
                nmat[notes[int(msg[PITCH])]["note_idx_on_nmat"]].insert(1,dur_b)
                #insert Duration(sec) at the 7th position
                dur_s = tempo*dur_b/MICROSECS
                nmat[notes[int(msg[PITCH])]["note_idx_on_nmat"]].insert(6,dur_s)
            
                #update notes array
                notes[int(msg[PITCH])]["status"] = "off"
                notes[int(msg[PITCH])]["onset"] = None

    nmat.insert(0,header)
    return nmat