import pandas as pd
import numpy as np
import csv

def shape_input(input_data,input_target,Add_context =False):

    data = pd.read_csv(input_data)
    timeframe = data.iat[1 ,0]
    if Add_context:
        with open(input_data,"r") as f:
            reader = list(csv.reader(f))
        data = [reader[i]+reader[i+1]+reader[i+2] for i in range(len(reader)-2)]
        with open(input_target,"r") as f:
            target = [[r[0]] for r in list(csv.reader(f))[1:-1]]
    else:
        data = data.drop(["time in seconds"],axis=1)
        target = pd.read_csv(input_target).drop(["time"], axis=1).drop(["power"], axis=1)

    if(len(data)<len(target)):
        target = target[:len(data)]
    else:
        data = data[:len(target)]

    target = np.ravel(target)
    
    return data, target, timeframe


