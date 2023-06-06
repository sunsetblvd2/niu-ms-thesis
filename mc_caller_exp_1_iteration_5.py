import sys
import os
import numpy as np
import pdb

power=np.arange(0,1040,40)
power[0]=1

queue_file=sys.argv[1]

## monte carlo trials
## emitter intensity
## x_t, emitter x-coordinate
## y_t, emitter y-coordinate
## n, attenuation
## domain size
## network size
## samples per period
## noise power
## algo.
## visual

for sigma in power:

    os.system('python mc_driver.py '+queue_file+'_mle 100 200 0 0 2 60 6 1 '+str(sigma)+' mle 0')
    os.system('python mc_driver.py '+queue_file+'_snap 100 200 0 0 2 60 6 1 '+str(sigma)+' snap 0')

