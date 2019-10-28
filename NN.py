import csv
import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def to_train_test(dataframe, percent = 0.3): #dataの30%をtest_dataに、70%をtrain_dataに変化している
    #percentに入れた小数点以下の数字分、test_dataを入れる。
    data_len = int(len(dataframe)*percent)
    #学習用データと測定用データ
    train_data = dataframe[:-data_len].dropna()
    test_data = dataframe[-data_len:].dropna()
    return train_data,test_data


col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")
X = pd.read_csv("input1.csv", names = col)
Y = pd.read_csv("input2.csv", names = ["Pitch_manual"])

X_train, X_test = to_train_test(X)
Y_train, Y_test = to_train_test(Y)

model = MLPClassifier(activation="tanh", hidden_layer_sizes=200, batch_size=1000, learning_rate="adaptive",)

model.fit(X_train,Y_train)

pre = model.predict(X_test)
print(accuracy_score(Y_test, pre, normalize=True, sample_weight=None))