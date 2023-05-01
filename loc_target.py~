import sys
import logging
import numpy as np
import matplotlib.pyplot as plt
import os
import datetime
import emitter
import wsnManager
import pdb


def loc_target_monte_carlo(montecarlo_N,emitter_set,domain_size,network_size,sample_T,localize,emitter_vis):

    logging.info('>> Beginning Monte Carlo simulation.')
    logging.info('>> Settings: ')
    logging.info('*** Number of iterations        : '+str(montecarlo_N))
    logging.info('*** Emitter_set                 : '+str(emitter_set))
    logging.info('*** Size of domain              : '+str(domain_size))
    logging.info('*** Size of network             : '+str(network_size))
    logging.info('*** Number of samples per period: '+str(sample_T))
    logging.info('*** Localization method         : '+str(localize))
    logging.info('*** Emitter visual setting      : '+str(emitter_vis))

    for n in range(0,montecarlo_N):
        
        logging.info('>> Iteration: '+str(n))

        theta=emitter_set[:len(emitter_set)-1]
        n=emitter_set[len(emitter_set)-1]

        Wsn=wsnManager.WsnManager(domain_size,network_size,sample_T,localize)
        Emitter=emitter.Isotropic(theta,n)

        if emitter_vis:
            Wsn.network.plot(Emitter)

        estimate=Wsn.network.sample(Emitter)

        logging.info('%_ESTIMATE:: '+str(estimate)) ## logging all estimates

    return 0

if __name__ == '__main__':

    cwd=os.getcwd()

    logfilename=cwd+'\\logs\\log_loc_target'+datetime.datetime.now().strftime('%y%b%d%H%M%S')+'.txt'
    logging.basicConfig(filename=logfilename,level=logging.INFO,format='%(message)s')
    logging.getLogger().addHandler(logging.StreamHandler())

    """
        Arguments:  montecarlo_N : int

                        Number of iterations in Monte Carlo run.

                    P_0 : int 

                        Source intensity

                    x_t : float

                        Source x-coordinate

                    y_t : float

                        Source y-coordinate

                    n : int

                        Emitter attenuation constant

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

    assert(len(sys.argv)==11), 'Incorrect list of arguments.'

    montecarlo_N=int(sys.argv[1])
    emitter_set=[int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5])]
    domain_size=int(sys.argv[6])
    network_size=int(sys.argv[7])
    sample_T=int(sys.argv[8])
    localize=str(sys.argv[9])
    emitter_vis=bool(int(sys.argv[10]))
    
    loc_target_monte_carlo(montecarlo_N,emitter_set,domain_size,network_size,sample_T,localize,emitter_vis)
