import pandas as pd
import numpy as np
import csv
import time 

def shape_input(input_data,input_target,Add_context =False):

    t1 = time.time()

    if Add_context:
        with open(input_data,"r") as f:
            reader = list(csv.reader(f))[1:]
        timeframe = reader[1][0]
        data = pd.DataFrame([reader[i][1:]+reader[i+1][1:]+reader[i+2][1:] for i in range(len(reader)-2)])
        with open(input_target,"r") as f:
            target = pd.DataFrame([[r[1]] for r in list(csv.reader(f))[2:-1]])
    else:    
        data = pd.read_csv(input_data)
        timeframe = data.iat[1 ,0]
        data = data.drop(["time in seconds"],axis=1)
        target = pd.read_csv(input_target).drop(["time"], axis=1).drop(["power"], axis=1)

    if(len(data)<len(target)):
        target = target[:len(data)]
    else:
        data = data[:len(target)]

    target = np.ravel(target)

    print("finish shaping in " + str(time.time( ) - t1 ))

    return data, target, float(timeframe)


