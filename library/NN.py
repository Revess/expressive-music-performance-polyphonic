import numpy as np
import os
import csv
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,classification_report,f1_score
import time as t

def NN(hiddenlayers=[100,100,100,100]):
    print("Reading data")
    start = t.time()
    x_ref = pd.read_csv(os.path.join('.','Data','Csv','Spectrum','S01-AT.csv'))
    y_ref = pd.read_csv(os.path.join('.','Data','Csv','Labels','S01-AT.csv'))
    SPECTRUM_PATH = os.path.join('.','Data','Csv','Spectrum')
    PREDICTIONS_PATH = os.path.join('.','Data','Csv','Predictions')
    SPECTRUM_DIR = os.listdir(SPECTRUM_PATH)
    elapsed = t.time() - start
    print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")
    print("Training")
    start = t.time()
    y_ref = y_ref.drop(["time in seconds"],1)
    x_ref = x_ref.drop(["time in seconds"],1)
    model = mlp(hidden_layer_sizes=(int(hiddenlayers[0]),int(hiddenlayers[1])),verbose=True,max_iter=5000)
    model.fit(x_ref,y_ref)
    elapsed = t.time() - start
    print("Done training: " + "{0:.2f}".format(elapsed) + "s")
    ("Predicting Files")
    for fileName in SPECTRUM_DIR:
        if fileName[-3:] == 'csv':
            print("Predicting file: " + str(fileName)) 
            PREDICTIONS_FILE_PATH = os.path.join(PREDICTIONS_PATH, fileName)
            SPECTRUM_FILE_PATH = os.path.join(SPECTRUM_PATH, fileName)
            x_predict = pd.read_csv(SPECTRUM_FILE_PATH)
            timeslices = x_predict["time in seconds"]
            x_predict = x_predict.drop(["time in seconds"],1)
            y_pred = model.predict(x_predict)
            print("Training set score: %f" % model.score(x_ref, y_ref))
            header = "time in seconds"
            for value in range(128):
                header += "," + str(value)
            header += "\n"
            timeslices = timeslices.to_numpy()
            y_pred = y_pred.astype(object)
            y_pred = np.insert(y_pred,0,timeslices,axis=1)
            with open(PREDICTIONS_FILE_PATH, "w", newline='') as result_csv:
                result_csv.write(header)
                wr = csv.writer(result_csv, quoting=csv.QUOTE_NONE)
                wr.writerows(y_pred)
                result_csv.close()
            print("\n")
        