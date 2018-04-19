# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 14:15:13 2018

@author: Administrator
"""
#%% import packages and find paths
import os
import tool
import execute_module
#import time
#import optimization_module
#import math


cur_path = os.getcwd()
cur_path1= cur_path + '\\param_txt\\'
path = []
for item in os.listdir(cur_path1):
    path.append(cur_path1 + item)
    
# flag_path = path[0]
# prep_path = path[1]
# result_path = path[2]
# stru_path = path[3]

# C:\Users\Public\Documents\CMS\FocalData\MonacoTemplates
#colone_path1 = input('Please input the Monaco Template file path:\n')
colone_path  = 'C:\\Users\\Public\\Documents\\CMS\\FocalData\\MonacoTemplates\\colonetemplate1.hyp'
            

tar_res_nam = ['PGTVnx6996','PGTVnd6996','PTV5096'] #这里需要进行调整来需要
step_size = [1,1,1,1,1,0.5,0.5,0.5]



ind_loc_strt = []
loc = [3,7,8,10,9]
start = [13,14,10,7,15]
cost_name = ['shrinkmargin=','isoconstraint=','isoeffect=','weight=','relativeimpact=']
ind_loc_strt.append(loc)
ind_loc_strt.append(start)
ind_loc_strt.append(cost_name)

theshold = 0.2
#%% ======== generate the correspoding template.hyp(dMLC/VMAT, isocenter, number of organs, costfun...) =========

#tool.run_generate_template(cur_path,path_tem,colone_path,tar_res_nam)


#%% ============== generate some variables in advance =====================

# read the prescription requist from prep.csv files



inf_iter = {}
diff_iter = {}
#%% ============= optimization step 1: shrink_margin optimization ============================ 
   # if target OK or NO? 
   # No --> 
   # Yes --> if X% > 98% then jump to step 2
   #         else  adjust the shrink margin parameters
iteration1 = 5
for i in range(iteration1):
    
    fla,inf,diff = execute_module.shrink_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt)
    
    inf_iter['iteration' + str(i)] = inf
    diff_iter['iteration' + str(i)] = diff
    
    if fla == 2: 
        print('The Set of ShrinkMargin is rational!!\n')
        
        
        ## delete the extra variables infunctional for target
        ## isoconstraint <-- isoeffect 
        break
    
     
#%%======================= optimization step 2: patient optimization =======================
   # 1) isoconstraint <-- isoeffect in serial of patient
   # 2) gradually, reduce isoconstraint and ensure the target OK
   # 3) if target bad or weight > threshold then run to step 3
   
iteration2 = 12
count = 0
for j in range(iteration2):
    ## read struct_fun from template   
    ## 
    
    fla2,inf,diff = execute_module.patient_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt,count)
    count += 1
    
    inf_iter['iteration' + str(j+i+1)] = inf
    diff_iter['iteration' + str(j+i+1)] = diff

    if fla2 == 3: 
        
        print('The Set Serial in patient is ok!!\n')
        break
    
    ## delete the extra variables infunctional for target
    ## isoconstraint <-- isoeffect 
    
#%% ==================== optimization step 3: OARs optimization ===========================
   # this can learn from the former program
   # if target OK ? --> ...
   # if OARs OK ? --> ... 
   
  
iteration3 = 18
for k in range(iteration3):
    
    fla3,inf,diff = execute_module.OARs_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt,theshold)
    
    inf_iter['iteration' + str(k + j + i + 2)] = inf
    diff_iter['iteration' + str(k + j + i + 2)] = diff
    


#%%  Save the optimization inforamtion data 
tool.save_results(cur_path,inf_iter,diff_iter)
tool.plot(cur_path)