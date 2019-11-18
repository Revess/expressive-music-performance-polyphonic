import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import classification_report,accuracy_score
from sklearn.utils.validation import column_or_1d
import numpy as np
from shape_input import shape_input

data, target, sampling_rate = shape_input("doc/spec.csv","doc/manual_mid_edit.csv")

# 試行するパラメータを羅列する
params = {
    "max_iter":[300],
    "early_stopping":[True],
    "momentum": [0.005],
    "alpha":[5],
    "hidden_layer_sizes":[(225,193,161,129,97,66)],
    # "batch_size":[100,200,500,1000],
}
grid_search = GridSearchCV(MLPClassifier(), param_grid=params, cv=3, n_jobs=-1,)
grid_search.fit(data, target)

gs_result = pd.DataFrame.from_dict(grid_search.cv_results_)
gs_result.to_csv('doc/gs_result.csv')

print(grid_search.best_score_)  # 最も良かったスコア
print(grid_search.best_params_)  # 上記を記録したパラメータの組み合わせ