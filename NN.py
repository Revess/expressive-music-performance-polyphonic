import numpy as np
import os
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,classification_report
from sklearn.utils.validation import column_or_1d
import time as t

print("Reading data")
start = t.time()
x = pd.read_csv(os.path.join('Data','Csv','spectrum.csv'))
y = pd.read_csv(os.path.join('Data','Csv','labels.csv'))
elapsed = t.time() - start
print("Done reading data: " + "{0:.2f}".format(elapsed) + "s")

print("Training")
start = t.time()
y = y.drop(["time in seconds"],1)
x = x.drop(["time in seconds"],1)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size= 0.25, random_state=27)
model = mlp(hidden_layer_sizes=(100,100,100),solver='sgd',verbose=True,power_t=0.99)
model.fit(x_train,y_train)
elapsed = t.time() - start
print("Done training: " + "{0:.2f}".format(elapsed) + "s")
y_pred = model.predict(x_test)



with open(os.path.join("Data","Output","Research.txt"), "w", newline='') as result_txt:
            result_txt.write(str(y_pred) + "\n")
            result_txt.write(str(accuracy_score(y_test, y_pred)))
            result_txt.close()
        