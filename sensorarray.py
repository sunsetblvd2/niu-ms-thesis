import numpy as np
import matplotlib.pyplot as plt
import logging
import grid
import sensor
import fusioncenter

class SensorArray:
    
    ## For a 2-D square sensor array centered about origin (0,0)
    ##  s_n : number of sensors in a single row
    ##  s_d : spacing between sensors in a single row
    def __init__(self,s_n,s_d):

        logging.info('*** Initializing sensors ***')

        self.sa_grid=grid.Grid(s_n*s_d-s_d,ax_t=s_d)##subtract to offset center

        self.sa=[]
        for i,p in enumerate(self.sa_grid.coordinates()):
            logging.info('>> Sensor '+str(i)+' coordinates: '+str((p[0],p[1])))
            self.sa.append(sensor.Sensor(p[0],p[1]))
        
        logging.info('%_EMITTER:: '+str(self.sa[0].theta_t))

        self.p_node=fusioncenter.FusionCenter(s_n*s_d)

    def sample(self,T):

        logging.info('*** Beginning sampling process ***')

        for t in range(0,T):
            #logging.info('>> t='+str(t))
            for i,sensor in enumerate(self.sa):
                #logging.info('>> Sensor '+str(i)+' sampling')
                sensor.sample()

    def transmit(self):
        self.p_node.receive(self.sa)

    def fuse(self):
        self.estimate=self.p_node.max_likelihood_estimate()
