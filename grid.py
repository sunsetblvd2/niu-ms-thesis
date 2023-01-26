import numpy as np
import pdb

class Grid:
    
    ## For a 2-D square grid centered about the origin
    ##  ax_l     : length of either axis of the 2-D grid (m)
    ##  org      : axes origin
    ##  ax_t   : length between axis ticks (m)
    def __init__(self,ax_l,org=(0,0),ax_t=1,ticks='range'):

        print('Dimensions: '+str(ax_l)+'x'+str(ax_l)+' m')
        print('Origin: '+str(org))
        print('Ticks: '+str(ax_t)+' m')
        print('Grid type: '+str(ticks))
        
        if ticks=='range':

            self.grid_ax_l=ax_l
            self.grid_org=org
            self.grid_ax_t=ax_t

            self.grid_ax_x=np.arange(self.grid_org[0]-(self.grid_ax_l/2), \
                                     self.grid_org[0]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)
            self.grid_ax_y=np.arange(self.grid_org[1]-(self.grid_ax_l/2), \
                                     self.grid_org[1]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)

        elif ticks=='linspace':

            self.grid_ax_l=ax_l
            self.grid_org=org
            self.grid_ax_t=ax_t

            self.grid_ax_x=np.arange(self.grid_org[0]-(self.grid_ax_l/2), \
                                     self.grid_org[0]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)
            self.grid_ax_y=np.arange(self.grid_org[1]-(self.grid_ax_l/2), \
                                     self.grid_org[1]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)

    ## return axes
    def axes(self):
        return self.grid_ax_x,self.grid_ax_y

    ## return dimensions
    def dimensions(self):
        return (self.grid_ax_x.shape[0],self.grid_ax_y.shape[0])
    
    ## return a mesh grid
    def meshgrid(self):
        XG,YG=np.meshgrid(self.grid_ax_x,self.grid_ax_y)
        return XG,YG
    
    ## return coordinates of each grid point as a list
    def coordinates(self):
        coordinates_list=[]
        for xc in self.grid_ax_x:
            for yc in self.grid_ax_y:
                coordinates_list.append((xc,yc))
        return coordinates_list
