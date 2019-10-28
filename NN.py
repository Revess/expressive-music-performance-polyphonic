import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report,accuracy_score
from sklearn.utils.validation import column_or_1d
import numpy as np


col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")

data = pd.read_csv("input1.csv", names = col)
# target = pd.read_csv("input2.csv", names = ["Pitch_manual"])
target = pd.read_csv("manual_mid_edit.csv", names = ["Pitch_manual","power"])
target = target.drop(["power"], axis=1)
target = target[:len(data)]
target = np.ravel(target)

data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2, random_state=0)
clf = MLPClassifier()

# 試行するパラメータを羅列する
params = {
    "momentum": [(n+1)*0.1 for n in range(10)],
    "alpha":[0],
    # "hidden_layer_sizes":[],
    # "baich_size":[],
}
grid_search = GridSearchCV(clf, param_grid=params, cv=5, n_jobs=-1,)
grid_search.fit(data, target)

print(grid_search.best_score_)  # 最も良かったスコア
print(grid_search.best_params_)  # 上記を記録したパラメータの組み合わせ
