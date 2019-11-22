import sys
import os
sys.path.insert(1,os.path.join('library'))
import Generate_Files as gf
import NN as nn

# print("===========Generating_MIDI===========")
# gf.generate_files(GenerateMidi=True)
print("===========Generating_Inputs===========")
gf.generate_files(GenerateLabels=True,GenerateSpec=True,WriteFile=True,window=22050,overlapping=0.001953125*2)
print("===========Training===========")
nn.NN(hiddenlayers=[11000/2,11000/2,11000/4])
print("===========Generating_Output===========")
gf.generate_files(GenerateOutput=True)