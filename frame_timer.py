import numpy as np
import time as t

#Find timestamps of the spectral data and calulate them in seconds
def frame_timer(num_samps,spectrum_width,sr=22050):
    print("Finding timestamps...", end="")
    s = t.time()
    times = np.array(0)
    sound_length = (1/sr)*num_samps
    offset = sound_length / spectrum_width
    times = [0]
    for i in range(spectrum_width-1):
        times.append(times[i] + offset)
    times = np.array(times)
    elapsed = t.time() - s
    print("Done in: " + "{0:.2f}".format(elapsed) + "s")
    return times