import numpy as np

class Sensor:

    ## for an individual sensor apart of a sensor array
    ##  xi           : sensor x-coordinate
    ##  yi           : sensor y-coordinate
    ##  target_theta : target [P_0,x-coordinate,y-coordinate]
    def __init__(self,xi,yi,target_theta=[25000,15,20]):

        self.I_list=[]
        self.theta_t=target_theta
        self.x=xi
        self.y=yi
        self.eta=1.7  ##threshold 2.5*sigma_w (noise)
        self.n=2  

    ## compute the distance between a sensor and a point (xt,yt)
    def distance(self,xt,yt):
        return np.sqrt((self.x-xt)**2+(self.y-yt)**2)
    
    ## compute the amplitude measured by a sensor given theta = [P0,xt,yt]
    def amplitude(self,theta):
        P_0=theta[0]
        xt=theta[1]
        yt=theta[2]
        d=self.distance(xt,yt)

        if d < 1:
            d=1 ## dont divide by d < 1

        return np.sqrt(P_0/(d**self.n))
    
    ## model influence WGN on signal amplitude measured by sensor
    def sample(self):
        
        s=self.amplitude(self.theta_t)+np.random.default_rng().normal()
        
        if s >= self.eta:
            I=1
        else:
            I=0
        self.I_list.append(I)
