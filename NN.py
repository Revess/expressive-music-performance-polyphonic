import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report,accuracy_score


col = ["sp"+str(n) for n in range(256)]
col.append("Pitch_YIN")

data = pd.read_csv("input1.csv", names = col)
# target = pd.read_csv("input2.csv", names = ["Pitch_manual"])
target = pd.read_csv("manual_mid_edit.csv", names = ["Pitch_manual","power"])
target = target.drop(["power"], axis=1)
target = target[:len(data)]


data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.2, random_state=0)
model = MLPClassifier(activation="tanh", hidden_layer_sizes=(200,128), batch_size=1000, learning_rate="adaptive",)
model.fit(data_train,target_train)

pre = model.predict(data_test)
print(classification_report(target_test, pre))