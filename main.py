# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 22:45:50 2018

@author: yunyangye
"""
import os
import csv
import numpy as np
from shutil import rmtree

#1.sampleing: get different value of model input (LHM)
#2.modify IDF file and run model, get model output (site EUI)
#3.train the model input and output by using meta model,generate new model input,generate model output by using meta model (Morris,FAST,Sobol,Non-parametric analysis (CompModSA))
#4.sensiticity analysis

###############################################################################
# sensitivity analysis
## method description

#### 1-Morris:
###### sample: from SALib.sample import morris
###### analyze: from SALib.analyze import morris

#### 2-FAST:
###### sample: from SALib.sample import fast_sampler
###### analyze: from SALib.analyze import fast

#### 3-Sobol:
###### sample: from SALib.sample import saltelli
###### analyze: from SALib.analyze import sobol

#### 4-Non-parametric analysis (CompModSA):
###### sample: Latin Hypercube Sampling (LHS)
###### analyze: check the type of relationship:
###### LIN_REG: Linear Regression
###### RS_REG: Response Surface Regression
###### GAM: Generalized Additive Models
###### RP_REG: Recursive Partitioning Regression

###############################################################################
     

pathway = os.getcwd()
###############################################################################
# list all the inputs which can be modify 
# define the climate zones that need to be considered
climate = ['3B','3C']# define the needed climate zones

# number of samples for training and testing meta-models
#number of samples in each climate zone = num_sample * number of sensitive model inputs
num_sample = 5
# kernel of meta model (options: 'rbf','linear','poly','sigmoid')
kernel = 'linear'

# sensitivity analysis inputs
## Morris
mo_num_sample = 200# number of the samples for each parameter [final #samples: num*(#parameters+1)]

mo_num_levels_sample = 8# the number of grid levels
mo_grid_jump_sample = 4# the grid jump size

## FAST
fa_num_sample = 1000# Sample size N > 4M^2 is required. M=4 by default
## Sobol
so_num_sample = 1000# Sample size N > 4M^2 is required. M=4 by default

## Non-parametric analysis (CompModSA)
np_num_sample = 10000# LHS sample size

# parameters' library
# list the entire sets of some inputs
climate_lib = ['3B','3C']


os.chdir(pathway)
######################################################################################
#1.sampleing: get different value of model input (LHM)
#os.chdir(os.path.join(pathway,'Meta'))
import sampleMeta as samp
#os.chdir(pathway)

for cz in climate:
    data_set,param_values = samp.sampleMeta(num_sample,cz) 
    # data_set contains variables name, min value, max value in climate zone cz
    #param_values is the sample which contain the vaiables' value
    
    ## record the data in the folder './results/samples'
    ## store the information of data_set
    with open('./results/samples/data_set_'+cz+'.csv', 'wb') as csvfile:
        for row in data_set:
            data = csv.writer(csvfile, delimiter=',')
            data.writerow(row)
    
    ## store the information of param_values
    with open('./results/samples/param_values_'+cz+'.csv', 'wb') as csvfile:
        for row in param_values:
            data = csv.writer(csvfile, delimiter=',')
            data.writerow(row)  

###################################################################################
#2.modify IDF file and run model, get model output (site EUI)s
###model inputs and outputs are saved in './results/energy_data.csv'
#os.chdir(os.path.join(pathway,'runModel'))
import parallelSimuMeta as ps
#os.chdir(pathway)
for cz in climate:
    model_results,run_time = ps.parallelSimu(cz,1)
rmtree('./Model/update_models')
print run_time

