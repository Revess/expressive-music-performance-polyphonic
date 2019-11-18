#edit MIDI file (per sampling time)
#before:num, time(tick),text,num, note, loudness
#after :note, power


import csv

def midi_edit(input_f,output_f,timeflame):
    with open(input_f,"r") as f1:
        reader = list(csv.reader(f1))[4:-3]
    result = []
    while reader:
        start = reader.pop(0)
        for i,r in enumerate(reader):
            if r[4] == start[4]:
                result.append([float(start[1])/1200,float(r[1])/1200,int(start[4]),int(start[5])])
                reader.pop(i)
                break
    with open(output_f,"w") as f2:
        writer = csv.writer(f2,lineterminator="\n")
        writer.writerow(["time","midi_note","power"])
        n = 0
        for r in result:
            while n*timeflame < r[0]:
                writer.writerow([n*timeflame,0,0])
                n += 1 
            while n*timeflame <= r[1]:
                writer.writerow([n*timeflame,r[2],r[3]])
                n += 1
    print("MIDI time slices : " +str(n))