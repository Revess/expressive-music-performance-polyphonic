import csv

with open("spec.csv","r") as f1:
    reader1 = list(csv.reader(f1))
with open("YIN_result.csv","r") as f2:
    reader2 = list(csv.reader(f2))
with open("manual_mid_edit.csv","r") as f3:
    reader3 = list(csv.reader(f3))

with open("input1.csv","w") as fw:
    writer = csv.writer(fw,lineterminator="\n")
    for n in range(len(reader2)):
        reader1[n].append(reader2[n][1])
        writer.writerow(reader1[n])

# midi_v = [[r] for r in reader3]

midi_v = []
for r in reader3:
    m_v = [0]*128
    m_v[int(r[0])] = 1
    midi_v.append(m_v)



with open("input2.csv","w") as fw:
    writer = csv.writer(fw,lineterminator="\n")
    for n in midi_v:
        writer.writerow(n) 