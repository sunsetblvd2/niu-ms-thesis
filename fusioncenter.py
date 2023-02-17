import numpy as np
from scipy import special as sp
import datetime
import logging
import os
import grid

import pdb


class FusionCenter:
    
    def __init__(self,grid_l,cell_l=0.1,grid_save=False):

        logging.info('*** Initializing fusion center ***')
        self.data_received=False
        self.lle_filled=False
        self.grid_save=grid_save
        
        ##self.le_grid=grid.Grid(grid_l,ax_t=cell_l)
        ## not using full grid to save time:
        ## using setting from varshney paper [-10,40] and [-10,40]
        ## also not using full granularity to save time
        ## Tested good.
        self.le_grid=grid.Grid(grid_l,ax_t=0.5,ticks='custom',x_lim_lower=-5,x_lim_upper=40, \
                y_lim_lower=-5,y_lim_upper=40)
        
        self.sa=[]

    def receive(self,sa):
        
        self.sa=sa

        ## L = 2^M (M-bit data received)
        self.M=0
        for digit in str(self.sa[0].I_list[0]):
            self.M+=1

        self.L=2**self.M

        self.data_received=True
        
        ## log CRLB
        self.cramer_rao_lower_bound()

        logging.info('%_CRLB_P0:: '+str(np.sqrt(self.crlbm[0,0])))
        logging.info('%_CRLB_xt:: '+str(np.sqrt(self.crlbm[1,1])))
        logging.info('%_CRLB_yt:: '+str(np.sqrt(self.crlbm[2,2])))

        return 0

    def qfunc(self,x):
        return 0.5-0.5*sp.erf(x/np.sqrt(2))

    def save_mat(self):

        assert(self.lle_filled), 'Attempting to save LLE before filling grid.'

        cwd=os.getcwd()
        outfile=cwd+'\\data\\le_mat_'+datetime.datetime.now().strftime('%y%b%d%H%M%S')+'.npy'
        
        logging.info('*** Saving LE matrix ***')
        logging.info(' >> File:: '+str(outfile))

        np.save(outfile,self.le_matrix)

    def fisher_information_matrix(self):

        logging.info('>> Computing FIM')

        assert(self.data_received), 'Sensor data unavailable. Cannot compute FIM.'
            
        ## 3) compute J11 -- J33
        self.fim=np.zeros((3,3))
        
        for i,sensor in enumerate(self.sa):
            
            ## a - amplitude (theta_target)
            ## eta - threshold for l=1
            x_i=sensor.x ## sensor x coord
            y_i=sensor.y ## sensor y coord
            x_t=sensor.theta_t[1] ## target x coord
            y_t=sensor.theta_t[2] ## target y coord
            d_i=sensor.distance(x_t,y_t) ## distance from sensor to target
            a_i=sensor.amplitude(sensor.theta_t) ## amplitude to sensor (true)
            eta_i=sensor.eta ## sensor threshold
            n_i=sensor.n

            ## 1) compute kappa for all i
                ## M-bit data received
                ## L = 2^M
            k_i_sum=0
            for l in range(0,self.L):           
                
                ## COMPUTE GAMMA
                ## this needs eta and ai for each sensor. ai computed from target.
                ## eta0 -inf
                ## eta1 sensor.eta
                ## eta2 inf
                ## each exp evaluates to 0 in inf and -inf cases
                
                if l==0:
                    alpha=(np.NINF-a_i)**2 / 2
                    beta=(eta_i-a_i)**2 / 2
                else:
                    alpha=(eta_i-a_i)**2 / 2
                    beta=(np.inf-a_i)**2 / 2

                gamma_il=(np.exp(-alpha)-np.exp(-beta))**2
                
                ## COMPUTE Pil -- Q(.)-Q(.)

                if l==0:
                    alpha=np.NINF-a_i
                    beta=eta_i-a_i
                else:
                    alpha=eta_i-a_i
                    beta=np.inf-a_i

                alpha_qval=self.qfunc(alpha)
                beta_qval=self.qfunc(beta)

                p_il=alpha_qval-beta_qval ## at some point this goes to ZERO
                    ## for some reason alpha and beta become equivalent.
                        ## each Q(.) evaluates to 1
                        ## is this natural? 
                        ## do i set alpha and beta incorrectly?

                if p_il==0:
                    p_il+=1e-12## avoid divide by zero

                ## SUMMATION
                k_i_sum+=(gamma_il/p_il)

            k_i=(1/(8*np.pi*(1**2)))*k_i_sum
            
            ## 3) compute J11 -- J33
            ## summations first. handle multiplication once loop exits.
            self.fim[0,0]+=k_i*(d_i**(-2*n_i)) / a_i**2  ## J11
            self.fim[0,1]+=k_i*(d_i**-(n_i+2))*(x_i-x_t) ## J12
            self.fim[0,2]+=k_i*(d_i**-(n_i+2))*(y_i-y_t) ## J13
            self.fim[1,0]+=k_i*(d_i**-(n_i+2))*(x_i-x_t) ## J21
            self.fim[1,1]+=k_i*(a_i**2)*(d_i**-4)*((x_i-x_t)**2)## J22
            self.fim[1,2]+=k_i*(a_i**2)*(d_i**-4)*(x_i-x_t)*(y_i-y_t) ## J23
            self.fim[2,0]+=k_i*(d_i**-(n_i+2))*(y_i-y_t) ## J31
            self.fim[2,1]+=k_i*(a_i**2)*(d_i**-4)*(x_i-x_t)*(y_i-y_t) ## J32
            self.fim[2,2]+=k_i*(a_i**2)*(d_i**-4)*((y_i-y_t)**2) ## J33
        

        self.fim[0,0]*=1 ## J11
        self.fim[0,1]*=n_i## J12
        self.fim[0,2]*=n_i## J13
        self.fim[1,0]*=n_i ## J21
        self.fim[1,1]*=n_i**2 ## J22
        self.fim[1,2]*=n_i**2 ## J23
        self.fim[2,0]*=n_i ## J31
        self.fim[2,1]*=n_i**2 ## J32
        self.fim[2,2]*=n_i**2 ## J33

        return 0

    def cramer_rao_lower_bound(self):

        logging.info('>> Computing CRLB Matrix')

        assert(self.data_received), 'Sensor data unavailable. Cannot compute CRLB.'
        
        self.fisher_information_matrix()

        ## Compute determinant of J
        ## |J|=J11*J22*J33+2*J12*J13*J23-J11*J23^2-J22*J13^2-J33*J12^2
        fim_det_t1=self.fim[0,0]*self.fim[1,1]*self.fim[2,2]
        fim_det_t2=2*self.fim[0,1]*self.fim[0,2]*self.fim[1,2]
        fim_det_t3=self.fim[0,0]*(self.fim[1,2]**2)
        fim_det_t4=self.fim[1,1]*(self.fim[0,2]**2)
        fim_det_t5=self.fim[2,2]*(self.fim[0,1]**2)

        fim_det=fim_det_t1+fim_det_t2-fim_det_t3-fim_det_t4-fim_det_t5

        ## fill CRLB matrix
        self.crlbm=np.zeros((3,3))
        
        self.crlbm[0,0]=self.fim[1,1]*self.fim[2,2]-(self.fim[1,2]**2)
        self.crlbm[0,1]=self.fim[0,2]*self.fim[1,2]-self.fim[0,1]*self.fim[2,2]
        self.crlbm[0,2]=self.fim[0,1]*self.fim[1,2]-self.fim[0,2]*self.fim[1,1]
        self.crlbm[1,0]=self.fim[0,2]*self.fim[1,2]-self.fim[0,1]*self.fim[2,2]
        self.crlbm[1,1]=self.fim[0,0]*self.fim[2,2]-(self.fim[0,2]**2)
        self.crlbm[1,2]=self.fim[0,1]*self.fim[0,2]-self.fim[0,0]*self.fim[1,2]
        self.crlbm[2,0]=self.fim[0,1]*self.fim[1,2]-self.fim[0,2]*self.fim[1,1]
        self.crlbm[2,1]=self.fim[0,1]*self.fim[0,2]-self.fim[0,0]*self.fim[1,2]
        self.crlbm[2,2]=self.fim[0,0]*self.fim[1,1]-(self.fim[0,1]**2)

        self.crlbm*=(1/fim_det)

        return 0

    def max_likelihood_estimate(self):

        assert(self.data_received), 'Sensor data unavailable. Cannot compute MLE.'

        self.p_x,self.p_y=self.le_grid.axes()

        le_grid_dim=self.le_grid.dimensions()
        self.le_matrix=np.zeros(le_grid_dim)

        for i,xg in enumerate(self.p_x):

            for j,yg in enumerate(self.p_y):

                theta=[25000,round(xg,2),round(yg,2)]

                sum_outer=0
                for index,sensor in enumerate(self.sa):

                    #logging.info('>> Sensor '+str(index)+' coordinates: '+str((sensor.x,sensor.y)))
                    #logging.info('>> Sensor '+str(index)+' threshold: '+str(sensor.nu))
                    #logging.info('>> Sensor '+str(index)+' amplitude(thetaLLE): '+str(sensor.amplitude(theta)))

                    sum_inner=0
                    for I_idx,I in enumerate(sensor.I_list):
                        
                        qval=self.qfunc(sensor.eta-sensor.amplitude(theta))
                        if qval == 0:
                            #logging.info('### qval=0. Adjusting qval to avoid NaN.')
                            qval+=1e-12
                        if qval == 1:
                            #logging.info('### qval=1. Adjusting qval to avoid NaN.')
                            qval+=-1e-12
                        
                        lle=I*np.log(qval)+(1-I)*np.log(1-qval)
                        sum_inner+=lle
                        
                        assert(not np.isnan(lle)), 'LLE NaN at sample '+str(I_idx)
                        assert(not np.isnan(sum_inner)), 'Inner sum NaN at sample '+str(I_idx)

                    sum_outer+=sum_inner

                    assert(not np.isnan(sum_outer)), 'Outer sum NaN at sensor '+str(index)
                
                #logging.info('>> Log p(I|'+str(theta)+')='+str(sum_outer))
                #logging.info('>> p(I|'+str(theta)+')='+str(le))
                #logging.info('>> Storing LE at '+str((i,j))+'in le_matrix.')

                self.le_matrix[i,j]=sum_outer
        
        self.lle_filled=True 

        if self.grid_save:
            self.save_mat()  ## save the grid, might be useful for large grids

        ## get the coordinates of the estimate.
        le_coords=np.unravel_index(np.argmax(self.le_matrix,axis=None),self.le_matrix.shape)

        self.estimate=(self.p_x[le_coords[0]],self.p_y[le_coords[1]])
        
        return self.estimate

