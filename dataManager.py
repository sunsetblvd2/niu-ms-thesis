import pdb
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.style.use('classic')

class DataManager:

    def __init__(self,expname,variable):

        """
        
            Parameters: expname : str

                          Experiment name.  
                        
                        variable : str

                            Experiment variable.
        
        """
        
        self.logdir=os.getcwd()+'\\logs\\'
        self.qdir=os.getcwd()+'\\queue\\'
        self.resultsdir=os.getcwd()+'\\results\\'
        self.expname=expname
        self.expresultspath=self.resultsdir+self.expname
        self.variable=variable
        self.data=[] # list of DataProcessor objects, 1 for each queue file

        self.populate()

    class DataParser:

        def __init__(self,queuefile):

            """
            
                Parameters: queuefile : str

                              Queue file name (full path).  
            
            """   

            self.queuefile=queuefile

            queuefilesplit=self.queuefile.rstrip('.txt').split('_')
            
            self.type=queuefilesplit[len(queuefilesplit)-1]
    
            self.trials=[]

            self.parse()

        def parse(self):

            """

                Parameters: none

            """

            with open(self.queuefile,'r') as file_r:

                for log_name in file_r:
            
                    log=log_name.rstrip()
            
                    trial={'P_0':0,
                           'x_t':0,
                           'y_t':0,
                           'n':0,
                           'sigma':0,
                           'results':[],
                           'rmse_x':0,
                           'rmse_y':0
                          }
            
                    mc_results_list=[]
                    with open(log,'r') as log_r:
                        for line in log_r:
                            if '*** Emitter_set' in line:
                                temp=line.split(':')
                                temp=temp[1].replace('[','')
                                temp=temp.replace(']','')
                                temp=temp.split(',')
                                
                                trial['P_0']=float(temp[0])
                                trial['x_t']=float(temp[1])
                                trial['y_t']=float(temp[2])
                                trial['n']=float(temp[3])
                    
                            if '*** Additive noise power' in line:
                                
                                temp=line.split(':')
                                trial['sigma']=float(temp[1])
                    
                            if '%_ESTIMATE' in line:
                                mc_results_list.append(line.rstrip()
                                               .replace('%_ESTIMATE:: ','')
                                               .replace('(','')
                                               .replace(')','')
                                               .replace(' ','')
                                               .split(','))
                    
                    point_estimates=np.zeros((len(mc_results_list),2))
                    for index,point in enumerate(mc_results_list):
                        point_estimates[index,0]=point[0]
                        point_estimates[index,1]=point[1]
                        trial['results'].append(point)
                    
                    mse_x_sum=0
                    mse_y_sum=0
            
                    for i in range(0,point_estimates.shape[0]):
                    
                        mse_x_sum+= ( abs ( point_estimates[i,0] - trial['x_t'] ) ) ** 2
                        mse_y_sum+= ( abs ( point_estimates[i,1] - trial['y_t'] ) ) ** 2
                    
                    rmse_x = np.sqrt( ( 1 / point_estimates.shape[0]) * mse_x_sum )
                    rmse_y = np.sqrt( ( 1 / point_estimates.shape[0]) * mse_y_sum )
            
                    trial['rmse_x']=rmse_x
                    trial['rmse_y']=rmse_y
            
                    self.trials.append(trial)

    def populate(self):

        queuefiles=[]
        for file_n in os.listdir(self.qdir):
            
            if self.expname in file_n:

                queuefiles.append(file_n)

        for queuefile in queuefiles:
        
            qpath=self.qdir+queuefile
            temp=self.DataParser(qpath)
            self.data.append(temp)
            
        return 0

    def plot(self):
        
        fig,axs=plt.subplots(2,1,figsize=(8,8))

        markers=['x','o']

        for index,algo in enumerate(self.data):

            x_x=[] # axis_coordinate
            y_x=[]
            x_y=[]
            y_y=[]

            for trial in algo.trials:

                x_x.append(trial[self.variable])
                y_x.append(trial['rmse_x'])
                x_y.append(trial[self.variable])
                y_y.append(trial['rmse_y'])
    
            axs[0].plot(x_x,y_x,'k--',marker=markers[index],label=algo.type)
            axs[1].plot(x_y,y_y,'k--',marker=markers[index],label=algo.type)
        
        axs[0].set_ylabel('RMSE x-coordinate')
        axs[1].set_ylabel('RMSE y-coordinate')

        if not os.path.isdir(self.expresultspath):
            os.system('mkdir '+self.expresultspath)

        figname=self.expresultspath+'\\'+self.expname+'_rmse.png'

        plt.legend(loc='center left',bbox_to_anchor=(1.1,0.5))
        plt.tight_layout()
        plt.savefig(figname)
#
