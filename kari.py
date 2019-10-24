import csv

with open("manual_mid_time.csv","r") as f1:
    with open("manual_mid_time_c.csv","w") as f2:
        writer = csv.writer(f2,lineterminator="\n")
        n = 256/44100
        for r in csv.reader(f1):
            while n < float(r[0]):
                writer.writerow([0,0])
                n = n + 256/44100
            while n < float(r[1]):
                writer.writerow([int(r[2]),int(r[3])])
                n = n + 256/44100
