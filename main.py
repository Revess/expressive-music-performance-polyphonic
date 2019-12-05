import sys
import os
sys.path.insert(1,os.path.join('library'))
import Generate_Files as gf
import NN as nn

# print("===========Generating_MIDI===========")
# gf.generate_files(GenerateMidi=True)
# print("===========Generating_Inputs===========")
# gf.generate_files(GenerateLabels=True,GenerateSpec=True,WriteFile=True,window=8192,overlapping=0.0125)
#Transform lables
print("===========Training===========")
nn.NN(hiddenlayers=[5523,5523])
print("===========Generating_Output===========")
gf.generate_files(GenerateOutput=True)