import csv
import numpy as np
from func import filters
from sklearn.metrics import f1_score


def note(l):
    return 440*pow(2,(int(l)-69)/12)

def n_eq(a,b):
    n1,n2 = round(a), round(b)
    s1 = [n1,n1+1,n1-1,n1+2,n1-2] 
    s2 = [n2,n2+1,n2-1],n2+2,n2-2
    for s in s1:
        if s in s2:
            return 1
    return 0
with open("manual_mid.csv","r") as f:
    reader = list(csv.reader(f))[4:-3]
result = []
while reader:
    start = reader.pop(0)
    for i,r in enumerate(reader):
        if r[4] == start[4]:
            result.append([float(start[1])/1200,float(r[1])/1200,int(start[4]),int(start[5])])
            reader.pop(i)
            break
result.append([0,0,0,0])
Filter = True
with open("doc/YIN_result.csv","r") as f:   
    output = list(csv.reader(f))
    if Filter:
        filtered = filters.medfilt( [float(i[1]) for i in output], 9 )
        output = [[output[i][0],filtered[i]] for i in range(len(output))]
    n = 0
    ans = 0
    i = 0
    for o in output:
        i+=1
        if result[n][1] == 0:
            break
        if float(o[0]) > result[n][1]:
            n += 1
        if result[n][0] <= float(o[0]) <= result[n][1]:
            ans += n_eq( note(result[n][2]), float(o[1]) )
                 
print(ans/i)

#     n = 0
#     res = []
#     for o in output:
#         if float(o[0]) < result[n][0]:
#             res.append(0)
#         if float(o[0]) > result[n][1]:
#             n += 1
#         if result[n][0] <= float(o[0]) <= result[n][1]:
#             res.append(note(result[n][2]))
# o = [float(o[1]) for o in  output]
# o = o[:len(res)]
# # o = np.ndarray(o)
# # res = np.ndarray(res)

# print(f1_score(res, o))
