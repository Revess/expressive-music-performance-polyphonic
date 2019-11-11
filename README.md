# expressive-music-performance-polyphonic
In this branch you will find the right code for the polyphonic analisis
File explenation:
  The following files can be ignored by the user and cannot run on their own.
    -audiospectrum_to_csv.py:
      Stft transform an audio file and write it to a .csv file
    -convert_midi_to_csv.py: (Created by Sergio)
      Convert a .mid file to a .csv file
    -output_to_midi.py:
      Convert the output of the NN.py to a .mid file (incomplete code)
    -Slice_onsets_to_csv.py:
      Write the labels for the NN by comparing time onsets of the 
      midi data to the timeslices of the spectral data.

  -Main.py:
    Contains all functions and is the file to easily run all functions nescesarry
    
  -Generate_Files.py:
    Run this file to generate any of the above called functions, 
    edit the boolean parameters at the start and start writing the right files to csv.

  -NN.py:
    Run this file to run the Neural Network.

TODO:
  -Improve NN output
