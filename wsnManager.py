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

        def __init__(self,domain_size,network_size,sample_T,noise_power,localize):

            """
                Parameters:  domain_size : int

                                The length of a square grid with dimensions domain_size x domain_size.

                             network_size : int

                                The length of a square network with dimensions network_size x network_size.

                             sample_T : int

                                The number of samples to collect.

                             noise_power : float

                                Additive noise power.

                             localize : str, {'mle', 'snap'}

                                The localization routine to use.

                Returns:  None

            """

            assert(network_size % 2 == 0 and network_size >= 2), 'Invalid number of sensors.'
            
            self.domain_size=domain_size
            self.network_size=network_size
            self.sample_T=sample_T
            self.noise_power=noise_power
            self.localize=localize

            self.network=self.Network(self.domain_size,self.network_size,self.sample_T,self.noise_power,self.localize)

        # ********************************************************
        # Network class- subclass of WsnManager
        # ********************************************************
        class Network:

            def __init__(self,domain_size,network_size,sample_T,noise_power,localize):

                """

                    Parameters:  domain_size : int

                                    Size of the domain.

                                 network_size : int

                                    Number of sensors in a row of the square network array.

                                 sample_T : int 

                                    Number of samples per sample period.

                                 noise_power : float

                                    Additive noise power.

                                 localize : str, {'mle', 'snap'}

                                    Localization method.

                """
                
                self.domain_size=domain_size
                self.network_size=network_size
                self.sample_T=sample_T
                self.noise_power=noise_power
                self.localize=localize

                self.grid=grid.Grid(self.domain_size,resolution=self.domain_size/self.network_size) # network grid
                self.coords=self.grid.coordinates(self.grid.domain_xo)
                self.sensors=[]
                
                for i in range(0,self.coords.shape[0]):

                    x=self.coords[i,0]
                    y=self.coords[i,1]
                    eta=1.7
                    sigma=self.noise_power

                    self.sensors.append(self.Sensor(x,y,eta,sigma))

                self.centralPcr=self.CentralPcr(self)

            # **************************************************************
            # Plot full network with emitter heatmap.
            # **************************************************************
            def plot(self,Emitter):

                """
                    Parameters:  Emitter : object
                        
                                    The emitter to sample.

                """

                Emitter.heatmap(self.domain_size)
                self.grid.plot(Emitter.fig,Emitter.ax)


                return 0

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
                return self.centralPcr.locate()
            
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
                    w=np.random.default_rng().normal(0,self.sigma)
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

                        self.snapManager=self.SnapManager(self)

                def locate(self):

                    if self.localize == 'mle':
                        
                        return self.mleManager.max_likelihood()
                        
                    elif self.localize == 'snap':

                        return self.snapManager.snap()

                class MleManager:

                    def __init__(self,CentralPcr):

                        self.centralPcr=CentralPcr
                    
                    def max_likelihood(self):

                        emitter_actual=self.centralPcr.network.emitter
                        
                        def qfunc(x):

                            return 0.5 - 0.5 * sp.erf(x/np.sqrt(2))

                        cells=self.centralPcr.grid.domain_xo
                        self.le_matrix=np.zeros((cells.size,cells.size))

                        for i,xg in enumerate(cells):
                            
                            for j,yg in enumerate(cells):

                                theta=[emitter_actual.P_0,round(xg,2),round(yg,2)]

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
                                
                                self.le_matrix[i,j]=sum_outer

                        le_coords=np.unravel_index(np.argmax(self.le_matrix,axis=None),self.le_matrix.shape)
                        self.estimate=(cells[le_coords[0]],cells[le_coords[1]])

                        return self.estimate

                class SnapManager:

                    def __init__(self,CentralPcr):

                        self.centralPcr=CentralPcr

                    def snap(self):

                        emitter_actual=self.centralPcr.network.emitter

                        cells=self.centralPcr.grid.domain_xo
                        self.le_matrix=np.zeros((cells.size,cells.size))

                        def inside_roc(coords_sensor,roc,coords_point):

                            sensor_x=coords_sensor[0]
                            sensor_y=coords_sensor[1]
                            x=coords_point[0]
                            y=coords_point[1]

                            d=roc**2

                            if ((abs(x-sensor_x))**2 + (abs(y-sensor_y))**2) <= d:

                                return True

                            else:

                                return False

                        for i,sensor in enumerate(self.centralPcr.network.sensors):

                            roc= ( emitter_actual.P_0 / sensor.eta ) ** (1 / emitter_actual.n)

                            for j,I in enumerate(sensor.I):

                                for k,xg in enumerate(cells):
                            
                                    for l,yg in enumerate(cells):

                                        inside=inside_roc((sensor.x,sensor.y),roc,(xg,yg))

                                        if I == 1 and inside is True:

                                            self.le_matrix[k,l]+=1

                                        elif I == 0 and inside is True:

                                            self.le_matrix[k,l]-=1

                        le_coords=np.unravel_index(np.argmax(self.le_matrix,axis=None),self.le_matrix.shape)
                        self.estimate=(cells[le_coords[0]],cells[le_coords[1]])

                        return self.estimate
