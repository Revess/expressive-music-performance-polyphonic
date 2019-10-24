#edit MIDI file (per sampling time(256/44100))
#before:num, time(tick),text,num, note, loudness
#after :note, power

import csv

with open("manual_mid.csv","r") as f1:
    reader = list(csv.reader(f1))[4:-3]
    result = []
    while reader:
        start = reader.pop(0)
        for i,r in enumerate(reader):
            if r[4] == start[4]:
                result.append([float(start[1])/1200,float(r[1])/1200,int(start[4]),int(start[5])])
                reader.pop(i)
                break
    with open("manual_mid_edit.csv","w") as f2:
        writer = csv.writer(f2,lineterminator="\n")
        n = 256/44100
        for r in result:
            while n < r[0]:
                writer.writerow([0,0])
                n = n + 256/44100
            while n < r[1]:
                writer.writerow([r[2],r[3]])
                n = n + 256/44100
