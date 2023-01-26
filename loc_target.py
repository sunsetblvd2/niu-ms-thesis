import sys
import numpy as np
import matplotlib.pyplot as plt

import sensorarray as sa

import pdb

print('\n>> Running target localization model...')

s_n=int(sys.argv[1]) ## number of sensors in a row
s_d=int(sys.argv[2]) ## spacing of sensors in a row
T=int(sys.argv[3]) ## number of samples T

s_arr=sa.SensorArray(s_n,s_d)
s_arr.sample(T)
s_arr.transmit()
s_arr.fuse()

pdb.set_trace()

