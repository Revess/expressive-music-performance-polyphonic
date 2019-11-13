import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score
import numpy as np
import csv
import time
from shape_input import shape_input

t1 = time.time()

data, target, sampling_rate = shape_input("doc/spec.csv","doc/manual_mid_edit.csv",True)

clf = MLPClassifier(
    hidden_layer_sizes = (3000,2000,1000,29),
    max_iter = 300,
    early_stopping = True,
    momentum = 0.005,
    alpha = 5,
    )

clf.fit(data,target)
predict = clf.predict(data)
df = pd.DataFrame(classification_report(target, predict,output_dict=True))
df.to_csv("doc/result_NN_.csv")

with open("doc/output.csv","w") as f:
    i = 0
    writer = csv.writer(f,lineterminator="\n")
    for l in predict:
        writer.writerow([i,440*pow(2,(int(l)-69)/12)])
        i = i + sampling_rate

t2 = time.time()
with open("doc/result.txt","w",encoding = "UTF-8") as f:
    f.write(str(cross_val_score(clf, data, target, cv=10)))
    f.write(str(t2-t1))