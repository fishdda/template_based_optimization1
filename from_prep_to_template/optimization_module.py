# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 09:18:31 2018

@author: Administrator
"""

#%% Optimization Module

def shrink_target(struct_fun,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt):
    '''
       1) find all the shrink_margin in struct_fun
       2) judge target dose is satisfied in each iteration
       3) ....
    '''
    import tool
    
    inf,shk_mgn,iso_effect,iso_constraint,weight,rel_imp = {},{},{},{},{},{}
    
    # extract all shrinkmargin from struct_fun
    shk_mgn = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][0],ind_loc_strt[1][0])   
    iso_effect = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][2],ind_loc_strt[1][2]) 
    iso_constraint = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][1],ind_loc_strt[1][1])  
    weight = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][3],ind_loc_strt[1][3]) 
    rel_imp = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][4],ind_loc_strt[1][4])  
    
    if diff_result[tar_res_nam[0]] >= 1 and diff_result[tar_res_nam[1]] >= 1 and diff_result[tar_res_nam[2]] >= 1:
        
        # flag change
        flag = 2
        
        # this means target has enough dose
        for key in iso_constraint.keys():
            
            if key not in tar_res_nam and key != 'patient':
                
                for i in range(len(iso_constraint[key])):
                    
                    iso_constraint[key][i][1] = (iso_constraint[key][i][1] + iso_effect[key][i][1])/2
        
        # transfer all shrinkmargin back to struct_fun
        struct_fun = tool.back_struct_fun(colone_path,shk_mgn,ind_loc_strt[2][0],ind_loc_strt[0][0]) 
        
        print('The shrink_margin set has been finished!!.........\n')
        print('Updated shrink margin:..........\n')
        for j in shk_mgn.keys():
            print(j,shk_mgn[j])
        
    else:
        
        flag = 3
        # 说明靶区剂量不够
        '''
           step1 : 调节 target shrink margin
           step2 : 调节 patient shrink margin
           step3 : 调节 OARs shrink margin
        '''
        #     =======调节参数模块========   #
        ###############################################
        ## 1) 先调整用 1.0 步长来增加 shk_mgn[target]中 shrink margin
        ## 2) 接着用 1.0 步长来增加 shk_mgn[patient]中 shrink margin
        for item in tar_res_nam:
            for index in shk_mgn[item]:
                if index[0] == 'type=mxd':
                    index[1] += step_size[0] # step_size[0] = 1
        
        for i in range(len(shk_mgn['patient'])):
            
            if shk_mgn['patient'][i][1] == 0:
                
                shk_mgn['patient'][i][1] += 0
            
            else:
                if shk_mgn['patient'][i][1] < 5:
                    
                    shk_mgn['patient'][i][1] = (grid+step_size[1])*2**(i-1) #step_size[1] = 1
                else:
                    shk_mgn['patient'][i][1] = 5
            
        
        ###############################################
        # transfer all shrinkmargin back to struct_fun
        struct_fun = tool.back_struct_fun(colone_path,shk_mgn,ind_loc_strt[2][0],ind_loc_strt[0][0])
        
        print('Target has still underdose, need to adjust parameters')
        print('Updated shrink margin:..........\n')
        for j in shk_mgn.keys():
            print(j,shk_mgn[j])
    

    # collect all the information into inf
    inf['shk_mgn'] = shk_mgn
    inf['iso_effect'] = iso_effect
    inf['iso_constraint'] = iso_constraint
    inf['weight'] = weight
    inf['rel_imp'] = rel_imp

    
    return struct_fun,flag,inf




def patient_opt(struct_fun,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt,count):
    '''
       1) find all the shrink_margin in struct_fun
       2) judge target dose is satisfied in each iteration
       3) ....
    '''
    
    import tool           
    inf,iso_effect,iso_constraint,weight,rel_imp = {},{},{},{},{}
    weight = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][3],ind_loc_strt[1][3]) 
    iso_effect = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][2],ind_loc_strt[1][2]) 
    iso_constraint = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][1],ind_loc_strt[1][1])  
    rel_imp = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][4],ind_loc_strt[1][4])  
    
    serial_inf_weight = []
    serial_inf_rel_imp = []
    
    for i in range(len(weight['patient'])):
        
        if weight['patient'][i][0] == 'type=se':
            
            serial_inf_weight.append(weight['patient'][i])
            
    for i in range(len(rel_imp['patient'])):
        
        if rel_imp['patient'][i][0] == 'type=se':
            
            serial_inf_rel_imp.append(weight['patient'][i])   
    

    
    if diff_result[tar_res_nam[0]] >= 1 and diff_result[tar_res_nam[1]] >= 1 and diff_result[tar_res_nam[2]] >= 1:
        
        
        flag = 2
        print('The original serial value in patient...\n')
        print(iso_constraint['patient'],'\n')
        
        ## 收patient上三个serial环，来控制剂量分布
        for i in range(len(iso_constraint['patient'])):
            
            if iso_constraint['patient'][i][0] == 'type=se':
                
                
                if weight['patient'][i][1] < 10 and rel_imp['patient'][i][1] <= 0.5:
                    
                    if count == 0: ## the first time need to be well!!
                        
                        iso_constraint['patient'][i][1] = iso_effect['patient'][i][1]
                        
                    else:
                        
                        iso_constraint['patient'][i][1] -= step_size[2]    # step_size[2] = 1
                    
                else:
                    
                    iso_constraint['patient'][i][1] = iso_effect['patient'][i][1]
                
        # transfer the updated variable to struct_fun                
        struct_fun = tool.back_struct_fun(colone_path,iso_constraint,ind_loc_strt[2][1],ind_loc_strt[0][1])
        
        print('The updated serial value in patient...\n')
        print(iso_constraint['patient'])
        print('The weight of parameters in patient...\n')
        print(serial_inf_weight)
        print('The relative impact in patient...\n')
        print(serial_inf_rel_imp)
        

    else:
        # 说明靶区剂量不够
        '''
           step1 : 调节 target shrink margin
           step2 : 调节 patient shrink margin
           step3 : 调节 OARs shrink margin
        '''
        flag = 3
        #     =======调节参数模块========   #
        ###############################################
#        break 
            
        
        ###############################################
        
        
#       transfer the last one variable to template, so we should halt to execute following code
#       struct_fun = tool.back_struct_fun(colone_path,iso_constraint,ind_loc_strt[2][1],ind_loc_strt[0][1])
        
        print('Target going to be wrong !...............\n')
        print('The updated serial value in patient unchanged...\n')
        print(iso_constraint['patient'],'\n')
        print('The weight of parameters in patient unchanged...\n')
        print(serial_inf_weight,'\n')
        print('The relative impact in patient unchanged...\n')
        print(serial_inf_weight,'\n')


    # collect all the information into inf
    inf['iso_effect'] = iso_effect
    inf['iso_constraint'] = iso_constraint
    inf['weight'] = weight
    inf['rel_imp'] = rel_imp        

  
    return struct_fun,flag,inf


def OARs_opt(struct_fun,tar_res_nam,diff_result,grid,colone_path,step_size,ind_loc_strt,theshold):
    '''
       1) find all the shrink_margin in struct_fun
       2) judge target dose is satisfied in each iteration
       3) ....
    '''
    
    import tool   
    inf,iso_effect,iso_constraint,weight,rel_imp = {},{},{},{},{}
    weight = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][3],ind_loc_strt[1][3]) 
    iso_effect = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][2],ind_loc_strt[1][2]) 
    iso_constraint = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][1],ind_loc_strt[1][1])  
    rel_imp = tool.extract_struc_fun(struct_fun,ind_loc_strt[0][4],ind_loc_strt[1][4])  
    ## In this program ,we only needs OARs
    for item in tar_res_nam:
        del weight[item]
        del iso_effect[item]
        del iso_constraint[item]
        del rel_imp[item]
    
    del weight['patient']
    del iso_effect['patient']
    del iso_constraint['patient']
    del rel_imp['patient']    
    
    del weight['Neck']
    del iso_effect['Neck']
    del iso_constraint['Neck']
    del rel_imp['Neck']    
    
    
    
    
    
    
    if diff_result[tar_res_nam[0]] >= 1 and diff_result[tar_res_nam[1]] >= 1 and diff_result[tar_res_nam[2]] >= 1:
        
        flag = 2 # indicate this functiion is good
        print('Original parameters\n')
        for key in iso_constraint.keys():
            print(key,iso_constraint[key])
        
        
        for key in iso_effect.keys():
            
            for i in range(len(iso_effect[key])):
                
                if iso_constraint[key][i][1] >= iso_effect[key][i][1]:
                    
                    if diff_result[key] > 1:
                        
                        iso_constraint[key][i][1] = iso_effect[key][i][1]
                    
                    else:
                        
                        if rel_imp[key][i][1] <= 0.5 and weight[key][i][1] <= 5:
                            
                            iso_constraint[key][i][1] = iso_effect[key][i][1]
                        
                        else:
                            
                            iso_constraint[key][i][1] += step_size[3]
                        
                else: ## (iso_constraint[key][i][1] < iso_effect[key][i][1])  
                    
                    if diff_result[key] > 1:
                         
                        if rel_imp[key][i][1] > 0.5 and weight[key][i][1] > 10:
                             
                            iso_constraint[key][i][1] = iso_constraint[key][i][1]
                             
                        else:
                             
                            iso_constraint[key][i][1] -= step_size[4]
                    
                    else:
                        
                        if diff_result[key] < 1-theshold:
                            
                            iso_constraint[key][i][1] = iso_effect[key][i][1]
                            
                        else:
                            
                            iso_constraint[key][i][1] = iso_constraint[key][i][1]
                            
                            
        # transfer the updated variable to struct_fun                
        struct_fun = tool.back_struct_fun(colone_path,iso_constraint,ind_loc_strt[2][1],ind_loc_strt[0][1])
        print('The parameters of OARs has been updated!!.........\n')
        for key in iso_constraint.keys():
            print(key,iso_constraint[key])
            
            
            
            
    else:
        
        flag = 3  # indicate this function is not good !
        print('Original parameters\n')
        for key in iso_constraint.keys():
            print(key,iso_constraint[key])
        
        
        
        for key in rel_imp.keys():
            
            for i in range(len(rel_imp[key])):
                
                if rel_imp[key][i][1] > 0.75:
                    
                    if diff_result[key] < 1-theshold:
                        
                        iso_constraint[key][i][1] += rel_imp[key][i][1]*step_size[5]
                        
                    elif diff_result[key] <= 1:
                        
                        iso_constraint[key][i][1] += rel_imp[key][i][1]*step_size[6]
                        
                    else:
                         
                        iso_constraint[key][i][1] -= step_size[7]
                
                else:
                    
                    if diff_result > 1:
                        
                        iso_constraint[key][i][1] -= step_size[7]
                        
                    else:
                        
                        iso_constraint[key][i][1] += rel_imp[key][i][1]*step_size[6]
                        
        # transfer the updated variable to struct_fun                
        struct_fun = tool.back_struct_fun(colone_path,iso_constraint,ind_loc_strt[2][1],ind_loc_strt[0][1]) 
        print('The parameters of target has been underdose!!.........\n')            
        for key in iso_constraint.keys():
            print(key,iso_constraint[key])

     
        
   
    inf['iso_effect'] = iso_effect
    inf['iso_constraint'] = iso_constraint
    inf['weight'] = weight
    inf['rel_imp'] = rel_imp   

    
    return struct_fun,flag,inf