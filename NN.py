import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report,accuracy_score
from sklearn.utils.validation import column_or_1d
import numpy as np


col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")

data = pd.read_csv("doc/input2.csv", names = col)
target = pd.read_csv("doc/manual_mid_edit_2.csv", names = ["Pitch_manual","power"]).drop(["power"], axis=1)[:len(data)]
df = pd.concat([data, target], axis=1)
df = df[df['Pitch_manual'] != 0]

target = df["Pitch_manual"]
data = df.drop(["Pitch_manual"], axis=1)

# 試行するパラメータを羅列する
params = {
    "max_iter":[300],
    "early_stopping":[True],
    "momentum": [0.005],
    "alpha":[5],
    "hidden_layer_sizes":[(215,188,170,158,150,145)],
    # "baich_size":[],
}
grid_search = GridSearchCV(MLPClassifier(), param_grid=params, cv=5, n_jobs=-1,)
grid_search.fit(data, target)

with open("doc/result_param.txt","a",encoding="UTF-8") as f:
    f.write(str(grid_search.best_score_))
    f.write(str(grid_search.best_params_))
print(grid_search.best_score_)  # 最も良かったスコア
print(grid_search.best_params_)  # 上記を記録したパラメータの組み合わせ