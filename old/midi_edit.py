#edit MIDI file
#before:num, time(tick),text,num, note, loudness
#after :start_time, end_time, note, loudness

import csv

with open("manual_mid.csv","r") as f1:
    reader = list(csv.reader(f1))[4:-3]
    with open("manual_mid_time.csv","w") as f2:
        writer = csv.writer(f2,lineterminator="\n")
        while reader:
            start = reader.pop(0)
            for i,r in enumerate(reader):
                if r[4] == start[4]:
                    writer.writerow([float(start[1])/1200,float(r[1])/1200,start[4],start[5]])
                    reader.pop(i)
                    break
        
