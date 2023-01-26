import numpy as np

import grid

class MaxLikelihood:
    
    ## For a 2-D square grid centered about the origin
    ##  ax_l     : length of either axis of the 2-D grid (m)
    ##  ax_t     : length between axis ticks (m)
    def __init__(self,ax_len,ax_tks=0.1):

        print('\n>> Building LE grid...')
        self.grid=grid.Grid(ax_len,ax_t=ax_tks) 

        self.ax_x,self.ax_y=self.grid.fetch_axes()

        self.le_matrix=np.zeros((self.ax_x.shape[0], \
                                 self.ax_y.shape[0]))

    #def liklihood_estimate_grid(self,I,nu,a):

    ## return the le grid
    def grid(self):
        return self.grid.fetch_grid()
        
