import sys
import os
sys.path.insert(1,os.path.join('library'))
import Generate_Files as gf
import NN as nn

print("===========Generating_Inputs===========")
gf.generate_files(GenerateLabels=True,GenerateSpec=True,WriteFile=True,window=2205,overlapping=10)
print("===========Training===========")
nn.NN(hiddenlayers=[110,125])
print("===========Generating_Output===========")
gf.generate_files(GenerateOutput=True)