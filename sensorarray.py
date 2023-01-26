import numpy as np
import matplotlib.pyplot as plt

import grid
import sensor
import fusioncenter
import maxlikelihood

import pdb

class SensorArray:
    
    ## For a 2-D square sensor array centered about origin (0,0)
    ##  s_n : number of sensors in a single row
    ##  s_d : spacing between sensors in a single row
    def __init__(self,s_n,s_d):

        print('\n>> Initializing sensor array...')
        print('Array row length: '+str(s_n))
        print('Spacing in row: '+str(s_d))

        self.sa_grid=grid.Grid(s_n*s_d-s_d,ax_t=s_d,ticks='linspace')##subtract to offset center

        self.sa=[]
        for p in self.sa_grid.coordinates():
            self.sa.append(sensor.Sensor(p[0],p[1]))
        print('Finished.')
        
        print('\n>> Initializing fusion center...')
        self.p_node=fusioncenter.FusionCenter(s_n*s_d)
        print('Finished.')

    def sample(self,T):
        print('\n>> Starting sample process...')
        print('T = '+str(T))
        for t in range(0,T):
            if t % 25 == 0:
                print('t = '+str(t))
            for i,sensor in enumerate(self.sa):
                sensor.sample()
        print('Finished.')

    def transmit(self):
        self.p_node.receive(self.sa)

    def fuse(self):
        self.p_node.max_likelihood_estimate()
