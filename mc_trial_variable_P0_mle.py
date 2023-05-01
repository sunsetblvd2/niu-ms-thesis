import os
import numpy as np
import pdb


intensity=np.arange(100,1100,100)

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

    os.system('python loc_target.py 100 '+str(P_0)+' 0 0 2 60 6 1 mle 0')

