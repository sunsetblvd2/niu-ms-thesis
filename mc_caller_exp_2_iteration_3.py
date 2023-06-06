import sys
import os
import numpy as np
import pdb

att=np.arange(2,5.1,0.12)

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

for val in att:

    os.system('python mc_driver.py '+queue_file+'_mle 100 200 0 0 '+str(val)+' 60 6 1 1 mle 0')
    os.system('python mc_driver.py '+queue_file+'_snap 100 200 0 0 '+str(val)+' 60 6 1 1 snap 0')
