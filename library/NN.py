import numpy as np
import os
import csv
import pandas as pd
import time as t
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Embedding, SimpleRNN, Dense

def NN(WriteFile=True,numNodes=256):
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
    x_ref = x_ref.drop(["time in seconds"],1)
    y_ref = y_ref.drop(["time in seconds"],1)
    x_comperison = x_comperison.drop(["time in seconds"],1)
    y_comperison = y_comperison.drop(["time in seconds"],1)
    x_predict = x_predict.drop(["time in seconds"],1)
    x_ref = x_ref.values
    y_ref = y_ref.values
    x_predict = x_predict.values
    x_comperison = x_comperison.values
    y_comperison = y_comperison.values
    x_ref = x_ref.reshape(int(x_ref.shape[0]),int(x_ref.shape[1]),1)
    x_comperison = x_comperison.reshape(int(x_comperison.shape[0]),int(x_comperison.shape[1]),1)
    x_predict = x_predict.reshape(int(x_predict.shape[0]),int(x_predict.shape[1]),1)
    print(x_ref.shape,y_ref.shape)

    print("Training")
    model = Sequential()
    model.add(SimpleRNN(numNodes, input_shape=(int(x_ref.shape[1]),int(x_ref.shape[2])),return_sequences=False))
    model.add(Dense(int(y_ref.shape[1]),activation='sigmoid'))
    # model.add(Dense(int(y_ref.shape[1]),activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])
    model.summary()
    model.fit(x_ref,y_ref,validation_data=(x_comperison, y_comperison),batch_size=2,epochs=2)
    y_pred = model.predict(x_predict)
    acc = model.evaluate(x_comperison, y_comperison)
    print("accuracy: " + str(acc))
    print(y_pred)
    # y_pred[y_pred <= 0.5] = 0
    # y_pred[y_pred > 0.5] = 1
    y_pred = y_pred.astype(int)
    print(y_pred)
    print("Done training")

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
        