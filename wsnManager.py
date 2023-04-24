import grid
import emitter
import numpy as np
import logging
from scipy import special as sp
import pdb


# ***********************************************************************
# A class to create wireless sensor network objects.
# ***********************************************************************
class WsnManager:

        def __init__(self,domain_size,network_size,sample_T,localize):

            """
                Parameters:  domain_size : int

                                The length of a square grid with dimensions domain_size x domain_size.

                             network_size : int

                                The length of a square network with dimensions network_size x network_size.

                             sample_T : int

                                The number of samples to collect.

                             localize : str, {'mle', 'snap'}

                                The localization routine to use.

                Returns:  None

            """

            assert(network_size % 2 == 0 and network_size >= 2), 'Invalid number of sensors.'
            
            self.domain_size=domain_size
            self.network_size=network_size
            self.sample_T=sample_T
            self.localize=localize

            self.network=self.Network(self.domain_size,self.network_size,self.sample_T,self.localize)

        # ********************************************************
        # Network class- subclass of WsnManager
        # ********************************************************
        class Network:

            def __init__(self,domain_size,network_size,sample_T,localize):

                """

                    Parameters:  domain_size : int

                                    Size of the domain.

                                 network_size : int

                                    Number of sensors in a row of the square network array.

                                 sample_T : int 

                                    Number of samples per sample period.

                                 localize : str, {'mle', 'snap'}

                                    Localization method.

                """
                
                self.domain_size=domain_size
                self.network_size=network_size
                self.sample_T=sample_T
                self.localize=localize

                self.grid=grid.Grid(self.domain_size,resolution=self.domain_size/self.network_size) # network grid
                self.coords=self.grid.coordinates(self.grid.domain_xo)
                self.sensors=[]
                
                for i in range(0,self.coords.shape[0]):

                    x=self.coords[i,0]
                    y=self.coords[i,1]
                    eta=1.7
                    sigma=1

                    self.sensors.append(self.Sensor(x,y,eta,sigma))

                self.centralPcr=self.CentralPcr(self)

            # *****************************************************
            # Each sensor collects a sample of the emitter passed
            # *****************************************************
            def sample(self,Emitter):
                
                """
                    Parameters:  Emitter : object
                        
                                    The emitter to sample.

                """

                self.emitter=Emitter

                for i in range(0,len(self.sensors)):

                    for j in range(0,self.sample_T):

                        sensor=self.sensors[i]
                        sensor.sample(Emitter)

                # do the localization algo. here < --
                self.centralPcr.locate()
            
            # ********************************************************
            # Sensor class- subclass of Network.
            # ********************************************************
            class Sensor:

                def __init__(self,x,y,eta,sigma):
                    
                    """
                        Parameters:  x : float
                                        
                                        Sensor x-coordinate.

                                     y : float

                                        Sensor y-coordinate.

                                     eta : float

                                        Sensor threshold.

                                     sigma : float
                                        
                                        Sensor noise power.

                    """
                    
                    self.x=x
                    self.y=y
                    self.eta=eta
                    self.sigma=sigma
                    self.S=[] # samples unquantized
                    self.I=[] # samples quantized

                # ********************************************
                # Sample an emitter.
                # ********************************************
                def sample(self,Emitter):
                    
                    """
                        Parameters:  Emitter : object

                                        Emitter to sample.

                    """

                    self.M=1 # quantization level (single bit)
                    self.L=2**self.M
                    
                    # ******************************************
                    # Quantize a sample.
                    # ******************************************
                    def quantize(s):

                        """
                            Parameters:  s : sample

                                            Sample to quantize.

                        """

                        if s > self.eta:

                            return 1

                        if s < self.eta:

                            return 0

                    a=Emitter.amplitude(self.x,self.y)
                    w=np.random.default_rng().normal()
                    s=a+w
                    self.S.append(s)
                    self.I.append(quantize(s))

            # **************************************************
            # Central Processing Node subclass of Network
            # **************************************************
            class CentralPcr:

                def __init__(self,Network):

                    self.network=Network
                    
                    self.domain_size=self.network.domain_size
                    self.network_size=self.network.network_size
                    self.sample_T=self.network.sample_T
                    self.localize=self.network.localize

                    self.grid=grid.Grid(self.domain_size)
                    self.coords=self.grid.coordinates(self.grid.domain_xo)

                    if self.localize == 'mle':
                        
                        self.mleManager=self.MleManager(self)
                        
                    elif self.localize == 'snap':

                        pass
                    
                def locate(self):

                    if self.localize == 'mle':
                        
                        self.mleManager.max_likelihood()
                        
                    elif self.localize == 'snap':

                        pass

                class MleManager:

                    def __init__(self,CentralPcr):

                        self.centralPcr=CentralPcr
                    
                    def max_likelihood(self):

                        emitter_actual=self.centralPcr.network.emitter
                        
                        def qfunc(x):

                            return 0.5 - 0.5 * sp.erf(x/np.sqrt(2))

                        cells=self.centralPcr.grid.domain_xo
                        self.le_matrix=np.zeros((cells.size,cells.size))

                        coords=[]
                        estimate=[]

                        for i,xg in enumerate(cells):
                            
                            for j,yg in enumerate(cells):

                                theta=[25000,round(xg,2),round(yg,2)]

                                emitter_temp=emitter.Isotropic(theta,emitter_actual.n)

                                sum_outer=0
                                for index,sensor in enumerate(self.centralPcr.network.sensors):

                                    sum_inner=0
                                    for I_idx,I in enumerate(sensor.I):
                                        
                                        qval=qfunc(sensor.eta-emitter_temp.amplitude(sensor.x,sensor.y))

                                        if qval == 0:

                                            qval+=1e-12

                                        if qval == 1:

                                            qval+=-1e-12
                                        
                                        lle=I*np.log(qval)+(1-I)*np.log(1-qval)
                                        sum_inner+=lle
                                        
                                        assert(not np.isnan(lle)), 'LLE NaN at sample '+str(I_idx)
                                        assert(not np.isnan(sum_inner)), 'Inner sum NaN at sample '+str(I_idx)

                                    sum_outer+=sum_inner

                                    assert(not np.isnan(sum_outer)), 'Outer sum NaN at sensor '+str(index)
                                
                                logging.info(str(theta)+' '+str(sum_outer))
                                self.le_matrix[i,j]=sum_outer

                                estimate.append(sum_outer)
                                coords.append(theta)

                            logging.info(str(i)+' of '+str(cells.size))

                        pdb.set_trace()

                        le_coords=np.unravel_index(np.argmax(self.le_matrix,axis=None),self.le_matrix.shape)

                        self.estimate=(cells[le_coords[0]],cells[le_coords[1]])

                        pdb.set_trace()
                        
                        return self.estimate


                class Snap:

                    def __init(self):

                        pass
