import csv

with open("doc/spec_2.csv","r") as f1:
    reader1 = list(csv.reader(f1))
with open("doc/YIN_result_2.csv","r") as f2:
    reader2 = list(csv.reader(f2))

with open("doc/input2.csv","w") as fw:
    writer = csv.writer(fw,lineterminator="\n")
    for n in range(len(reader2)):
        reader1[n].append(reader2[n][1])
        writer.writerow(reader1[n])