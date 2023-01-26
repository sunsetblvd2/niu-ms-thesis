import numpy as np
from scipy import special as sp

import grid

import pdb

class FusionCenter:
    
    def __init__(self,grid_l,cell_l=0.1):

        self.le_grid=grid.Grid(grid_l,ax_t=cell_l)

    def receive(self,sa):

        self.sa=sa

    def qfunc(self,x):
        return 0.5-0.5*sp.erf(x/np.sqrt(2))

    def max_likelihood_estimate(self):

        self.p_x,self.p_y=self.le_grid.axes()

        le_grid_dim=self.le_grid.dimensions()
        self.le_matrix=np.zeros(le_grid_dim)

        for i,xg in enumerate(self.p_x):
            for j,yg in enumerate(self.p_y):
                theta=[25000,round(xg,2),round(yg,2)]

                sumll_s=0
                for sensor in self.sa:
                    sumll_t=0
                    for I in sensor.I_list:
                        sumll_t=sumll_t+(I*np.log(self.qfunc(sensor.nu-sensor.amplitude(theta))) \
                               +(1-I)*np.log(1-self.qfunc(sensor.nu-sensor.amplitude(theta))))
                    sumll_s=sumll_s+sumll_t
                
                self.le_matrix[i,j]=sumll_s
                print(str((theta[1],theta[2]))+': '+str(self.le_matrix[i,j]))
