import pickle
import csv
from func import filters

sampling_rate= 4098/44100

loaded_model = pickle.load(open('model.sav', 'rb'))
with open("doc/input2.csv","r") as f:
    input = [[float(l) for l in r] for r in csv.reader(f)]

with open("doc/result_model_0.csv","w") as f:
    i = 0
    writer = csv.writer(f,lineterminator="\n")
    for l in loaded_model.predict(input):
        writer.writerow([i,440*pow(2,(int(l)-69)/12)])
        i = i + sampling_rate