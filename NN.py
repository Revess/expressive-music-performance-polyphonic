import csv
import pandas as pd
from sklearn.linear_model import LinearRegression

with open("input.csv","r") as f:
    data = list(csv.reader(f))

col = ["sp"+str(n) for n in range(len(data[0])-2)]
col.append("Pitch_YIN")
col.append("Pitch_manual")

df = pd.DataFrame(data, [n for n in range(len(data))] , col)


linear_regression = LinearRegression()

X = df.drop("Pitch_manual", 1)
Y = df.Pitch_manual

linear_regression.fit(X,Y)