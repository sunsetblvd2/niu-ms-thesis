import numpy as np
import logging
import matplotlib.pyplot as plt

class Grid:
    
    ## For a 2-D square grid centered about the origin
    ##  ax_l     : length of either axis of the 2-D grid (m)
    ##  org      : axes origin
    ##  ax_t   : length between axis ticks (m)
    def __init__(self,ax_l,org=(0,0),ax_t=1,ticks='range', \
            x_lim_lower=0, x_lim_upper=0, y_lim_lower=0, y_lim_upper=0):
        
        logging.info('*** Initializing grid ***')
        
        if ticks=='range':

            logging.info('>> Grid x-domain: '+str(x_lim_lower)+':'+str(x_lim_upper))
            logging.info('>> Grid y-domain: '+str(y_lim_lower)+':'+str(y_lim_upper))
            logging.info('>> Grid origin: '+str(org)+' m')
            logging.info('>> Grid ticks: '+str(ax_t)+' m')
            logging.info('>> Grid type: '+str(ticks))

            self.grid_ax_l=ax_l
            self.grid_org=org
            self.grid_ax_t=ax_t

            self.grid_ax_x=np.arange(self.grid_org[0]-(self.grid_ax_l/2), \
                                     self.grid_org[0]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)
            self.grid_ax_y=np.arange(self.grid_org[1]-(self.grid_ax_l/2), \
                                     self.grid_org[1]+(self.grid_ax_l/2)+self.grid_ax_t,
                                     self.grid_ax_t)

        elif ticks=='custom':

            logging.info('>> Grid x-domain: '+str(x_lim_lower)+':'+str(x_lim_upper))
            logging.info('>> Grid y-domain: '+str(y_lim_lower)+':'+str(y_lim_upper))
            logging.info('>> Grid origin: '+str(org)+' m')
            logging.info('>> Grid ticks: '+str(ax_t)+' m')
            logging.info('>> Grid type: '+str(ticks))

            x_num=(x_lim_upper-x_lim_lower)/ax_t
            self.grid_ax_x=np.linspace(x_lim_lower,x_lim_upper,num=int(x_num)+1,endpoint=True)

            y_num=(y_lim_upper-y_lim_lower)/ax_t
            self.grid_ax_y=np.linspace(y_lim_lower,y_lim_upper,num=int(y_num)+1,endpoint=True)
            

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

    def plot_grid(self):
        
        X,Y=self.meshgrid()

        fig,ax=plt.subplots()
        ax.scatter(X,Y)
        plt.show()

