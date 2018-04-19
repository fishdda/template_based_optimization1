# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 15:35:49 2018

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 13:56:53 2018

@author: EXTHuaXia
"""


def public_execution(path,colone_path):
    
    '''
       This program mainly execute the extract information from template to program
    '''
    
    import tool
    import time
    
    flag = tool.read_flag(path[0])    
        
    while flag == '1':        
        '''
        This time sleep is for Monaco Calculation
        '''
        time.sleep(5)    
        
        flag = tool.read_flag(path[0])      
        
        print ('flag = 1,waiting for Monaco Calculation...\n')      
    
    print ('flag = ' + flag + ', start adjusting optimiation parameters...\n')    
        
    if flag == '0':      
       
       # 先调节shrink margin
       prep_results = tool.genrate_prescription(tool.read_prep(path[1]))
       
       # read the generated template information from .hyp files
       struct,struct_index,line = tool.read_template(colone_path)
       
       # read the name of all the organs 
       str_name_eval = tool.read_str_name(path[3])
     
       # read the DVH statistics from the Monaco TPS
       plan_result =tool.read_results(path[2]) 
    
       # read the results of each optimization iteration
       actu_result,diff_result = tool.actu_diff_results_read(str_name_eval,plan_result,prep_results)


    return struct,struct_index,line,diff_result



def extra_optimization_parameters(line):
    
    import math
#    # read MC settings
#    ext_para_inf = {}
#    
#    for line1 in line:
#        
#        if '!MCVARPERPLAN' in line1:
#            
#            name1 = 'per calculation'
#        
#        else:
#            
#            name2 = 'per control point'
#    
#
#        if '!MCVARIANCE' in line1:
#            
#            line1[name1] = line1[15:20]
    for line1 in line:   
        if '!DOSEGRIDSIZE' in line1:
            grid = math.ceil(float(line1[17:20]))
    
    return grid


#%% Read prescription file (excel)
def read_prep(path):
    """
       output : list. => include (name,dose constraint type,value)
    """
    import csv
    prep = []
    with open(path) as csvfile:  
        readCSV = csv.reader(csvfile, delimiter=',')  
        for row in readCSV:  
            prep.append(row) 

    return prep


def genrate_prescription(prep):
    
    prep_results = {}
    count = 0
    for item in prep: 
        if item[0] == 'frac' or item[0] == 'prep':
            
            count+= 1
    
        else:
            
            if '%' in item[2]:
                
                prep_results[item[0]] = int(item[2][:-1])
            
            else:
                
                prep_results[item[0]] = int(item[2])
  
    return prep_results
#%% Read flag & write flag from flag.txt

def read_flag(path):
    """ 
       output : flag is a str type
    """
    with open(path, "r+") as f:
        line = f.readlines()
    return line[1][-1]

def write_flag(path):
    """
       this function to change flag from 0 to 1
    """    
    f = open(path, "r+")
    line = f.readlines()
    line[1] = 'flag = 1'
    s=''.join(line)   
    f.seek(0)
    f.write(s)
    f.close()

#%% Read results from results.txt stroe dosimetric statistics(prescription)

def actu_diff_results_read(str_name_eval,plan_result,prep_results):
    '''
       output: dict results in each iterations
    '''
    actu_result = {}
    diff_result = {}
    if len(str_name_eval) == len(plan_result):
        for j in range(len(str_name_eval)):
            actu_result[str_name_eval[j]] = plan_result[j] 
    
    for key in prep_results.keys():
        diff_result[key] = round(actu_result[key]/prep_results[key],2)
    
    return actu_result,diff_result


    
def read_results(path):
    """
       This function only read the results saved in .txt files
       output: line is a list of float with different units       
    """
    new_line = []
    
    with open(path, "r+") as f:
        
        line = f.readlines()
    
    for i in range(len(line)):
        
        if line[i][-3:-1] != ' %':    
            
            new_line.append(float(line[i][:-5]))
            
        else:
            
            new_line.append(float(line[i][:-3]))
    
    return new_line

def read_str_name(path):
    """
       This function read the dosimetric criteria, 
       return dosimetric names(list.)
       if one  structure  has different evaluation indexes,
       it can be remarked as 'PTV1','PTV2','PTV3'.....
       
    """
    name = []
    name_stru = {}
    with open(path, "r+") as f:
        line = f.readlines()
    
    # to load the name to list. files
    for i in range(len(line)):
        
        if line[i][:-1] != '':
            
            name.append(line[i][:-1])
        else:
            
            name.append(line[i-1][:-1] + str())
            
            line[i] = line[i-1]
    
    # to remark the structure name
    for s in name:
        
        name_stru[s] = (name.count(s),name.index(s))
    
    for key,values in name_stru.items():
        
        if values[0] != 1:
            for i in range(values[0]):
                name[values[1]+i] = name[values[1]+i] + str(i+1)
    
    return name
    

#%% Read template files and extract dose parameters

def read_template(path):
    '''
    This function :
        1) input .hyp file path
        2) return three variables:
             1. line(list), records all information in .hyp file
             2. struct_index(list), record location of each structure
             3. struct_fun (dict.), records cost funtion, isoconstraint,isoeffect.... in each structure
    Warning this function only suitable for saved template
    '''
    struct = []
    
    struct_fun = {} 
    
    line = []  # store the pointer's location in file
    
    pointer = []
    
    with open(path, "r+") as f:
        
      line1 = f.readline()
      
      line.append(line1)
      
      while line1:
          
        pointer.append(f.tell())  #record the pointer loaction to help write
        
        line1 = f.readline()
        
        line.append(line1)

    # read information in .hyp file      
    # 标记出所有structure所在line中位置
    struct_index = [i for i,a in enumerate(line) if a=='!VOIDEF\n']
    
    dose_engine_index = [i for i,a in enumerate(line) if a=='!DOSE_ENGINES\n']
    
    count = len(struct_index)
    
    
    
    for j in struct_index:
        
        stru_name = line[j+1]
        
        struct.append(stru_name[9:-1])
    
    # list_fun 记录cost function个数和type    
    for index in range(count):
        
        count_fun = 0
        
        list_fun = []
        
        type_cost = ['type=se','type=pa','type=mxd','type=po','type=qp','type=conf','type=o_q','type=u_q','type=u_v','type=o_v']
        
        if index == count-1:
            
            for flag in range(struct_index[index],dose_engine_index[0]):
                
                if line[flag] == '    !COSTFUNCTION\n':
                    
                    count_fun = count_fun + 1
                    
                    list_fun.append([line[flag+1][8:-1],flag+1])
                    
                    # cost functions differ with flag+1
                    if line[flag+1][8:-1] in type_cost:
                        
                        list_fun.append([line[flag+4][8:-1],flag+4])  # 'type = se'
                        list_fun.append([line[flag+6][8:-1],flag+6])  # 'totalvolume = 0'  
                        list_fun.append([line[flag+9][8:-1],flag+9])  # 'multicriterial = 0'
                        list_fun.append([line[flag+10][8:-1],flag+10])  # 'shrinkmargin = 0'
                        list_fun.append([line[flag+13][8:-1],flag+13])  # 'alpha = 0'
                        list_fun.append([line[flag+16][8:-1],flag+16])  # 'refdose = 100'
                        list_fun.append([line[flag+18][8:-1],flag+18])  # 'exponent = 13'
                        list_fun.append([line[flag+19][8:-1],flag+19])  # 'isoconstraint = 15'
                        list_fun.append([line[flag+20][8:-1],flag+20])  # 'isoeffect = 12'
                        list_fun.append([line[flag+23][8:-1],flag+23])  # ''

        else:
            for flag in range(struct_index[index],struct_index[index+1]):
                
                if line[flag] == '    !COSTFUNCTION\n':
                    
                    count_fun = count_fun + 1
                    
                    list_fun.append([line[flag+1][8:-1],flag+1])
                    
                    if line[flag+1][8:-1] in type_cost:
                        
                        list_fun.append([line[flag+4][8:-1],flag+4])
                        list_fun.append([line[flag+6][8:-1],flag+6])
                        list_fun.append([line[flag+9][8:-1],flag+9])
                        list_fun.append([line[flag+10][8:-1],flag+10])
                        list_fun.append([line[flag+13][8:-1],flag+13])
                        list_fun.append([line[flag+16][8:-1],flag+16])
                        list_fun.append([line[flag+18][8:-1],flag+18])
                        list_fun.append([line[flag+19][8:-1],flag+19])
                        list_fun.append([line[flag+20][8:-1],flag+20])
                        list_fun.append([line[flag+23][8:-1],flag+23])
                    
        list_fun.append(count_fun)
        
        struct_fun[struct[index]] = list_fun    

    return struct_fun,struct_index,line
 
#%% extract variable from struct_fun


def extract_struc_fun(struct_fun,loc,start):
    '''
       name: e.g. isoconstraint,
       loc: e.g. location in struct_fun
       start: number start from the str
    '''
    name = {}
    for key in struct_fun.keys():
        name[key] = []
        for n in range(struct_fun[key][-1]):
            name[key].append([struct_fun[key][11*n][0],round(float(struct_fun[key][11*n+loc][0][start:]),2)])
     
    return name







def back_struct_fun(colone_path,name,cost_name,loc):
    '''
       transfer the altered variable to struct_fun
    '''
    import tool
    struct_fun,struct_index,line = tool.read_template(colone_path)
    for key in name.keys():
        for n in range(len(name[key])):
            struct_fun[key][11 * n + loc][0] = cost_name + str(name[key][n][1])

    return struct_fun


#%% write the updated line into .hyp files
    
def write_template(line,path,updated_struct_fun):
    """
        This function input: updated_struct_fun
                      output:
        both updated_struct_fun and flag all be written into files
    """
        
    # write the updated_struct_fun to the line 
    for key in updated_struct_fun:
        
        for value in updated_struct_fun[key]:
            
            if type(value) == list:
                
                line[value[1]] = '        ' + value[0] +'\n'
   
    # write list line to the original file
    s=''.join(line)   
    
    f = open(path,'w+')
    
    f.seek(0)
    
    f.write(s)
    
    f.close()


def exist_read_mod(path):
    
    line = []  # store the pointer's location in file
    
    pointer = []
    
    with open(path, "r+") as f:
        
      line1 = f.readline()
      
      line.append(line1)
      
      while line1:
          
        pointer.append(f.tell())  #record the pointer loaction to help write
        
        line1 = f.readline()
        
        line.append(line1)    
    
    return line





def modify_qp(path_qp,Vol,Dose,Weight,Opti_all,Surf_margin):
    
    import tool
    
    qp = tool.exist_read_mod(path_qp)
    
    
    # 调节权重
    qp[-3] = '        weight=' + str(Weight) + '\n'
    # 调节Opti_all
    qp[4] = '        totalvolume=' + str(Opti_all) + '\n'
    # 调节surfacemargin
    qp[5] = '        sanesurfacedose=' + str(Surf_margin) + '\n'
    # 给百分数体积
    qp[15] = '        refvolume=' + str(Vol) + '\n'
    # 给剂量
    qp[18] = '        isoconstraint=' + str(Dose) + '\n'
    
    qp[-2] = '    !END\n'
    
    return qp[:-1]
    
    
def modify_se(path_se,Dose,Weight,Shrink_margin,Opti_all,Powe_Law):
    
    import tool
    
    se = tool.exist_read_mod(path_se)
    
    
    se[4] = '        totalvolume=' + str(Opti_all) + '\n'
    
    se[18] = '        isoconstraint=' + str(Dose) + '\n'
    
    se[-3] = '        weight=' + str(Weight) + '\n'
    
    se[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
    
    se[16] = '        exponent=' + str(Powe_Law) +'\n'
       
    se[-2] = '    !END\n'
    
    return se[:-1]


def modify_pa(path_pa,Ref_dose,Volume,Weight,Powe_Law,Opti_all,Shrink_margin):
    
    import tool
    
    pa = tool.exist_read_mod(path_pa)
    
    pa[13] = '        refdose=' + str(Ref_dose) + '\n'
    
    pa[18] = '        isoconstraint=' + str(Volume) + '\n'
    
    pa[-3] = '        weight=' + str(Weight) + '\n'
    
    pa[16] = '        exponent=' + str(Powe_Law) +'\n'
    
    pa[4] = '        totalvolume=' + str(Opti_all) + '\n'
    
    pa[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
       
    pa[-2] = '    !END\n'
    
    return pa[:-1]

def modify_mxd(path_mxd,Dose,Weight,Opti_all,Shrink_margin):
    
    import tool
    
    mxd = tool.exist_read_mod(path_mxd)
    
    mxd[4] = '        totalvolume=' + str(Opti_all) +'\n'
    
    mxd[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
    
    mxd[18] = '        isoconstraint=' + str(Dose) + '\n'
    
    mxd[-3] = '        weight=' + str(Weight) + '\n'
    
    mxd[-2] = '    !END\n'
    
    return mxd[:-1]

def generate_template(path,tar_res_nam,prep_name,OARs_nam_level):
    
    #%% 预先输入的信息
    template_line = []
    path_part2 = path[1]
    path_part3 = path[6]
    path_part4 = path[7]
    path_part5 = path[8]

    pa = path[2]
    qp = path[3]
    se = path[4]
    mxd = path[5]
    import tool
    import math
    
   
    #%% 生成part1
    part1 = ['000610b6\n','!LAYERING\n']
    for item in prep_name:
        if item == 'patient':
            part1.append(str('    ' + item + '\n'))       
        else:
            part1.append(str('    ' + item + ':T\n'))
                
    part1.append('!END\n')
    

    
    #%% 生成 part2
    part2 = tool.exist_read_mod(path_part2)
    part2[-2] = '    conformalavoidance=0\n'
    part2 = part2[:-1]
    

    
    
    length = len(tar_res_nam)
    target = []
    prep_v = 0.95
    prep_d = 69.96
    prep_d2 = 50.96
    grid = 3
    prep_stem = 54
    prep_cord = 45
    prep_patriod = [28,48]
    Vol_patriod = [50,30]
    # 先把靶区剂量给定
    for item in tar_res_nam:
        
        if tar_res_nam.index(item) == length-1:
            # three cost function should be loaded
            part2[1] = '    name=' + item +'\n'      
            qp1 = tool.modify_qp(qp, prep_v, prep_d2, 1, 1, 1)
            mxd1 = tool.modify_mxd(mxd, prep_d, 0.01, 0, grid)
            mxd2 = tool.modify_mxd(mxd, prep_d2*1.1, 0.01, 0, math.ceil(prep_d-prep_d2*1.1))
            
            target = target + part2 + qp1 + mxd1 + mxd2
            target.append('!END\n')
            
            
        else:
            
            part2[1] = '    name=' + item +'\n'  
            qp2 = tool.modify_qp(qp, prep_v, prep_d, 1, 1, 1)

            target = target + part2 + qp2
            target.append('!END\n')
        
    # 再给危及器官剂量参数

    OARs = []
    
    for item in OARs_nam_level:
        
        if item[1] == 0:
            # this means this is patient
            part2[1] = '    name=' + item[0] +'\n'
            mxd1 =tool.modify_mxd(mxd, prep_d*1.1, 0.01, 1,0)
            mxd2 = tool.modify_mxd(mxd, prep_d2, 0.01, 0, grid)
            se1 = tool.modify_se(se, prep_d2*0.75, 0.01, 2*grid, 0, 12)
            se2 = tool.modify_se(se, prep_d2*0.75, 0.01, 4*grid, 0, 12)
            se3 = tool.modify_se(se, prep_d2*0.75, 0.01, 8*grid, 0, 12)
            OARs =  OARs + part2 + mxd1 + mxd2 + se1 + se2 + se3
            OARs.append('!END\n')
            
        if item[1] == 1:
            if 'PRV' in item[0]:
                if 'Cord' in item[0]:
                    part2[1] = '    name=' + item[0] +'\n'
                    se4 = tool.modify_se(se, prep_cord*0.75, 0.01, 0, 1, 12)
                    OARs = OARs + part2 + se4
                    OARs.append('!END\n')
                else:
                    part2[1] = '    name=' + item[0] +'\n'
                    se4 = tool.modify_se(se, prep_stem*0.75, 0.01, 0, 1, 12)
                    OARs = OARs + part2 + se4
                    OARs.append('!END\n')
                        
            else:
                if 'Cord' in item[0]:
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd1 = tool.modify_mxd(mxd, prep_cord, 0.01, 1, 0)
                    OARs = OARs + part2 + mxd1
                    OARs.append('!END\n')
                else:
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd1 = tool.modify_mxd(mxd, prep_stem, 0.01, 1, 0)
                    OARs = OARs + part2 + mxd1
                    OARs.append('!END\n')
                
        if item[1] == 2:
            part2[1] = '    name=' + item[0] +'\n'
            mxd1 = tool.modify_mxd(mxd, prep_d2, 0.01, 1, 0)       
            OARs = OARs + part2 + mxd1
            OARs.append('!END\n')
            
        if item[1] == 3:
            if item[0] == 'PAROTIDS':
                part2[1] = '    name=' + item[0] +'\n'
                se1 = tool.modify_se(se, prep_d2*0.75, 0.01, grid, 0, 12)
                se2 = tool.modify_se(se, prep_d2*0.75, 0.01, 2*grid, 0, 12)
                pa1 = tool.modify_pa(pa, prep_patriod[0], Vol_patriod[0], 0.01, grid, 1, 0)
                pa2 = tool.modify_pa(pa, prep_patriod[1], Vol_patriod[1], 0.01, grid, 1, 0)
                OARs = OARs + part2 + se1 + se2 + pa1 + pa2
                OARs.append('!END\n')
                    
            
            else:
                part2[1] = '    name=' + item[0] +'\n'
                se1 = tool.modify_se(se, prep_d2*0.75, 0.01, grid, 0, 12)
                OARs = OARs + part2 + se1
                OARs.append('!END\n')
    
    ## 接下来是剂量参数的给出

    part3 = tool.exist_read_mod(path_part3)
    part3[-2] = '!END\n'
    part4 = tool.exist_read_mod(path_part4)
    part4[-2] = '!END\n'
    part5 = tool.exist_read_mod(path_part5)
    

            
    template_line = template_line + part1 + target + OARs + part3[:-1] + part4[:-1] + part5[:-1]      
    print('template has been generated !\n')
    
    return template_line





def level_organ(prep_name,tar_res_nam):
    
    print ('Level 规则：\n')
    print ('if appears patient,level: 0\n')
    print ('if appears stem or cord,level: 1\n')
    print ('if appears 视觉系统,level: 2\n')
    print ('if appears 其他(patroid...),level: 3\n')
    OARs_nam_level = []
    for item in prep_name:
        if item not in tar_res_nam:
            
            print('the OARs: ', item, '\n')
            st = input('请给这个器官打上level标签: \n')
            if len(st) !=  1:
                print('it is wrong!')
            else:
                OARs_nam_level.append([item,int(st)])
            
    
    return OARs_nam_level


def run_generate_template(cur_path,path_tem,colone_path,tar_res_nam):
     
    import  tool
    prep_path = path_tem[0]
    prep = tool.read_prep(prep_path)
    prep_name = []
    for item in prep:
        if item[2] != '':
            prep_name.append(item[0])
    prep_name.append('patient')
       
    
    OARs_nam_level=tool.level_organ(prep_name,tar_res_nam)
            
    template = tool.generate_template(path_tem,tar_res_nam,prep_name,OARs_nam_level)
    template[-1] = '!ISPHANTOMMATERIAL    0\n'
    
    
    template.append('')        
    s=''.join(template)   
    
    f = open(colone_path,'w+')
    
    f.seek(0)
    
    f.write(s)
    
    f.close()
    
def save_results(cur_path,inf_iter,diff_iter):
    
    import pandas as pd
    
    weight_iter = {}
    iso_constraint_iter = {}
    iso_effect_iter = {}
    relative_impact_iter = {}
    for key in inf_iter.keys():
        weight_iter[key] = inf_iter[key]['weight']
        iso_constraint_iter[key] = inf_iter[key]['iso_constraint']
        iso_effect_iter[key] = inf_iter[key]['iso_effect']
        relative_impact_iter[key] = inf_iter[key]['rel_imp']
    
    weight_iter = pd.DataFrame(weight_iter)
    iso_constraint_iter = pd.DataFrame(iso_constraint_iter)
    iso_effect_iter = pd.DataFrame(iso_effect_iter)
    relative_impact_iter = pd.DataFrame(relative_impact_iter)
    diff_iter = pd.DataFrame(diff_iter)
    
    
    kk = []
    cols1 = []
    cols = list(diff_iter)

    for item in cols:
        kk.append(int(item[9:]))
        
    kk.sort()
    
    for i in kk:
        cols1.append('iteration'+str(i))
    
    
    
    diff_iter = diff_iter.ix[:,cols1]
    weight_iter = weight_iter.ix[:,cols1]
    iso_constraint_iter = iso_constraint_iter.ix[:,cols1]
    iso_effect_iter = iso_effect_iter.ix[:,cols1]
    relative_impact_iter = relative_impact_iter.ix[:,cols1]
    diff_iter.to_csv(cur_path + '\\result\\diff_iter.csv')
    weight_iter.to_csv(cur_path + '\\result\\weight_iter.csv')
    iso_constraint_iter.to_csv(cur_path + '\\result\\iso_constraint_iter.csv')
    iso_effect_iter.to_csv(cur_path + '\\result\\iso_effect_iter.csv')
    relative_impact_iter.to_csv(cur_path + '\\result\\relative_impact_iter.csv')
    
    return diff_iter,weight_iter,iso_constraint_iter,iso_effect_iter,relative_impact_iter
    
    
def plot(path):
    import pandas as pd
    import matplotlib.pyplot as plt

    
    
    # 读入数据
    data = pd.read_csv(path + '\\result\\diff_iter.csv')
#    isoconstraint = pd.read_csv(path + '\\iso_constraint_iter.csv')
#    isoeffect = pd.read_csv(path + '\\iso_effect_iter.csv')
#    weight = pd.read_csv(path + '\\weight_iter.csv')
#    rel_imp = pd.read_csv(path + '\\relative_impact_iter.csv')
    data.head()
    
    
    # 看看数据维度，并清洗数据
    data.shape
    col = data.columns
    d = data[col[0]]
    dat = data.T
    dat = dat[1:]
    ss = []
    for i in d:
        ss.append(i)
        
    dat.columns = ss
    
    # 去掉Neck器官
    del dat['Neck']
    kk = dat.columns
    mm = dat[kk[0:-1]]
    
    
    # 画出图像
    fig = plt.figure()
    mm.plot(subplots=True, layout=(5, 6), figsize=(18,18), sharex=False)
    plt.legend(loc='best')
    plt.show()
    fig.savefig(path + '\\result\\iteration.png', dpi=fig.dpi)   
    
    
    
    
    
    
    
    
    
    
        #OARs_nam = list(set(prep_name).difference(set(tar_res_nam)))
    #OARs_nam = prep_name[3:]
    ### 增加一个函数让物理师打标签
    #OARs_nam_level = []
    #for i in OARs_nam:
    #    if i in ['patient']:
    #        OARs_nam_level.append([i,0])
    #    if i in ['Spinal Cord','Cord PRV','Brain Stem','Stem PRV']:
    #        OARs_nam_level.append([i,1])
    #    if i in ['Len L','Len R','Optic Chiasm','Optic Nerve L',
    #             'Optic Nerve R','Pituitary','TMJ-L','TMJ-R','Inner Ears']:
    #        OARs_nam_level.append([i,2])
    #    if i in ['Neck','Larynx','Oral Cavity','Mandible','Thyroid','Trachea',
    #             'Esophagus','PAROTIDS']:
    #        OARs_nam_level.append([i,3])
    
    
    
        #%% 检测template生成的是不是对
    #hyp_path = 'C:/Users/Shelter6/Desktop/project/template_and_results1/RTOG0615NPCnew.hyp'
    
    
    #struct_fun,struct_index,line = tool.read_template(hyp_path)
    #for i,j in zip(line[:-1],template):
    #    if i[-1] != j[-1] :
    #        print((i,j))
    #        print((line[:-1].index(i),template.index(j)))
    
  
    