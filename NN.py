import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report,accuracy_score
from sklearn.utils.validation import column_or_1d
import numpy as np


col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")

data = pd.read_csv("input1.csv", names = col)
target = pd.read_csv("manual_mid_edit.csv", names = ["Pitch_manual","power"])
target = target.drop(["power"], axis=1)
target = target[:len(data)]
target = np.ravel(target)

clf = MLPClassifier()

# 試行するパラメータを羅列する
params = {
    "max_iter":[300],
    "early_stopping":[True],
    "momentum": [0.005],
    "alpha":[5],
    "hidden_layer_sizes":[(215,188,170,158),(215,188,170,158,150),(215,188,170,158,150,145)],
    # "baich_size":[],
}
grid_search = GridSearchCV(clf, param_grid=params, cv=5, n_jobs=-1,)
grid_search.fit(data, target)

with open("result_param.txt","a",encoding="UTF-8") as f:
    f.write(grid_search.best_score_)
    f.write(grid_search.best_params_)
print(grid_search.best_score_)  # 最も良かったスコア
print(grid_search.best_params_)  # 上記を記録したパラメータの組み合わせ