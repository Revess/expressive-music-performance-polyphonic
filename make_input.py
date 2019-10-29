import csv

with open("doc/spec_2.csv","r") as f1:
    reader1 = list(csv.reader(f1))
with open("doc/YIN_result_2.csv","r") as f2:
    reader2 = list(csv.reader(f2))
with open("doc/manual_mid_edit_2.csv","r") as f3:
    reader3 = list(csv.reader(f3))

with open("doc/input2.csv","w") as fw:
    writer = csv.writer(fw,lineterminator="\n")
    for n in range(len(reader2)):
        reader1[n].append(reader2[n][1])
        writer.writerow(reader1[n])
        
# midi_v = []
# for r in reader3:
#     m_v = [0]*128
#     m_v[int(r[0])] = 1
#     midi_v.append(m_v)

# with open("input2.csv","w") as fw:
#     writer = csv.writer(fw,lineterminator="\n")
#     for n in midi_v[:len(reader2)]:
#         writer.writerow(n) 