import numpy as np
import os
import csv
import pandas as pd
import time as t
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, Dense

def NN(WriteFile=True,hiddenlayers=[100,100,100,100]):
    print("Reading data")
    start = t.time()
    x_ref = pd.read_csv(os.path.join('.','Data','Csv','refspec.csv'))
    y_ref = pd.read_csv(os.path.join('.','Data','Csv','reflabels.csv'))
    x_predict = pd.read_csv(os.path.join('.','Data','Csv','predspec.csv'))
    x_comperison = pd.read_csv(os.path.join('.','Data','Csv','compspec.csv'))
    y_comperison = pd.read_csv(os.path.join('.','Data','Csv','complabels.csv'))
    elapsed = t.time() - start
    print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")
    print("Preparing data")
    timeslices = x_predict["time in seconds"]
    x_ref = x_ref.values
    y_ref = y_ref.values
    x_predict = x_predict.values
    x_comperison = x_comperison.values
    y_comperison = y_comperison.values
    x_ref = x_ref.reshape(1,int(x_ref.shape[0]),int(x_ref.shape[1]))
    print(x_ref.shape,y_ref.shape)

    print("Training")
    start = t.time()
    model = Sequential()
    model.add(SimpleRNN(128, input_shape=(int(x_ref.shape[1]),int(x_ref.shape[2]))))
    model.add(Dense(int(y_ref.shape[1]),activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])
    model.summary()
    model.fit(x_ref,y_ref,validation_data=(x_comperison, y_comperison),batch_size=2,epochs=5)
    y_pred = model.predict(x_predict)
    print(y_pred)

    elapsed = t.time() - start
    print("Done training: " + "{0:.2f}".format(elapsed) + "s")

    if(WriteFile):
        header = "time in seconds"
        for value in range(128):
            header += "," + str(value)
        header += "\n"
        timeslices = timeslices.to_numpy()
        y_pred = y_pred.astype(object)
        y_pred = np.insert(y_pred,0,timeslices,axis=1)
        with open(os.path.join("Data","Output","prediction.csv"), "w", newline='') as result_csv:
            result_csv.write(header)
            wr = csv.writer(result_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(y_pred)
            result_csv.close()
        