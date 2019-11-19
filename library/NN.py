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
    x = pd.read_csv(os.path.join('.','Data','Csv','spectrum.csv'))
    test_vals = pd.read_csv(os.path.join('.','Data','Csv','spectrum2.csv'))
    y = pd.read_csv(os.path.join('.','Data','Csv','labels.csv'))
    # x_test = pd.read_csv(os.path.join('.','Data','Csv','spectrum3.csv'))
    # y_test = pd.read_csv(os.path.join('.','Data','Csv','labels2.csv'))
    elapsed = t.time() - start
    print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")
    print("Training")
    start = t.time()
    timeslices = test_vals["time in seconds"]
    y = y.drop(["time in seconds"],1)
    test_vals = test_vals.drop(["time in seconds"],1)
    x = x.drop(["time in seconds"],1)
    # x_test = x_test.drop(["time in seconds"],1)
    # y_test = y_test.drop(["time in seconds"],1)
    model = mlp(hidden_layer_sizes=(int(hiddenlayers[0]),int(hiddenlayers[1])),verbose=True,max_iter=5000)
    model.fit(x,y)
    elapsed = t.time() - start
    print("Done training: " + "{0:.2f}".format(elapsed) + "s")
    y_pred = model.predict(test_vals)
    print("Training set score: %f" % model.score(x, y))
    print("Test set score: %f" % model.score(test_vals, y_pred))

    if(WriteFile):
        header = "time in seconds"
        for value in range(128):
            header += "," + str(value)
        header += "\n"
        timeslices = timeslices.to_numpy()
        y_pred = y_pred.astype(object)
        y_pred = np.insert(y_pred,0,timeslices,axis=1)
        with open(os.path.join("Data","Output","research.csv"), "w", newline='') as result_csv:
            result_csv.write(header)
            wr = csv.writer(result_csv, quoting=csv.QUOTE_NONE)
            wr.writerows(y_pred)
            result_csv.close()
        