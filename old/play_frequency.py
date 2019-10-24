from synthesizer import Player, Synthesizer, Waveform
import csv

with open("result_full.csv","r",encoding="UTF-8") as f:
    data = [r for r in csv.reader(f)]


player = Player()
player.open_stream()
synth = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)

cut = [[d[0],round(float(d[1]),1)] for d in data[125:]]

l_note = cut[0][1]
i = 0
res = []
for c in cut:
    if l_note == c[1]:
        i += 1
    else:
        res.append([l_note,i])
        i = 1
        l_note = c[1]

time = float(data[1][0])

for r in res:
    player.play_wave(synth.generate_constant_wave(r[0], time*r[1]))

