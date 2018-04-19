

Created on Sun Mar 18 12:47:32 2018

author: Paul

def initial():

    inf_parameters = []
    print ('Give some IMRT parameters in advance!!\n')
    weight_target = input('Please give the weight_target: \n')
    weight_OARs = input('Please give the weight_OARs: \n')
    k_se = input('Please give the power law of Serial function: \n')
    k_pa = input('Please give the power law of Parallel function: \n')
    
    inf_parameters.append(float(weight_target))
    inf_parameters.append(float(weight_OARs))
    inf_parameters.append(float(k_se))
    inf_parameters.append(float(k_pa))
    
    return inf_parameters


def prep_name_gene(path,tar_res_nam):
    
    import temp_tool
    dose_criteria = []
    prep_path = path[7]
    prep = temp_tool.read_prep(prep_path)
    prep_name = []
    prep_patriod = []
    Vol_patriod = []
    for item in prep:
        if item[2] != '':
            prep_name.append(item[0])
            
        if item[0] == tar_res_nam[0]:
            
            dose_criteria.append(float(item[1][1:-1])/100)
            dose_criteria.append(float(item[2])/100)
            
        if item[0] == tar_res_nam[2]:
            
            dose_criteria.append(float(item[2])/100)
            
        if item[0] == 'Spinal Cord':
            
            dose_criteria.append(float(item[2])/100)
            
        if item[0] == 'Brain Stem':
            
            dose_criteria.append(float(item[2])/100)
            
        if item[0] == 'PAROTIDS':
            prep_patriod.append(float(item[1][1:]))
            Vol_patriod.append(float(item[2][:-1]))
            
    prep_name.remove('PAROTIDS')        
    prep_name.append('patient')
    dose_criteria.append(prep_patriod)
    dose_criteria.append(Vol_patriod)
    
    
    
    return prep_name,dose_criteria


def write_colone(template,colone_path):
    
    template.append('')        
    s=''.join(template)   
    
    f = open(colone_path,'w+')
    
    f.seek(0)
    
    f.write(s)
    
    f.close()
    
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




def level_organ(prep_name,tar_res_nam):
    
    print ('Level principle：\n')
    print ('if appears patient,level-->0\n')
    print ('if appears stem or cord,level-->1\n')
    print ('if appears eye,nerve,or....,level-->2\n')
    print ('if appears others(patroid...),level-->3\n')
    OARs_nam_level = []
    for item in prep_name:
        if item not in tar_res_nam:
            
            print(str('the OARs: ' + item))
            st = input('Please give this organ a level(label): \n')
            if len(str(st)) !=  1:
                print('it is wrong!')
            else:
                OARs_nam_level.append([item,int(st)])
            
    
    return OARs_nam_level


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
    
    import temp_tool
    
    qp = temp_tool.exist_read_mod(path_qp)
    
    
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
    
    import temp_tool
    
    se = temp_tool.exist_read_mod(path_se)
    
    
    se[4] = '        totalvolume=' + str(Opti_all) + '\n'
    
    se[18] = '        isoconstraint=' + str(Dose) + '\n'
    
    se[-3] = '        weight=' + str(Weight) + '\n'
    
    se[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
    
    se[16] = '        exponent=' + str(Powe_Law) +'\n'
       
    se[-2] = '    !END\n'
    
    return se[:-1]


def modify_pa(path_pa,Ref_dose,Volume,Weight,Powe_Law,Opti_all,Shrink_margin):
    
    import temp_tool
    
    pa = temp_tool.exist_read_mod(path_pa)
    
    pa[13] = '        refdose=' + str(Ref_dose) + '\n'
    
    pa[18] = '        isoconstraint=' + str(Volume) + '\n'
    
    pa[-3] = '        weight=' + str(Weight) + '\n'
    
    pa[16] = '        exponent=' + str(Powe_Law) +'\n'
    
    pa[4] = '        totalvolume=' + str(Opti_all) + '\n'
    
    pa[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
       
    pa[-2] = '    !END\n'
    
    return pa[:-1]

def modify_mxd(path_mxd,Dose,Weight,Opti_all,Shrink_margin):
    
    import temp_tool
    
    mxd = temp_tool.exist_read_mod(path_mxd)
    
    mxd[4] = '        totalvolume=' + str(Opti_all) +'\n'
    
    mxd[9] = '        shrinkmargin=' + str(Shrink_margin) +'\n'
    
    mxd[18] = '        isoconstraint=' + str(Dose) + '\n'
    
    mxd[-3] = '        weight=' + str(Weight) + '\n'
    
    mxd[-2] = '    !END\n'
    
    return mxd[:-1]

def generate_template(path,tar_res_nam,prep_name,OARs_nam_level,dose_criteria,dose_inf):
    
    #%% 预先输入的信息
    template_line = []
    part2 = path[3]
    part3 = path[4]
    part4 = path[5]
    part5 = path[6]

    pa = path[1]
    qp = path[8]
    se = path[10]
    mxd = path[0]
     
    prep_v = dose_criteria[0]
    prep_d = dose_criteria[1]
    prep_d2 = dose_criteria[2]
    prep_cord = dose_criteria[3]
    prep_stem = dose_criteria[4]  
    prep_patriod = dose_criteria[5]
    Vol_patriod = dose_criteria[6]
    
    
    weight_target = dose_inf[0]
    weight_OARs = dose_inf[1]
    k_se = dose_inf[2]
    k_pa = dose_inf[3]
    max_dose = 54
    
    
    import temp_tool
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
    part2 = temp_tool.exist_read_mod(part2)
    part2[-2] = '    conformalavoidance=0\n'
    part2 = part2[:-1]
    

    
    
    length = len(tar_res_nam)
    target = []
    grid = 3

    # 先把靶区剂量给定
    for item in tar_res_nam:
        
        if tar_res_nam.index(item) == length-1:
            # three cost function should be loaded
            part2[1] = '    name=' + item +'\n'      
            qp1 = temp_tool.modify_qp(qp, prep_v, prep_d2, weight_target, 1, 1)
            mxd1 = temp_tool.modify_mxd(mxd, prep_d, weight_OARs, 0, grid)
            mxd2 = temp_tool.modify_mxd(mxd, prep_d2*1.1, weight_OARs, 0, math.ceil(prep_d-prep_d2*1.1))
            
            target = target + part2 + qp1 + mxd1 + mxd2
            target.append('!END\n')
            
            
        else:
            
            part2[1] = '    name=' + item +'\n'  
            qp2 = temp_tool.modify_qp(qp, prep_v, prep_d, weight_target, 1, 1)

            target = target + part2 + qp2
            target.append('!END\n')
        
    # 再给危及器官剂量参数

    OARs = []
    
    for item in OARs_nam_level:
        
        if item[1] == 0:
            # this means this is patient
            part2[1] = '    name=' + item[0] +'\n'
            mxd1 =temp_tool.modify_mxd(mxd, prep_d*1.1, weight_OARs, 1, 0)
            mxd2 = temp_tool.modify_mxd(mxd, prep_d2, weight_OARs, 0, grid)
            se1 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, 2*grid, 0, k_se)
            se2 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, 4*grid, 0, k_se)
            se3 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, 8*grid, 0, k_se)
            OARs =  OARs + part2 + mxd1 + mxd2 + se1 + se2 + se3
            OARs.append('!END\n')
            
        if item[1] == 1:
            if 'PRV' in item[0]:
                if 'Cord' in item[0]:
                    part2[1] = '    name=' + item[0] +'\n'
                    se4 = temp_tool.modify_se(se, prep_cord*0.75, weight_OARs, 0, 1, k_se)
                    OARs = OARs + part2 + se4
                    OARs.append('!END\n')
                else:
                    part2[1] = '    name=' + item[0] +'\n'
                    se4 = temp_tool.modify_se(se, prep_stem*0.75, weight_OARs, 0, 1, k_se)
                    OARs = OARs + part2 + se4
                    OARs.append('!END\n')
                        
            else:
                if 'Cord' in item[0]:
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd1 = temp_tool.modify_mxd(mxd, prep_cord, weight_OARs, 1, 0)
                    OARs = OARs + part2 + mxd1
                    OARs.append('!END\n')
                else:
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd1 = temp_tool.modify_mxd(mxd, prep_stem, weight_OARs, 1, 0)
                    OARs = OARs + part2 + mxd1
                    OARs.append('!END\n')
                
        if item[1] == 2:
            part2[1] = '    name=' + item[0] +'\n'
            mxd1 = temp_tool.modify_mxd(mxd, max_dose, weight_OARs, 1, 0)       
            OARs = OARs + part2 + mxd1
            OARs.append('!END\n')
            
        if item[1] == 3:
            if item[0] == 'PAROTIDS':
                part2[1] = '    name=' + item[0] +'\n'
                se1 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, grid, 0, k_se)
                se2 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, 2*grid, 0, k_se)
                pa1 = temp_tool.modify_pa(pa, prep_patriod[0], Vol_patriod[0], weight_OARs, k_pa, 1, 0)
                pa2 = temp_tool.modify_pa(pa, prep_patriod[1], Vol_patriod[1], weight_OARs, k_pa, 1, 0)
                OARs = OARs + part2 + se1 + se2 + pa1 + pa2
                OARs.append('!END\n')
                    
            
            else:
                part2[1] = '    name=' + item[0] +'\n'
                se1 = temp_tool.modify_se(se, prep_d2*0.75, weight_OARs, grid, 0, k_se)
                OARs = OARs + part2 + se1
                OARs.append('!END\n')
    
    ## 接下来是剂量参数的给出

    part3 = temp_tool.exist_read_mod(part3)
    part3[-2] = '!END\n'
    part4 = temp_tool.exist_read_mod(part4)
    part4[-2] = '!END\n'
    part5 = temp_tool.exist_read_mod(part5)
    

            
    template_line = template_line + part1 + target + OARs + part3[:-1] + part4[:-1] + part5[:-1]      
    print('template has been generated !\n')
    
    return template_line


    
