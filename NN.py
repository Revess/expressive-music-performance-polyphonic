import numpy as np
import os
import csv
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,classification_report
from sklearn.utils.validation import column_or_1d
import time as t

# import plot_learning_curve
# from sklearn.naive_bayes import GaussianNB
# from sklearn.model_selection import ShuffleSplit

print("Reading data")
start = t.time()
x = pd.read_csv(os.path.join('Data','Csv','spectrum.csv'))
test_vals = pd.read_csv(os.path.join('Data','Csv','spectrum2.csv'))
y = pd.read_csv(os.path.join('Data','Csv','labels.csv'))
elapsed = t.time() - start
print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")

print("Training")
start = t.time()
timeslices = test_vals["time in seconds"]
y = y.drop(["time in seconds"],1)
test_vals = test_vals.drop(["time in seconds"],1)
x = x.drop(["time in seconds"],1)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size= 0.25, random_state=27)
model = mlp(hidden_layer_sizes=(100,100),verbose=True,max_iter=5000)
model.fit(x_train,y_train)
elapsed = t.time() - start
print("Done training: " + "{0:.2f}".format(elapsed) + "s")
y_pred = model.predict(test_vals)
print("Training set score: %f" % model.score(x_train, y_train))
print("Test set score: %f" % model.score(x_test, y_test))

# plot_learning_curve.plot_learning_curve(GaussianNB,"Curve",x_train,y,ylim=(0.7, 1.01), cv=ShuffleSplit(n_splits=100, test_size=0.2, random_state=0), n_jobs=4)

txt = True
if(txt):
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
        