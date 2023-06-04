import os
import numpy as np
import pdb


intensity=np.array([1,50,100,150,200,250,300,350,400,450,500])

## monte carlo trials
## emitter intensity
## x_t, emitter x-coordinate
## y_t, emitter y-coordinate
## n, attenuation
## domain size
## network size
## samples per period
## algo.
## visual

for P_0 in intensity:

    os.system('python mc_driver.py 100 '+str(P_0)+' 0 0 2 60 6 1 mle 0')
    os.system('python mc_driver.py 100 '+str(P_0)+' 0 0 2 60 6 1 snap 0')

