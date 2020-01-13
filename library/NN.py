import numpy as np
import os
import csv
import pandas as pd
import time as t
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Embedding, SimpleRNN, Dense, Flatten,Dropout
from matplotlib import pyplot

def NN(WriteFile=True):
    print("Reading data")
    start = t.time()
    x_ref = pd.read_csv(os.path.join('.','Data','Csv','Spectrum','S01-CT.csv'))
    y_ref = pd.read_csv(os.path.join('.','Data','Csv','Labels','S01-CT.csv'))
    x_predict = pd.read_csv(os.path.join('.','Data','Csv','Spectrum','S02-CT.csv'))
    x_comperison = pd.read_csv(os.path.join('.','Data','Csv','Spectrum','S02-AT.csv'))
    y_comperison = pd.read_csv(os.path.join('.','Data','Csv','Labels','S02-AT.csv'))
    elapsed = t.time() - start
    print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")
    print("Preparing data")
    timeslices = x_predict.loc[:,"time in seconds"]

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
    # cb_list = [EarlyStopping(monitor='val_loss',min_delta=0.0000001 , patience=2, verbose=1)]
    model = Sequential()
    model.add(SimpleRNN(1024, return_sequences=False, input_shape=(x_ref.shape[1],x_ref.shape[2])))
    model.add(Dense(128,activation='sigmoid'))
    model.add(Dense(128,activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam',metrics=['accuracy'])
    model.summary()
    history = model.fit(x_ref,y_ref,validation_data=(x_comperison,y_comperison), epochs=1000)
    pyplot.plot(history.history['loss'])
    pyplot.plot(history.history['val_loss'])
    pyplot.title('model train vs validation loss')
    pyplot.ylabel('loss')
    pyplot.xlabel('epoch')
    pyplot.legend(['train', 'test'], loc='upper right')
    pyplot.show()
    pyplot.plot(history.history['accuracy'])
    pyplot.plot(history.history['val_accuracy'])
    pyplot.title('model train vs validation accuracy')
    pyplot.ylabel('accuracy')
    pyplot.xlabel('epoch')
    pyplot.legend(['train', 'test'], loc='upper right')
    pyplot.show()
    y_pred = model.predict(x_predict)
    y_pred[y_pred <= 0.5] = 0
    y_pred[y_pred > 0.5] = 1
    y_pred = y_pred.astype(int)
    print("Done training")

    if(WriteFile):
        header = "time in seconds"
        for value in range(128):
            header += "," + str(value)
        header += "\n"
        timeslices = timeslices.to_numpy()
        y_pred = y_pred.astype(object)
        print(timeslices.shape)
        y_pred = np.insert(y_pred,0,timeslices,axis=1)
        with open(os.path.join("Data","Csv",'Predictions',"prediction.csv"), "w", newline='') as result_csv:
            result_csv.write(header)
            wr = csv.writer(result_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(y_pred)
            result_csv.close()