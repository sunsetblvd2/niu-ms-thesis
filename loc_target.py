import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import sensorarray as sa


def loc_target_monte_carlo(N,s_n,s_d,T):

    logging.info('>> BEGINNING MC')

    for n in range(0,N):
    
        logging.info('>> MC'+str(n))

        s_arr=sa.SensorArray(s_n,s_d)
        s_arr.sample(T)
        s_arr.transmit()
        s_arr.fuse()
        
        estimate=s_arr.estimate ## get estimate as array size (2,)

        logging.info('%_ESTIMATE:: '+str(estimate)) ## logging all estimates

    ## monte carlo finished
    logging.info('>> END OF MC')

    ## fetch the CRLB where is CRLB call?

    return 0

if __name__ == '__main__':

    cwd=os.getcwd()

    logfilename=cwd+'\\logs\\log_loc_target'+datetime.datetime.now().strftime('%y%b%d%H%M%S')+'.txt'
    logging.basicConfig(filename=logfilename,level=logging.INFO,format='%(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    assert(len(sys.argv)==5), 'Incorrect list of arguments.'

    N=int(sys.argv[1])
    s_n=int(sys.argv[2]) ## number of sensors in a row
    s_d=int(sys.argv[3]) ## spacing of sensors in a row
    T=int(sys.argv[4]) ## number of samples T

    logging.info('*** Start ***')
    logging.info('*** SYS ARGS ***')
    logging.info('>> Monte carlo runs       N : '+str(N))
    logging.info('>> Sensor row length    s_n : '+str(s_n))
    logging.info('>> Sensor row spacing   s_d : '+str(s_d)+' m')
    logging.info('>> Sampling period        T : '+str(T)+' s')

    loc_target_monte_carlo(N,s_n,s_d,T)
