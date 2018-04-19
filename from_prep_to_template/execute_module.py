# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 11:23:39 2018

@author: Administrator
"""

#%% program running module

def shrink_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt):
    '''
     flag_path = path[0]
     prep_path = path[1]
     result_path = path[2]
     stru_path = path[3]
     
    '''
  

    import optimization_module
    import tool
    
    struct_fun1,struct_index,line,diff_result = tool.public_execution(path,colone_path)
       
    grid = 3
    
   # remark the OARS name
#       OARs = str_name_eval[3:] 
   
    struct_fun_updated,mark1,information = optimization_module.shrink_target(struct_fun1,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt)
   
    if mark1 == 3:
        
        print ('Flag = 3:  target shrinkmargin still not good !!\n')
       
        tool.write_template(line,colone_path,struct_fun_updated)
       
        # write flag to 1
        tool.write_flag(path[0])
       
    else:
       
        tool.write_template(line,colone_path,struct_fun_updated)
       
        print ('Flag = 2: shrinkmargin is good  !!\n')
        # write flag to 1
        tool.write_flag(path[0])
           
    return mark1,information,diff_result
           
           
         
def patient_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt,count):
    
    import optimization_module
    import tool
    
    struct_fun1,struct_index,line,diff_result = tool.public_execution(path,colone_path)
       
    grid = 3
    
   # remark the OARS name
#       OARs = str_name_eval[3:] 
       
    struct_fun_updated,mark2,information = optimization_module.patient_opt(struct_fun1,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt,count)
    
    if mark2 == 3:
        
        print ('Target was underdose!!\n')
        tool.write_template(line,colone_path,struct_fun_updated)
       
        print('Updated finished...\n')
        # write flag to 1
        tool.write_flag(path[0])
       
    else:
        tool.write_template(line,colone_path,struct_fun_updated)

        # write flag to 1
        tool.write_flag(path[0])
        print('Target has maintained...\n')
           
           
    return mark2,information,diff_result    
#    OARs_opt(struct_fun,hyp_path,flag_path,target_name,diff_result,line)
    

def OARs_running(path,colone_path,tar_res_nam,step_size,ind_loc_strt,theshold):
    
    import optimization_module
    import tool
    
    struct_fun1,struct_index,line,diff_result = tool.public_execution(path,colone_path)
       
    grid = 3
       
    struct_fun_updated,mark3,information = optimization_module.OARs_opt(struct_fun1,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt,theshold)
    
    if mark3 == 3:
        print ('Target was underdose!!\n')
        tool.write_template(line,colone_path,struct_fun_updated)
       
        print('Updated finished...\n')
        # write flag to 1
        tool.write_flag(path[0])
       
    else:
        tool.write_template(line,colone_path,struct_fun_updated)

        # write flag to 1
        tool.write_flag(path[0])
        print('Target has maintained...\n')
           
           
    return mark3,information,diff_result