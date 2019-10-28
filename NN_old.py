import csv
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier

col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")

X = pd.read_csv("input1.csv", names = col)
Y = pd.read_csv("input2.csv", names = ["Pitch_manual"])

clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(128,30), random_state=1)
clf.fit(X, Y.values.ravel()) 