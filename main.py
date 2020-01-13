import sys
import os
sys.path.insert(1,os.path.join('library'))
import Generate_Files as gf
import NN as nn

# print("===========Generating_Inputs===========")
# gf.generate_files(GenerateInput=True,window=2048,overlapping=0.25)
print("===========Training===========")
nn.NN()
print("===========Generating_Output===========")
gf.generate_files(GenerateOutput=True)