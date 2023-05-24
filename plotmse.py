import sys
import os
import pdb
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use('classic')

process_list_file=os.getcwd()+'\\queue\\'+sys.argv[1]

to_process=[]
with open(process_list_file,'r') as file_r:
    for line in file_r:
        to_process.append(line.rstrip())

trials=[]
for log_name in to_process:

    log_path=os.getcwd()+'\\logs\\'
    log=log_path+log_name+'.txt'

    trial={'theta':np.zeros((3,)),
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
    
                theta=[]
                for i in range(0,len(temp)-1):
    
                    theta.append(float(temp[i]))
    
            if '%_ESTIMATE' in line:
                mc_results_list.append(line.rstrip()
                               .replace('%_ESTIMATE:: ','')
                               .replace('(','')
                               .replace(')','')
                               .replace(' ','')
                               .split(','))
    
    trial['theta'][0]=theta[0]
    trial['theta'][1]=theta[1]
    trial['theta'][2]=theta[2]

    point_estimates=np.zeros((len(mc_results_list),2))
    for index,point in enumerate(mc_results_list):
        point_estimates[index,0]=point[0]
        point_estimates[index,1]=point[1]
        trial['results'].append(point)
    
    mse_x_sum=0
    mse_y_sum=0

    x_t=theta[1]
    y_t=theta[2]
    
    for i in range(0,point_estimates.shape[0]):
    
        mse_x_sum+= ( abs ( point_estimates[i,0] - x_t ) ) ** 2
        mse_y_sum+= ( abs ( point_estimates[i,1] - y_t ) ) ** 2
    
    rmse_x = np.sqrt( ( 1 / point_estimates.shape[0]) * mse_x_sum )
    rmse_y = np.sqrt( ( 1 / point_estimates.shape[0]) * mse_y_sum )

    trial['rmse_x']=rmse_x
    trial['rmse_y']=rmse_y

    trials.append(trial)

def plot():

    fig,axs=plt.subplots(2,1)

    # p0 on x
    # rmse on y
    # for x coord
    x1_data=[]
    y1_data=[]
    x2_data=[]
    y2_data=[]

    for trial in trials:
        x1_data.append(trial['theta'][0])
        y1_data.append(trial['rmse_x'])
        x2_data.append(trial['theta'][0])
        y2_data.append(trial['rmse_y'])

    axs[0].plot(x1_data,y1_data)
    axs[1].plot(x2_data,y2_data)

    axs[0].set_ylim(0,max(y1_data)*1.5)
    axs[1].set_ylim(0,max(y2_data)*1.5)

    axs[0].set_xlabel('Signal Intensity')
    axs[1].set_xlabel('Signal Intensity')

    axs[0].set_ylabel('x-coordinate RMSE')
    axs[1].set_ylabel('y-coordinate RMSE')

    plt.tight_layout()
    plt.show()

plot()

