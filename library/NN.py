import numpy as np
import os
import csv
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,classification_report
from sklearn.utils.validation import column_or_1d
import time as t

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
    print("Training")
    start = t.time()
    timeslices = x_predict["time in seconds"]
    y_ref = y_ref.drop(["time in seconds"],1)
    x_predict = x_predict.drop(["time in seconds"],1)
    x_ref = x_ref.drop(["time in seconds"],1)
    x_comperison = x_comperison.drop(["time in seconds"],1)
    y_comperison = y_comperison.drop(["time in seconds"],1)
    model = mlp(hidden_layer_sizes=(int(hiddenlayers[0]),int(hiddenlayers[1])),verbose=True,max_iter=5000)
    model.fit(x_ref,y_ref)
    elapsed = t.time() - start
    print("Done training: " + "{0:.2f}".format(elapsed) + "s")
    y_pred = model.predict(x_predict)
    print("Training set score: %f" % model.score(x_ref, y_ref))
    #print("Cassification score: %f" % classification_report(y_ref,y_pred))
    print("Test set score: %f" % model.score(x_comperison, y_comperison))

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
        