import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import sensorarray as sa
import emitter
import grid
import wsnManager
import pdb


def loc_target_monte_carlo(montecarlo_N,domain_size,network_size,sample_T,localize,emitter_vis):

    logging.info('>> Beginning Monte Carlo simulation.')
    logging.info('>> Settings: ')
    logging.info('*** Number of iterations        : '+str(montecarlo_N))
    logging.info('*** Size of domain              : '+str(domain_size))
    logging.info('*** Size of network             : '+str(network_size))
    logging.info('*** Number of samples per period: '+str(sample_T))
    logging.info('*** Localization method         : '+str(localize))
    logging.info('*** Emitter visual setting      : '+str(emitter_vis))

    for n in range(0,montecarlo_N):
        
        logging.info('>> Iteration: '+str(n))

        theta=[25000,0,0]
        n=2
        
        Wsn=wsnManager.WsnManager(domain_size,network_size,sample_T,localize)
        Emitter=emitter.Isotropic(theta,n)

        if emitter_vis:
            Emitter.heatmap(Wsn.domain_size)

        Wsn.network.sample(Emitter)

        pdb.set_trace()

        s_arr=sa.SensorArray(s_n,s_d)
        s_arr.sample(T)
        s_arr.transmit()
        s_arr.fuse()
        
        estimate=s_arr.estimate ## get estimate as array size (2,)

        logging.info('%_ESTIMATE:: '+str(estimate)) ## logging all estimates

    ## monte carlo finished
    logging.info('>> END OF MC')

    return 0

if __name__ == '__main__':

    cwd=os.getcwd()

    logfilename=cwd+'\\logs\\log_loc_target'+datetime.datetime.now().strftime('%y%b%d%H%M%S')+'.txt'
    logging.basicConfig(filename=logfilename,level=logging.INFO,format='%(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    """
        Arguments:  montecarlo_N : int

                        Number of iterations in Monte Carlo run.

                    domain_size : int

                        Size of domain.

                    network_size  : int

                        The number of sensors per row in a square array.

                    sample_T     : int

                        Number of samples per sample period.

                    localize     : str, {'mle','snap'}

                        Localization method.

                    emitter_vis  : bool

                        Visualize the emitter in the domain with a heatmap. True to plot.

    """

    assert(len(sys.argv)==7), 'Incorrect list of arguments.'

    montecarlo_N=int(sys.argv[1])
    domain_size=int(sys.argv[2])
    network_size=int(sys.argv[3])
    sample_T=int(sys.argv[4])
    localize=str(sys.argv[5])
    emitter_vis=bool(sys.argv[6])
    
    loc_target_monte_carlo(montecarlo_N,domain_size,network_size,sample_T,localize,emitter_vis)
