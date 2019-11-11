import sys
import os
sys.path.insert(1,os.path.join('library'))
import Generate_Files as gf
import NN as nn

# print("===========Generating_MIDI===========")
# gf.generate_files(GenerateMidi=True)
print("===========Generating_Inputs===========")
gf.generate_files(GenerateLabels=True,GenerateSpec=True,WriteFile=True,window=2048*8,overlapping=4)
print("===========Training===========")
nn.NN(hiddenlayers=[int(10837/4),int(10837/4),100])
print("===========Generating_Output===========")
gf.generate_files(GenerateOutput=True)