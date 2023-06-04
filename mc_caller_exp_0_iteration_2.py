import os
import numpy as np
import pdb


intensity=np.array([1000,2000,3000,4000,5000,6000,7000,8000,9000,10000])

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

