import numpy as np
import logging
import matplotlib.pyplot as plt
import pdb

class Grid:
    
    # ****************************************************************
    # Construct a square grid with origin (0, 0)
    # ****************************************************************
    def __init__(self,size,resolution=0):

        """

            Parameters: size : int

                            Length of the x- and y-domain of the square grid.

                        resolution : int {0, 1, 2}

                            Length of square cells centered about each grid point.

                            0 : 1.00 resolution. (Default)
                            1 : 0.50 resolution.
                            2 : 0.25 resolution.
                            n : n resolution.


        """
        
        assert(size % 2 == 0), 'Grid size must be an even integer.'
        assert(size >= 4), 'Size does not meet minimum condition.'

        if resolution not in [0, 1, 2]:
            print('>> Warning! Grid resolution selection is custom. Cannot guarantee stability.')

        self.o=0
        self.size=size
        self.res=resolution

        if self.res == 0:

            self.res=1.0

        elif self.res == 1:

            self.res=0.5

        elif self.res == 2:

            self.res=0.25

        else:

            self.res=self.res

        start=self.o-round(self.size/2,2)
        stop=self.o+round(self.size/2,2)
        num=int(self.size/self.res)+1

        self.domain=np.linspace(start,stop,num=num,endpoint=True)

        self.X,self.Y=np.meshgrid(self.domain,self.domain) # define cells
        self.offset() # define center points of cells

    # **************************************************************************
    # Construct a sub-grid of a square grid with origin (0, 0). The sub-grid is
    # constructed using the center points of cells in the square grid.
    # **************************************************************************
    def offset(self):

        """
        
            Parameters:  None

            Returns:  None

        """

        start=min(self.domain)+(self.res/2)
        stop=max(self.domain)-(self.res/2)
        num=self.domain.size-1

        self.domain_xo=np.linspace(start,stop,num=num,endpoint=True)

        self.X_xo,self.Y_xo=np.meshgrid(self.domain_xo,self.domain_xo)

    # ***************************************************************************
    # Return the coordinates of a square grid as a 2-D array.
    # ***************************************************************************
    def coordinates(self,domain):

        """ 

            Parameters:  domain : array

                         1-D array of points on x- and y-axes.

        """
        
        coordinates=np.zeros((domain.size**2,2))
        i=0
        
        for x in domain:

            for y in domain:

                coordinates[i,0]=x
                coordinates[i,1]=y
                i+=1

        return coordinates

    # ********************************************************************************
    # Plot the grid.
    # ********************************************************************************
    def plot(self,fig,ax):

        """

            Parameters: cells : bool, optional
                            
                            If true, show cells on the plot. Otherwise, do not show.
                            Default is False.

        """

        self.offset()
        
        #fig,ax=plt.subplots()

        ax[0,0].scatter(self.X_xo,self.Y_xo,s=4,color='gray',label='sensor')

        ax[0,0].set_xticks(self.domain)
        ax[0,0].set_yticks(self.domain)

        plt.grid(True)

        plt.legend()
        plt.show()

# end

