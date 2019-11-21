import csv

def note(l):
    return 440*pow(2,(int(l)-69)/12)



with open("doc/manual_mid.csv","r") as f:
    reader = list(csv.reader(f))[4:-3]
result = []
while reader:
    start = reader.pop(0)
    for i,r in enumerate(reader):
        if r[4] == start[4]:
            result.append([float(start[1])/1200,float(r[1])/1200,int(start[4]),int(start[5])])
            reader.pop(i)
            break

with open("doc/res2/output.csv","r") as f:   
    output = list(csv.reader(f))
    n = 0
    ans = 0
    for o in output:
        if result[n][0] <= float(o[0]) <= result[n][1]:
            if note(result[n][2]) == float(o[1]):
                ans += 1
        if float(o[0]) > result[n][1]:
            n += 1
print(ans/len(output))