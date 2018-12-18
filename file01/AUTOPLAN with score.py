class Temp:
    '''
       this class mainly intended to generate a template automatically
       
    '''
    
    def  __init__(self,path,csv_file,colone_path):
        
        self.path = path
        self.csv = csv_file
        self.col = colone_path
        
    def exist_read_mod(self,path1):
    
        self.line = []  # store the pointer's location in file
        
        with open(path1, "r+",errors = 'ignore') as f:
            
          line1 = f.readline()
          
          self.line.append(line1)
          
          while line1:
              
    #        pointer.append(f.tell())  #record the pointer loaction to help write
            
            line1 = f.readline()
            
            self.line.append(line1)    
        
        return self.line
        
    def classify(self,strt_ind_list):
        
        self.level_OARs = {}
        for item in strt_ind_list:
            if item[2] > 2 and item[2] < 7:
                self.level_OARs[item[0]] = 1
            elif item[2] > 6 and item[2] < 16:
                self.level_OARs[item[0]] = 2
            elif item[2] == 16:
                self.level_OARs[item[0]] = 3
            elif item[2] > 16 and item[2] < 24:
                self.level_OARs[item[0]] = 3
        return self.level_OARs
    
    def modify_qp(self,qp,Vol,Dose,Weight,Opti_all,Surf_margin):
        
        self.qp = qp
        self.qp[15] = ''.join(['        refvolume=',str(Vol),'\n'])
        self.qp[18] = ''.join(['        isoconstraint=',str(Dose),'\n'])
        self.qp[-3] = ''.join(['        weight=',str(Weight),'\n'])
        self.qp[4] = ''.join(['        totalvolume=',str(Opti_all),'\n'])
        self.qp[5] = ''.join(['        sanesurfacedose=',str(Surf_margin),'\n'])      
        self.qp[-2] = ''.join(['    !END\n'])
        
        return self.qp[:-1]
    
    def modify_po(self,po,Dose,alpha):
        
        self.po = po
        self.po[18] = ''.join(['        isoconstraint=',str(Dose),'\n'])
        self.po[10] = ''.join(['        alpha=',str(alpha),'\n'])
        self.po[-2] = ''.join(['    !END\n'])
        
        return self.po[:-1]    
    
    
    def modify_se(self,se,Dose,Weight,Shrink_margin,Opti_all,Powe_Law):
    
        self.se = se 
        self.se[18] = ''.join(['        isoconstraint=',str(Dose),'\n'])
        self.se[-3] = ''.join(['        weight=',str(Weight),'\n'])
        self.se[9] = ''.join(['        shrinkmargin=',str(Shrink_margin),'\n'])
        self.se[4] = ''.join(['        totalvolume=',str(Opti_all),'\n'])        
        self.se[16] = ''.join(['        exponent=',str(Powe_Law),'\n'])
        self.se[-2] = ''.join(['    !END\n'])
        
        return self.se[:-1]


    def modify_pa(self,pa,Ref_dose,Volume,Weight,Powe_Law,Opti_all,Shrink_margin):

        self.pa = pa
        self.pa[13] = ''.join(['        refdose=',str(Ref_dose),'\n'])      
        self.pa[18] = ''.join(['        isoconstraint=',str(Volume),'\n'])       
        self.pa[-3] = ''.join(['        weight=',str(Weight),'\n'])
        self.pa[16] = ''.join(['        exponent=',str(Powe_Law),'\n'])        
        self.pa[4] = ''.join(['        totalvolume=',str(Opti_all),'\n'])        
        self.pa[9] = ''.join(['        shrinkmargin=',str(Shrink_margin),'\n'])           
        self.pa[-2] = ''.join(['    !END\n'])
        
        return self.pa[:-1]

    def modify_mxd(self,mxd,Dose,Weight,Opti_all,Shrink_margin):
        
        self.mxd = mxd
        self.mxd[18] = ''.join(['        isoconstraint=',str(Dose),'\n' ])       
        self.mxd[-3] = ''.join(['        weight=',str(Weight),'\n'])
        self.mxd[4] = ''.join(['        totalvolume=',str(Opti_all),'\n' ])      
        self.mxd[9] = ''.join(['        shrinkmargin=',str(Shrink_margin),'\n'])        
        self.mxd[-2] = ''.join(['    !END\n'])
        
        return self.mxd[:-1]

    def modify_qod(self,qod,Dose,RMS,Shrink_margin):

        self.qod = qod
        self.qod[17] = ''.join(['        thresholddose=',str(Dose),'\n']) 
        self.qod[18] = ''.join(['        isoconstraint=',str(RMS),'\n']) 
        self.qod[9] = ''.join(['        shrinkmargin=',str(Shrink_margin),'\n'  ])   
        self.qod[-2] = ''.join(['    !END\n']) 
        
        return self.qod[:-1]

    def read_struct(self,structure):
        '''
           This function output a list of structure name from struct.dcm file
        '''
        self.contours = []
        for i in range(len(structure.ROIContourSequence)):
            self.contour = {}
            self.contour['color'] = structure.ROIContourSequence[i].ROIDisplayColor
            self.contour['number'] = structure.ROIContourSequence[i].ReferencedROINumber
            self.contour['name'] = structure.StructureSetROISequence[i].ROIName
            assert self.contour['number'] == structure.StructureSetROISequence[i].ROINumber
            self.contour['contours'] = [s.ContourData for s in structure.ROIContourSequence[i].ContourSequence]
            self.contours.append(self.contour)
        
        return self.contours


    def read_csv(self):
        
        self.pres_strt,self.dose_frac = [],[]
        self.pres_strt_ind = {} # initialization
        
        import csv
        with open(self.csv) as csvfile:  
            readCSV = csv.reader(csvfile, delimiter=',')  
            prep = [row for row in readCSV]  
        
        self.pres_strt = list(set([l[0] for l in prep if l[0] != 'prep' and l[0] != 'frac' ]))
        
        self.dose_frac = [l for l in prep if l[0] == 'prep' or l[0] == 'frac' ]
        
        for item in self.pres_strt: self.pres_strt_ind[item] = [] # initialization
        
        for item in prep:
            
            if item[0] != 'prep' and item[0] != 'frac':
                
                if item[2][-1] != '%':
                    
                    self.pres_strt_ind[item[0]].append((item[1],float(item[2])/100))
                    
                else:
                    
                    self.pres_strt_ind[item[0]].append((item[1],float(item[2][:-1])))
    
        
        return self.pres_strt,self.dose_frac,self.pres_strt_ind

    def write_colone(self,template):
        
        template.append('')        
        s=''.join(template)          
        f = open(self.col,'w+')        
        f.seek(0)        
        f.write(s)        
        f.close()


    def cf_OAR(self,path_new,OBJ):
        '''
        this function is aimed to convert the item to 
        most helpful one
        '''
        import re
        weight_OARs = 0.01
        k_se = 12
        k_pa = 3

        self.cost_fun = []
        for i,j in enumerate(OBJ[1]):
            
            if j[0][0] == 'D':
                       
                if j[0] == 'Dmean':
                    
                    se = self.modify_se(path_new['se'], j[1], weight_OARs, 0, 0, 1)        
                    self.cost_fun.extend(se)
                    
                elif j[0] == 'Dmax':
                    
                    mxd =self.modify_mxd(path_new['mxd'], j[1], weight_OARs, 0, 0)
                    self.cost_fun.extend(mxd)
                
                else:
                    
                    se = self.modify_se(path_new['se'], j[1]*0.75, weight_OARs, 0, 0, 16)
                    self.cost_fun.extend(se)
                
            
                
            elif j[0][0] == 'V' :
                
                ss = (re.findall("\d+", j[0]))
                s = float(ss[0])
                flag = j[1]
                
                if flag <= 15.0:               
                    se = self.modify_se(path_new['se'], s*0.75, weight_OARs, 3, 0, k_se)
                    self.cost_fun.extend(se)
                else:
                    pa = self.modify_pa(path_new['pa'], s, flag, weight_OARs, k_pa, 0, 0)
                    self.cost_fun.extend(pa)  
    
        return self.cost_fun


    def ge_tem_pros(self,strt_ind_list,path_beam,dose_frac):
    
        import math
        self.template_line = []
        grid = 3
        tar = [(item[0],item[1],float(item[1][0][0][1:])) for item in strt_ind_list if 'PTV' in item[0] or 'PGTV' in item[0] or 'GTV' in item[0]]
        tar.sort(key=lambda x:x[2],reverse = True)
        tar_nam = [item[0] for item in tar]
        
        
        OARs_nam = [item[0] for item in strt_ind_list if item[0] not in tar_nam]
        prep_name = []
        prep_name = prep_name + tar_nam + OARs_nam
        ##tar_res_nam = [item[0] for item in OARs_nam_level if 'PTV' in item[0] or 'PGTV' in item[0]] 
           

        ind = self.path[0].rindex('\\')
        path_new = {}
        for item in self.path:
            path_new[item[int(ind+1):-4]] = self.exist_read_mod(item)
        
        
        pres = float(dose_frac[1][1])/100
        weight_target = 1
        weight_OARs = 0.01
        k_se = 12
        k_pa = 3
        RMS = 1
        max_dose = 47.5
        ## ================== part1 ================= ##
        part1 = ['000610b6\n','!LAYERING\n']
        for item in prep_name:
            if item == 'patient' or item == 'BODY':
                part1.append(str('    ' + item + '\n'))       
            else:
                part1.append(str('    ' + item + ':T\n'))
                    
        part1.append('!END\n')
         
        ## ==================  part2 ================ ##    
        part2 = path_new['part2']  ## read template
        part2[-2] = '    conformalavoidance=0\n'
        part2 = part2[:-1]
        target = []
        OARs = []   
        
        for i,item in enumerate(tar):
            
            if i != len(tar)-1:  ## inner target 1
                
                part2[1] = '    name=' + item[0] +'\n' 
#                prep_v = float((item[1][0][1]+3)/100)
                prep_d = float(item[1][0][0][1:])
                tar_pen = self.modify_po(path_new['po'],prep_d,0.6)
                qod = self.modify_qod(path_new['qod'],prep_d+2,RMS,0)
                target = target + part2 + tar_pen + qod
                target.append('!END\n')
                
            else:   ## external target
                
                part2[1] = '    name=' + item[0] +'\n'    
#                prep_v = float((item[1][0][1]+3)/100)
                prep_d = float(item[1][0][0][1:])
                po = self.modify_po(path_new['po'],prep_d,0.6)
                
                ## set two quadratic overdose to external targets
                qod1 = self.modify_qod(path_new['qod'],pres,RMS,0)
    #            QOD2 = temp_tool.modify_QOD(QOD_path,prep_d-4,RMS1,grid)
                qod2 = self.modify_qod(path_new['qod'],prep_d*1.1,RMS,grid*math.floor(abs(prep_d*1.1-pres)/grid))
                
                target = target + part2 + po +qod1 + qod2
                target.append('!END\n')
    
        for item in strt_ind_list:
            
            if item[0] not in tar_nam:
                            
                if item[-1] == 5: ##　stem and cord
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    cf1 = self.cf_OAR(path_new,item)
                    OARs = OARs + part2 + cf1
                    OARs.append('!END\n')                           
                                                      
                elif item[-1] == 6: ##  normal tissues
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    cf2 = self.cf_OAR(path_new,item)
                    OARs = OARs + part2 + cf2
                    OARs.append('!END\n')      
                elif item[-1] == 7: ##  normal tissues
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    cf3 = self.cf_OAR(path_new,item)
                    OARs = OARs + part2 + cf3
                    OARs.append('!END\n')        
                    
                elif item[-1] == 8: ##  normal tissues
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    cf4 = self.cf_OAR(path_new,item)
                    OARs = OARs + part2 + cf4
                    OARs.append('!END\n')     
                
                elif item[-1] == 9: ##  normal tissues
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    cf5 = self.cf_OAR(path_new,item)
                    OARs = OARs + part2 + cf5
                    OARs.append('!END\n')    
                
                
                elif item[-1] == 100: ## patient
                
                    part2[1] = '    name=' + item[0] +'\n'
                    ## global maximum dose
                    mxd1 = self.modify_mxd(path_new['mxd'], round(pres*1.06,2), weight_OARs, 1, 0)
                    ## the outer target dose
                    QOD1 = self.modify_qod(path_new['qod'],max_dose,RMS,grid*0)
                    QOD2 = self.modify_qod(path_new['qod'],max_dose*0.8,RMS/2,grid*math.floor((max_dose*0.2)/grid))
                    QOD3 = self.modify_qod(path_new['qod'],max_dose*0.6,RMS/2,grid*math.floor((max_dose*0.4)/grid))
                    OARs = OARs + part2 + mxd1 + QOD1 + QOD2 + QOD3
                    OARs.append('!END\n')
            
        
        ## ================== part3 ================ ##
        part3 = path_new['part3']
        part3[-2] = '!END\n'
        
        ## ================== part4 ================ ##
        part4 = self.exist_read_mod(path_beam)
        part4[-2] = '!END\n'
        
        ## ================== part5 ================ ##
        part5 = path_new['part5']
        for i,item in enumerate(part5):
            if 'FRACTIONS' in item:
                part5[i] = ''.join(['!FRACTIONS    ',dose_frac[0][1],'\n'])
            elif 'PRESCRIPTION' in item:
                part5[i] = ''.join(['!PRESCRIPTION    ',str(float(dose_frac[1][1])/100),'\n'])
        
        ## ================== template ==================== ##        
        self.template_line = self.template_line + part1 + target + OARs + part3[:-1] + part4[:-1] + part5[:-1]      
        print('###############################')
        print('template has been generated !')
        print('###############################')
        return self.template_line


    def ge_tem_HN(self,strt_ind_list,path_beam,dose_frac):
        '''
           This function generate an initial .hyp template for optimization
           
           path:
           tar_res_nam:
           prep_name:
           OARs_nam_level: 这个必须是排好序的器官名称
           dose_criteria:
           dose_inf:
        '''
        import math
        grid = 3
        self.template_line = []
        prep_name = [item[0] for item in strt_ind_list]
        ##tar_res_nam = [item[0] for item in OARs_nam_level if 'PTV' in item[0] or 'PGTV' in item[0]] # 寻找靶区的名字
        
        ind = self.path[0].rindex('\\')
        path_new = {}
        for item in self.path:
            path_new[item[int(ind+1):-4]] = self.exist_read_mod(item)
        
        pres = float(dose_frac[1][1])/100
        prep_d2 = 50.96
        prep_cord =40
        prep_stem = 50 
        prep_patriod = [50,50]
        Vol_patriod = [60,30]
        prep_v = 0.98  ## 98% == 0.98
        weight_target = 1
        weight_OARs = 0.01
        k_se = 12
        k_pa = 3
        max_dose = 54  ## 视觉系统的限制条件
        len_max = 9 ## 视觉系统的len特殊照顾
        RMS0 = 0.5
        RMS1 = 1
        ## ================== 生成part1 ================= ##
        part1 = ['000610b6\n','!LAYERING\n']
        for item in prep_name:
            if item == 'patient' or item == 'BODY':
                part1.append(str('    ' + item + '\n'))       
            else:
                part1.append(str('    ' + item + ':T\n'))
                    
        part1.append('!END\n')
        ## ============================================== ##

        ## ================== 生成 part2 ================ ##
    
        part2 = path_new['part2']  ## 读取一个模板进来
        part2[-2] = '    conformalavoidance=0\n'
        part2 = part2[:-1]
        target = []
        OARs = []
        
        
        for item in strt_ind_list:
            
            if 'PGTV' in item[0]:  ## 内靶区
                
                part2[1] = ''.join(['    name=',item[0],'\n']) 
                tar_pen = self.modify_qp(path_new['qp'], prep_v, pres, weight_target, 0, 1)
                QOD = self.modify_qod(path_new['qod'],pres+1,RMS1,0)
                target = target + part2 + tar_pen + QOD
                target.append('!END\n')
                
            if 'PTV' in item[0]:   ## 外靶区
                
                part2[1] = '    name=' + item[0] +'\n' 
                qp = self.modify_qp(path_new['qp'], prep_v, prep_d2, weight_target, 0, 1)
                QOD1 = self.modify_qod(path_new['qod'],pres,RMS0,0)
    #            QOD2 = temp_tool.modify_qod(QOD_path,prep_d-4,RMS1,grid)
                QOD2 = self.modify_qod(path_new['qod'],prep_d2*1.1,RMS1+0.5,math.floor((pres-prep_d2*1.1)/3)*3)
                target = target + part2 + qp + QOD1 + QOD2
                target.append('!END\n')
                
            if item[2] == 5 or item[2] == 6:##　stem or stem prv
               
               if 'PRV' in item[0]: ## stem PRV
                   
                   part2[1] = '    name=' + item[0] +'\n'
                   se = self.modify_se(path_new['se'], prep_stem*0.75, weight_OARs, 0, 0, k_se)
                   OARs = OARs + part2 + se
                   OARs.append('!END\n')
                   
                   
               else:
                   ## stem 
                   
                   part2[1] = '    name=' + item[0] +'\n'
                   mxd = self.modify_mxd(path_new['mxd'], prep_stem, weight_OARs, 0, 0)
                   OARs = OARs + part2 + mxd
                   OARs.append('!END\n')
                 
            
            if item[2] == 3 or item[2] == 4: ##  cord or cord prv
                
               if 'PRV' in item[0]:
                   
                   part2[1] = '    name=' + item[0] +'\n'
                   se = self.modify_se(path_new['se'], prep_cord*0.75, weight_OARs, 0, 0, k_se)
                   OARs = OARs + part2 + se
                   OARs.append('!END\n')
                   
               else:
                   
                   part2[1] = '    name=' + item[0] +'\n'
                   mxd = self.modify_mxd(path_new['mxd'], prep_cord, weight_OARs, 0, 0)
                   OARs = OARs + part2 + mxd
                   OARs.append('!END\n')
                   
            
            
            if item[2] > 6 and item[2] < 16: ## optical system
                
                if 'len' in item[0] or 'Len' in item[0] or 'LEN' in item[0]:
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd = self.modify_mxd(path_new['mxd'], len_max, weight_OARs, 0, 0)       
                    OARs = OARs + part2 + mxd
                    OARs.append('!END\n')
                    
                else:
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    mxd = self.modify_mxd(path_new['mxd'], max_dose, weight_OARs, 0, 0)       
                    OARs = OARs + part2 + mxd
                    OARs.append('!END\n')
    
            
            if item[2] > 15 and item[2] < 24: ## parotid or other
                
                if item[0].upper() == 'PAROTIDS' or item[0].upper() == 'PAROTID ALL':
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    se1 = self.modify_se(path_new['se'], prep_d2*0.75, weight_OARs, grid, 0, k_se)
    #                se2 = self.modify_se(se_path, prep_d2*0.75, weight_OARs, 2*grid, 0, k_se)
                    pa1 = self.modify_pa(path_new['pa'], prep_patriod[1], Vol_patriod[1], weight_OARs, k_pa, 0, 0)
    #                pa2 = self.modify_pa(pa_path, prep_patriod[1], Vol_patriod[1], weight_OARs, k_pa, 1, 0)
                    OARs = OARs + part2 + se1 + pa1
                    OARs.append('!END\n')
                
                elif item[0] == 'Thyroid' or item[0].upper() == 'THYROID':
                   
                    part2[1] = '    name=' + item[0] +'\n'
                    se1 = self.modify_se(path_new['se'], prep_d2*0.75, weight_OARs, grid, 0, k_se)
    #                se2 = self.modify_se(se_path, prep_d2*0.75, weight_OARs, 2*grid, 0, k_se)
                    pa1 = self.modify_pa(path_new['pa'], prep_patriod[0], Vol_patriod[0], weight_OARs, k_pa, 0, 0)
    #                pa2 = self.modify_pa(pa_path, prep_patriod[1], Vol_patriod[1], weight_OARs, k_pa, 1, 0)
                    OARs = OARs + part2 + se1 + pa1
                    OARs.append('!END\n')
                                 
                else:
                    
                    part2[1] = '    name=' + item[0] +'\n'
                    se = self.modify_se(path_new['se'], prep_d2*0.75, weight_OARs, grid, 0, k_se)
                    OARs = OARs + part2 + se
                    OARs.append('!END\n')
            
            if item[2] == 24: ## patient
            
                part2[1] = '    name=' + item[0] +'\n'
                mxd1 =self.modify_mxd(path_new['mxd'], round(pres*1.075,0), weight_OARs, 1, 0)
    #            mxd2 = self.modify_mxd(mxd_path, prep_d2, weight_OARs, 0, grid)
    #            se1 = self.modify_se(se_path, prep_d2*0.75, weight_OARs, 2*grid, 0, k_se)
    #            se2 = temp_tool.modify_se(se_path, prep_d2*0.75, weight_OARs, 4*grid, 0, k_se)
    #            se3 = temp_tool.modify_se(se_path, prep_d2*0.75, weight_OARs, 8*grid, 0, k_se)
                QOD1 = self.modify_qod(path_new['qod'],prep_d2,RMS1,grid*0)
                QOD2 = self.modify_qod(path_new['qod'],prep_d2*0.8,RMS1,grid*math.floor((prep_d2*0.2)/grid))
                QOD3 = self.modify_qod(path_new['qod'],prep_d2*0.6,RMS1,grid*math.floor((prep_d2*0.4)/grid))
                OARs = OARs + part2 + mxd1 + QOD1 + QOD2 +QOD3
                OARs.append('!END\n')
            
        
        ## ================== part3 ================ ##
        part3 = path_new['part3']
        part3[-2] = '!END\n'
        
        ## ================== part4 ================ ##
        part4 = self.exist_read_mod(path_beam)
        part4[-2] = '!END\n'
        
        ## ================== part5 ================ ##
        part5 = path_new['part5']
        for i,item in enumerate(part5):
            if 'FRACTIONS' in item:
                part5[i] = ''.join(['!FRACTIONS    ',dose_frac[0][1],'\n'])
            elif 'PRESCRIPTION' in item:
                part5[i] = ''.join(['!PRESCRIPTION    ',str(float(dose_frac[1][1])/100),'\n'])
                
    
        
        ## ================== 生成总的template ==================== ##        
        self.template_line = self.template_line + part1 + target + OARs + part3[:-1] + part4[:-1] + part5[:-1]      
        print('###############################')
        print('template has been generated !')
        print('###############################')
        return self.template_line
    
    def initial(self,struct,struct_set,path_beam,selection):
    
        ## ============ Read struct file =========== ##
        contours = self.read_struct(struct)
        stru_name = [item['name'] for item in contours]
        pres_name,dose_frac,strt_index = self.read_csv()
        ## ============ Read CSV file ============== ##
        
        
        ## if pres_name in stru_name
        Err = []
        self.tras = {}
        for item in pres_name:
            if item not in stru_name:
                print('Name Error: {}'.format(item))
                Err.append(item)
        print('This means this name is not in the struct_name.\n')
        for item in stru_name:
            print('the name in strut_set were: {}'.format(item))
        stat = input('Do you want to change the name? if Yes enter 1 & No enter 0\n')
        if stat == '1':
            for item in Err:
                print('Original one:{}'.format(item))
                ss = input('new one:')
                self.tras[item] = ss
        else:
            pass
        
        for item in strt_index.keys():
            
            if item in Err:
                strt_index[self.tras[item]] = strt_index[item]
                del strt_index[item]
        
        self.strt_ind_list = []
        ## solve the order issue
        for key in strt_index.keys():
            if key in struct_set.keys():
                self.strt_ind_list.append((key,strt_index[key],struct_set[key]))
                
        for item in stru_name:
            if item == 'Body' or item == 'patient' or item == 'BODY':
                self.strt_ind_list.append((item,'',struct_set[item]))
        
        self.strt_ind_list.sort(key=lambda x:x[2])   
        if selection == '1':
            ## this indicate the prostate
            template = self.ge_tem_pros(self.strt_ind_list,path_beam,dose_frac)
            
        else:
            
            template = self.ge_tem_HN(self.strt_ind_list,path_beam,dose_frac)
        
        template[-1] = '!ISPHANTOMMATERIAL    0\n' 
        
        self.write_colone(template)
        
        return self.strt_ind_list,self.tras
#def extract(X,path_struct_set):
#    
#    stru_name = []
#    for p in path_struct_set:
#        structure= pydicom.read_file(p,force=True)
#        contours = X.read_struct(structure)
#        for item in contours:
#            stru_name.append(item['name']) 
#    
#    stru_name = list(set(stru_name))
#    struct_set = {}
#    for item in stru_name:
#        if 'CTV' in item:
#            struct_set[item] = 0
#        elif 'PTV' in item:
#            struct_set[item] = 1
#        else:
#            struct_set[item] = 2
#            
#    return struct_set
class Tool:
    ''' 
       we need to build this Tool for optimization
    '''
    def __init__(self,path,ind_loc_strt,iter_path):
        self.path = path
        self.ind = ind_loc_strt
        self.iter_path = iter_path
        self.dvh_name = ''
  
    def read_dvh(self):
        
        with open(self.path[2][2], "r+") as f:
            line = f.readlines()
            
        for i in line[1]:
            if i == '=':
                k = line[1].index(i)
                
        self.dvh_name = line[1][k+2:]
        return self.dvh_name
    
    def write_dvh(self,new_name):
        """
           this function to change dvh_name
        """    
        f = open(self.path[2][2], "r+")
        
        line = f.readlines()
        
        line[1] = ''.join(['dvh_name = ',new_name])
        
        s=''.join(line)   
        
        f.seek(0)
        
        f.write(s)
        
        f.close()
        
    def write_tem_name(self):
        """
           write name to certain path
        """    
        f = open(self.path[2][7], "r+")
        
        line = f.readlines()
        
        ind = self.path[4].rindex('\\')
        
        line[1] = ''.join(['template = ',self.path[4][ind+1:-4]])
        
        s=''.join(line)   
        
        f.seek(0)
        
        f.write(s)
        
        f.close()
        
    def write_name(self,ID):
        """
           write name to certain path
        """    
        f = open(self.path[2][4], "r+")
        
        line = f.readlines()
        
        line[1] = ''.join(['name = ',ID])
        
        s=''.join(line)   
        
        f.seek(0)
        
        f.write(s)
        
        f.close()
    
    def csv_read_to_dvh(self):
        import csv
        self.DVH = {}
        path_dvh = ''.join([self.path[3],self.dvh_name,'.csv'])
        csv_reader = csv.reader(open(path_dvh, encoding='utf-8'))
        row = [ row for row in csv_reader]
        ## wash dvh data
        for item in row:
            if len(item) == 3:
                for i in range(len(item)):
                    item[i] = item[i].replace(' ','')
                    
        dvh = row[3:-3]  ## remove redundant data
        flag = []
        for i in range(len(dvh)-1):
            if dvh[i][0] != dvh[i+1][0]:
                flag.append((dvh.index(dvh[i]),dvh[i][0]))
                continue
        flag.append((dvh.index(dvh[-1]),dvh[-1][0]))
                
                
        for item in flag: self.DVH[item[1]] = []        
                
                
        for j in range(len(flag)):
            
            if j != 0:
                
                for k in range(flag[j-1][0]+1,flag[j][0]+1):
                    
                    self.DVH[flag[j][1]].append((float(dvh[k][1]),float(dvh[k][2])))
                    
            else:
                
                for k in range(flag[j][0]+1):
                    
                    self.DVH[flag[j][1]].append((float(dvh[k][1]),float(dvh[k][2])))
        
        return self.DVH
    
    def txt_read_to_dvh(self):
    
        DVH = []   
        with open(self.txtpath, "r+") as f: 
            line = f.readlines()
            
        for item in line:
            if 'Structure Name' in item:
                flag = line.index(item)
                break
            
        
        for item in line[flag+1:-1]:
            m = []
            kk = item.split('  ')
            
            for i in kk:
                if i != '':
                    if '\n' in i:
                        m.append(i[:-2])
                    else:
                        m.append(i)
                        
            DVH.append(m)
        name = list(set([item[0] for item in DVH]))
        name.remove('')
        dvh = {}
        for i in name: dvh[i] = []
        
        for item in DVH:
            if '' not in item:
                dvh[item[0]].append((item[1],item[2]))
            
        return dvh
    

    def read_flag(self):
        '''
           path here is flag.txt in self.path
        '''
        with open(self.path[2][3], "r+") as f: 
            line = f.readlines()
        return line[1][-1]
    
    def write_flag(self):
        """
           this function to change flag from 0 to 1
        """    
        f = open(self.path[2][3], "r+")        
        line = f.readlines()
        line[1] = 'flag = 1'
        s=''.join(line)   
        f.seek(0)
        f.write(s)
        f.close()
        
    def write_iter(self,iter_num):
        """
           this function to change flag from 0 to 1
        """    
        f = open(self.iter_path, "r+")        
        line = f.readlines()
        line[1] = ''.join(['iteration = ',str(iter_num)])
        s=''.join(line)   
        f.seek(0)
        f.write(s)
        f.close()    
        
    def show_OARs(self,diff_result,tar_res_nam):
        '''
           This program tries to show OARs which are overdose
        '''
        self.OARs = {}
        
        for key in diff_result.keys():
            
            if key not in tar_res_nam:
            
                for item in diff_result[key]:
            
                 if item[1] > 1 and 'CTV' not in key and 'PTV' not in key:
                    
                    self.OARs[key] = diff_result[key]
        
        print('================================================')
        print('OARs still overdose:     \n')
        print(self.OARs)
        print('================================================')
         
    def read_template(self):
        
        self.line,self.strt,self.pointer,self.dose_eng_index ,self.strt_index= [],[],[],[],[]
        self.strt_fun = {}
     
        with open(self.path[4], "r+") as f:
            
          line1 = f.readline()
          
          self.line.append(line1)
          
          while line1:
              
            self.pointer.append(f.tell())  #record the pointer loaction to help write
            
            line1 = f.readline()
            
            self.line.append(line1)
    
        # mark place of structure in line
        self.strt_index = [i for i,a in enumerate(self.line) if a=='!VOIDEF\n']
        
        self.dose_eng_index = [i for i,a in enumerate(self.line) if a=='!DOSE_ENGINES\n']
        
        count = len(self.strt_index)
        
        self.strt = [self.line[j+1][9:-1] for j in self.strt_index]
                
        # list_fun record number of cost function and type    
        for index in range(count):
            
            count_fun = 0
            
            list_fun = []
            
            indx = [4,6,9,10,13,16,18,19,20,23,21,22]
            
            type_cost = ['type=se','type=pa','type=mxd','type=po','type=qp','type=conf','type=o_q','type=u_q','type=u_v','type=o_v']
            
            if index == count-1:
                
                for flag in range(self.strt_index[index],self.dose_eng_index[0]):
                    
                    if self.line[flag] == '    !COSTFUNCTION\n':
                        
                        count_fun = count_fun + 1
                        
                        list_fun.append([self.line[flag+1][8:-1],flag+1])
                        
                        # cost functions differ with flag+1
                        if self.line[flag+1][8:-1] in type_cost:
                            
                            for item in indx:
                                
                                list_fun.append([self.line[flag+item][8:-1],flag+item])                               
            else:
                
                for flag in range(self.strt_index[index],self.strt_index[index+1]):
                    
                    if self.line[flag] == '    !COSTFUNCTION\n':
                        
                        count_fun = count_fun + 1
                        
                        list_fun.append([self.line[flag+1][8:-1],flag+1])
                        
                        if self.line[flag+1][8:-1] in type_cost:
                            
                            for item in indx:
                                
                                list_fun.append([self.line[flag+item][8:-1],flag+item])
                       
            list_fun.append(count_fun)
            
            self.strt_fun[self.strt[index]] = list_fun    
    
        return self.strt_fun,self.strt_index,self.line
    
    def write_template(self,line,updated_struct_fun):
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
        
        f = open(self.path[-1],'w+')
        
        f.seek(0)
        
        f.write(s)
        
        f.close()    
    
    def read_csv_zs(self,DVH,tras):
        '''
           This function outputs two variables:
               1) list of struct name
               2) dict of dose indices
        '''
        import csv
        # tras =  {'TM L': 'TMJ-L', 'TM R': 'TMJ-R'}
        self.pres_strt_ind = {}
        self.pres_strt = []
        self.dvh_data = {}
        
        with open(self.path[0]) as csvfile:  
            readCSV = csv.reader(csvfile, delimiter=',')  
            prep = [row for row in readCSV]  
        
        
        # to ensure the prep list has the same name with struct name
        for item in prep:
            if item[0] in tras.keys(): item[0] = tras[item[0]]
        ## extract the evaluation indices in prescription csv
        
        self.pres_strt = list(set([l[0] for l in prep if l[0] != 'prep' and l[0] != 'frac' ]))
        
#        dose_frac = [l for l in prep if l[0] == 'prep' or l[0] == 'frac' ]
        
        for item in self.pres_strt: self.pres_strt_ind[item] = [] # initialization
        
        for item in prep:
            
            if item[0] != 'prep' and item[0] != 'frac':
                
                if item[2][-1] != '%':
                    
                    self.pres_strt_ind[item[0]].append((item[1],float(item[2])/100))
                    
                else:
                    
                    self.pres_strt_ind[item[0]].append((item[1],float(item[2][:-1])))
    

        for item in self.pres_strt:
            if item.replace(' ','') in DVH.keys():
                self.dvh_data[item] = DVH[item.replace(' ','')] 
        
        
        
        return self.dvh_data,self.pres_strt_ind
 
    
    def DVH_inf(self,dvh_data):
        '''
           This function deals with the dvh data for evaluation and guide for next parameters modification
           dvh_data : dict.({'Brain':[(d1,v1),(d2,v2),....]})
           dvh_data_diff : differential dvh data
           
           In this program, PTV5096's maximum dose has some problems.
        '''
        dvh_data_diff = {}
        self.dvh_inf = {}
        self.dvh_inf['Dmean'] = {}
        self.dvh_inf['Dmax'] = {}
        for key in dvh_data.keys():
            
            dvh_data_diff[key] = [(dvh_data[key][i][0],dvh_data[key][i][1]-dvh_data[key][i+1][1]) for i in range(len(dvh_data[key])-1)]
            
            dvh_data_diff[key].append((dvh_data[key][-1][0],dvh_data[key][-1][1]))
            
            self.dvh_inf['Dmean'][key] = round(sum(item[0]*item[1] for item in dvh_data_diff[key])/sum([item[1] for item in dvh_data_diff[key]]),1)
         
                
            for item in dvh_data[key]:
                
                if item[1] == 0:
                    
                    flag = dvh_data[key].index(item)
                    break
                
            self.dvh_inf['Dmax'][key] = dvh_data[key][flag-1][0]
     
        return self.dvh_inf

    def back_strt_fun(self,struct_fun,struct_index,line,path,name,cost_name,loc):
        '''
           transfer the altered variable to struct_fun
           if you want to change cost function, remember to change 13
        '''       
        for key in name.keys():
              
            for n in range(len(name[key])):
                
                struct_fun[key][13 * n + loc][0] = cost_name + str(name[key][n][1])
    
        return struct_fun

    def extract_strt_fun(self,struct_fun,loc,start):
        '''
        To extract some parameters from struct_fun to help optimization
           name: e.g. isoconstraint,
           loc: e.g. location in struct_fun
           start: number start from the str
        '''
        self.name = {}
        
        for key in struct_fun.keys():
            
            self.name[key] = []
                
            for n in range(struct_fun[key][-1]):
                
                self.name[key].append([struct_fun[key][13*n][0],round(float(struct_fun[key][13*n+loc][0][start:]),5)])
         
        return self.name

 
    def plan_results1(self,dvh_inf,dvh_new_data,pres_strt_ind):
        '''
           This function returns a plan results of DVH
           the name of dvh_new_data must be consistent with struct_index
           
        '''
        import numpy as np
        from scipy.interpolate import interp1d 
        self.dvh_indices,self.diff_result = {},{}
        for item in pres_strt_ind.keys(): self.dvh_indices[item] = []
        for item in pres_strt_ind.keys(): self.diff_result[item] = []
        
        for item in pres_strt_ind:
                
                for j in pres_strt_ind[item]:
                    
                    if j[0] == 'Dmax':
                        
                        self.dvh_indices[item].append((j[0],round(dvh_inf[j[0]][item]/100,2)))
                        
                    elif j[0] == 'Dmean':
    
                        self.dvh_indices[item].append((j[0],round(dvh_inf[j[0]][item]/100,2)))
                        
                        
                    elif j[1] == 95.0:
                        
                        cover = float(j[0][1:])*100  ## indicate prescription dose
                        
                        for item1 in dvh_new_data[item]:
                            ## retify the problem in 0-5100
                            if item1[1] == 100:
                                
                                index = dvh_new_data[item].index(item1)
                                
                                print('appear 5096 in 0-5111')
                                
                                
                        if cover <= dvh_new_data[item][index][0]:
                            
                            self.dvh_indices[item].append((j[0],100))
                        
                        else:
                            
                            mini = 100
                            mini_id = 0
                            for item1 in dvh_new_data[item]:
                                if abs(item1[0]-cover) <= mini:
                                    mini = abs(item1[0]-cover)
                                    mini_id = dvh_new_data[item].index(item1)
                                    
                            x,y = [],[]
                            for i in range(mini_id-1,mini_id+2):
                                y.append(round(dvh_new_data[item][i][1],4))
                                x.append(round(dvh_new_data[item][i][0],4))
                                
                            x = np.array(x)
                            y = np.array(y)
                            f=interp1d(x,y,kind = 'linear')#interpolate
                            self.dvh_indices[item].append((j[0],round(float(f(cover)),4)))
                        
                    elif j[0][0] == 'V':
                       
                        ## to find with interpolate without consider 0.03cc              
                        mini = 10000
                        dose = float(j[0][1:])*100
                        for item1 in dvh_new_data[item]:
                            if abs(item1[0]-dose) < mini:
                                mini = abs(item1[0]-dose)
                                mini_id = dvh_new_data[item].index(item1)
                        xx = [dvh_new_data[item][i][0] for i in range(mini_id-1,mini_id+2)]
                        yy = [dvh_new_data[item][i][1] for i in range(mini_id-1,mini_id+2)]
                        f=interp1d(xx,yy,kind = 'linear')#quadratic interpolate
                        self.dvh_indices[item].append((j[0],round(float(f(dose)),2)))   
                        
        for item in self.dvh_indices:
            for i,j in zip(self.dvh_indices[item],pres_strt_ind[item]):
                self.diff_result[item].append((j[0],round(i[1]/j[1],2)))
        
        return self.dvh_indices,self.diff_result

    def opt_prostate(self,diff_result,tar_res_nam):
        '''
           This is the optimization program for prostate
           inf: the dict stored the isoconstraints, isoeffects,weights,relative impact information etc.
           diff_result: a reference for evaluate the discrepancy from original prescription requirements
           tar_res_nam: list stored the target name
        '''
        import math
    #    count = 0
        
        IE = self.inf['ise'] 
        
        IC = self.inf['isc'] 
        
        W = self.inf['wgt'] 
        
        R = self.inf['rlp']  
        
        T = [diff_result[i] for i in tar_res_nam]
        
        print (T)
        
        tar_sum = sum([math.floor(item[0][1]) for item in T])
    
        if tar_sum == len(T):
            
            flag = 2 # indicate target is good
            
            print('Original parameters\n')
            
            for key in IC.keys():
                ## restrict the constraints
                if key in tar_res_nam or key == 'patient':
                    
                    for i,item in enumerate(IC[key]):
                        ## item = [type='qp',70]
                        if item[0] == 'type=o_q':
                            
                            print(item)
                            
                            if R[key][i][1] <= 0.5: ##(+,++)
                                
                                IC[key][i][1] = (IE[key][i][1]+IC[key][i][1])/2
                                    
                            elif R[key][i][1] <= 0.75: ##(+++)
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = (IE[key][i][1]+IC[key][i][1])*2/3
                                    
                                else:
                                    
                                    IC[key][i][1] = min((IC[key][i][1]+R[key][i][1]),IE[key][i][1])
                            
                            else:  ##(++++)
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IC[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = max((IC[key][i][1]+R[key][i][1]),IE[key][i][1])
                                    
                                    
                        else:
                            
                            IC[key][i][1] = IC[key][i][1]
                                
                else: ## this means the normal tissue
                    
                    for i,item in enumerate(diff_result[key]):
                        
                        if item[1] > 1:
                            
                            if R[key][i][1] >=0.75 or W[key][i][1] >3:    
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2
                                    
                                else:
                                    
                                    IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2
                                                        
                            elif R[key][i][1] == 0 or W[key][i][1] == 0.01:
    
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IE[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1] - item[1]                        
                                              
                            else:
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IE[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1] - item[1]/2                               
    
                        elif item[1] <= 0.5:
                            
                            if R[key][i][1] >=0.75 or W[key][i][1] >3:    
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IC[key][i][1] + item[1]
                                    
                                else:
                                    
                                    IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2
                                                        
                            elif R[key][i][1] == 0 or W[key][i][1] == 0.01:
                                
                                IC[key][i][1] = (IE[key][i][1]+ IC[key][i][1])/2
                                              
                            else:
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = (IE[key][i][1]+IC[key][i][1])/2
                                    
                                else:
                                    
                                    IC[key][i][1] = IE[key][i][1]                             
                                
                        else: 
                            
                            if R[key][i][1] >=0.75 or W[key][i][1] >3:    
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2 
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1] + (1-item[1])/2
                                                        
                            elif R[key][i][1] == 0 or W[key][i][1] == 0.01:
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IE[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1] - item[1]
                                              
                            else:
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = (IE[key][i][1]+IC[key][i][1])/2
                                    
                                else:
                                    
                                    IC[key][i][1] -= item[1]/2                   
                    
                    
                
          
        else:
            
            flag = 3  # indicate this function is not good !
            
            print('Original parameters\n')
            
            for key in IC.keys():
                
                print(key,IC[key])
            
            #################################
            ## Please write your code here ##
            #################################
            
            
            
            for key in IC.keys(): # in this IC, the target cosntraints also in it
                
                if key in tar_res_nam or key == 'patient':
                    
                    for i,item in enumerate(IC[key]):
                        
                        IC[key][i][1] += R[key][i][1]/2
                        
                else:
                             
                    for i,item in enumerate(diff_result[key]):
                                               
                        if item[1] < 0.6:  ## 
                            
        
                            IC[key][i][1] += R[key][i][1]
                            
                        elif item[1] < 0.85: ## 
                            
                            IC[key][i][1] += R[key][i][1]/2
                            
                        else:                        
                             
                            IC[key][i][1] += R[key][i][1]/3
                    
                        
    
    
    
        self.inf['ise'] = IE
        
        self.inf['isc'] = IC
        
        self.inf['wgt'] = W
        
        self.inf['rlp'] = R  
        
        
        
        return self.inf,flag


    def opt_HeadNeck(self,diff,tar_res_nam,level_OARs):        
        '''
           This is home developed automatic optimization module
           ##
           input: inf(iso_effect,iso_constraint,weight,rel_imp,step_size)
                  step_size(the step for adjusting dose parameters)
                  diff_result(the evaluation index)
                  level_OARs(the OARs with level for us)
                  theshold(theshold set for optimization)
                  
           ##       
           output: updated inf(iso_effect,iso_constraint,weight,rel_imp)
                   flag to mark whether target is overdose or underdose
                   
           希望采用自适应步长的方法进一步优化出比较好的结果
           而且此 program 也只是针对三个靶区结构
           此种写法目前只能针对每个器官对应一个评价指标，如果存在两个评价指标，此程序会报错
           
           relative_impact :
               1) +: 0-0.25
               2) ++: 0.25-0.5
               3) +++: 0.5-0.75
               4) ++++: 0.75-1.0
           
           
           ##
           这里没有才有input imrt constarints和evaluation indices一一对应来改变参数
           这里大部分情况是多对一的情况,或者是多对多情况
           
        
        '''
        import math
#        count = 0
        
        IE = self.inf['ise'] 
        
        IC = self.inf['isc'] 
        
        W = self.inf['wgt'] 
        
        R = self.inf['rlp']  

#        for item in tar_res_nam:
#        
#            del W[item]
#            
#            del IE[item]
#            
#            del IC[item]
#            
#            del R[item]
#    
#        del W['patient']
#        
#        del IE['patient']
#        
#        del IC['patient']
#        
#        del R['patient']
        
        diff_result = {}         ## 打一个补丁,将原来的diff换成新的
        for key in diff.keys():
            diff_result[key] = diff[key][0][1]
        
        target = [diff_result[i] for i in tar_res_nam]
        tar_sum = sum([math.floor(item) for item in target])
        
        prior_name = ['Neck']
        

    #    for item in diff_result.keys():
    #        if item == 'PAROTIDS':
    #            diff_result['Parotids'] = diff_result[item]
    #            del diff_result[item]
        ## force_OARs = {'Spinal Cord': 1, 'Cord PRV': 1,
        ## 'Brain Stem': 1, 'Stem PRV': 1, 'Len L': 2, 
        ## 'Len R': 2, 'Optic Chiasm': 2, 'Optic Nerve L': 2,
        ## 'Optic Nerve R': 2, 'Pituitary': 2, 'Inner Ears': 2,
        ## 'Parotids': 3, 'Esophagus': 4, 'Trachea': 4, 
        ## 'Thyroid': 4, 'Mandible': 4, 'Oral Cavity': 4, 'Larynx': 4, 'Neck': 4}
    
        if tar_sum == len(tar_res_nam):
            
            flag = 2 # indicate this functiion is good
            
            print('Original parameters\n')
            
            for key in IC.keys():
                
                print(key,IC[key])
                
            
            #################################
            ## please write your code here ##
            #################################
                if key in tar_res_nam or key == 'patient':
                    
                    for i,item in enumerate(IC[key]):
                        ## item = [type='qp',70]
                        if item[0] == 'type=o_q':
                            
                            print(item)
                            
                            if R[key][i][1] <= 0.5: ##(+,++)
                                
                                IC[key][i][1] = IE[key][i][1]
                                    
                            elif R[key][i][1] <= 0.75: ##(+++)
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IE[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = min((IC[key][i][1]+R[key][i][1]),IE[key][i][1])
                            
                            else:  ##(++++)
                                
                                if IC[key][i][1] > IE[key][i][1]:
                                    
                                    IC[key][i][1] = IC[key][i][1]
                                    
                                else:
                                    
                                    IC[key][i][1] = max((IC[key][i][1]+R[key][i][1]),IE[key][i][1])
                                    
                                    
                        else:
                            
                            IC[key][i][1] = IC[key][i][1]                
           
                
                if key in level_OARs and level_OARs[key] == 1: # this  indicate the stem and cord
                                    
                    for i in range(len(IE[key])):
                        
                        if 'PRV' in key.upper():
                    
                            if diff_result[key] > 1 :  # 这是对PRV给劲
                                
                                if R[key][i][1] >= 0.75 or W[key][i][1] >= 3:  # 变量极其难压制
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2
                                        
                                    else:
                                        
                                        IC[key][i][1]  += R[key][i][1]
                                                        
                                elif R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，这里需要将他压下去
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = (IE[key][i][1] + IC[key][i][1])/2
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)
    
                                
                                else:
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = (IC[key][i][1]+IE[key][i][1])/2
                                        
                                    else:
                                        
                                        IC[key][i][1] += round(diff_result[key],3)/3
                                                                          
                            elif diff_result[key] > 0.75: # 这是做计划次要矛盾
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    ## 其实这里会陷入问题，对于isoconstraint,isoeffect,哪一个小取哪一个
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1]  += round(diff_result[key],3)
                                
                                elif R[key][i][1] <= 0.5 and W[key][i][1] <= 5 and R[key][i][1] > 0 and W[key][i][1] > 0:  # 变量比较容易
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] += round(diff_result[key],3)/3
                                
                                else:
                                   
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1]  = IE[key][i][1]
                            
                                
                            elif diff_result[key] > 0:  # 这种属于基本满足情况
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1]  = IC[key][i][1]
                                
                                elif R[key][i][1] <= 0.5 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0: # 考察一下权重和敏感度
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1]  -= round(diff_result[key],3)/3
                                    
                                else:
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                        
                        else:  
                            
                            if diff_result[key] > 1:# 这是对Stem&Cord的压制
                            
                                if R[key][i][1] >= 0.75 or W[key][i][1] >= 5:  # 变量极其难压制
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2 
                                                        
                                elif R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，这里需要将他压下去
                                    
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)
                                
                                else:
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1] 
                                        
                            elif diff_result[key] >= 0.75: # 这是对Stem&Cord的压制
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    ## 其实这里会陷入问题，对于isoconstraint,isoeffect,哪一个小取哪一个
                                    if IC[key][i][1] > IE[key][i][1]:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2
                                
                                elif R[key][i][1] < 0.75 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0:  # 变量比较容易
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)//3
                                
                                else:
                                   
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                    else:
                                        
                                        IC[key][i][1]  = IC[key][i][1] ##冻结
                                              
                            elif diff_result[key] > 0:  # 这种属于肯定满足情况
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                
                                elif R[key][i][1] < 0.75 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0: # 考察一下权重和敏感度
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                    
                                else:
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                if key in level_OARs and level_OARs[key] == 2: # 这说明是视觉系统
                
                    for i in range(len(IE[key])):
                        
                        if diff_result[key] > 1:  # 这是做计划的主要矛盾
                            
                            if R[key][i][1] >= 0.75 or W[key][i][1] > 5:  # 变量比较难压制
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2 # isoconstraint走diff_result/2步长
                            
                            elif R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，这里需要将他压下去
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                    
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)
                            
                            else:
                                
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IE[key][i][1]                             
                                
                                else:
                                    
                                    IC[key][i][1] -= round(diff_result[key],3)/2 # isoconstraint走diff_result步长
                                
                        elif diff_result[key] >= 0.75:  #这是做计划的次要矛盾
                            
                            if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                ## 其实这里会陷入问题，对于isoconstraint,isoeffect,哪一个小取哪一个
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IE[key][i][1]   
                                    
                                else:
                                    
                                    IC[key][i][1] -= round(diff_result[key],3)/2
                            
                            elif R[key][i][1] <= 0.75 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0:  # 变量比较容易
    
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IE[key][i][1]  
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1]
                            
                            else:
                                
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IC[key][i][1] 
                                    
                                else:
                                    
                                    IC[key][i][1] += R[key][i][1]                              
                            
                        elif diff_result[key] > 0:  # 这种属于肯定满足情况
                            
                            if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IE[key][i][1]   
                                    
                                else:
                                    
                                    IC[key][i][1] -= round(diff_result[key],3)/3
                            
                            elif R[key][i][1] <= 0.5 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0: # 考察一下权重和敏感度
                                
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IE[key][i][1]  
                                    
                                else:
                                    
                                    IC[key][i][1] = IC[key][i][1]                            
                            else:
                                
                                if IC[key][i][1] > IE[key][i][1]: 
                                        
                                    IC[key][i][1] = IC[key][i][1]  
                                    
                                else:
                                    
                                    IC[key][i][1] += R[key][i][1]  
                                    
                if key in level_OARs and level_OARs[key] == 3: # this indicates parotids
                
                    for i in range(len(IE[key])):
                        
    #                    if i == 0:  # 这是指的第一个serial函数
    #                        IC[key][i][1] = IC[key][i][1]
    #                    
    #                    else:
                      
                            if diff_result[key] > 1:  # 这是做计划的主要矛盾
                                
                                if R[key][i][1] >= 0.75 or W[key][i][1] > 5:  # 变量比较难压制
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1]  = IC[key][i][1] # isoconstraint走diff_result/2步长
                                
                                
                                elif R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，这里需要将他压下去
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)
                                        
                                else:
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/3
                                        
                            elif diff_result[key] > 0.85: # 这是做计划次要矛盾
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    ## 其实这里会陷入问题，对于isoconstraint,isoeffect,哪一个小取哪一个
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2
                                
                                elif R[key][i][1] <= 0.75 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0:  # 变量比较容易
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/3    
                                        
                                else:
                                   
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IC[key][i][1]  
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]   
                        
                                
                            elif diff_result[key] > 0:  # 这种属于肯定满足情况
                                
                                if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]   
                                
                                elif R[key][i][1] <= 0.5 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0: # 考察一下权重和敏感度
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2  
                                    
                                else:                                    
                                        IC[key][i][1] += R[key][i][1]
                                                         
                if key in level_OARs and level_OARs[key] == 4: # 这是剩余的organs
                
                    for i in range(len(IE[key])):
                        
                        if diff_result[key] > 1:  # 这是做计划的主要矛盾
                            
                            if key in prior_name:
                                
                                if R[key][i][1] >= 0.5 or W[key][i][1] >= 3:
                                    # 变量比较难压制
                                    if IC[key][i][1] < IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1] 
    
                                    else: 
    
                                        IC[key][i][1] += R[key][i][1]                                
    
                                else:
                                    ## 这表明这是很难压下去的
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]
                                                                    
                            else:
                                                    
                                if R[key][i][1] >= 0.75 or W[key][i][1] > 5:  # 变量比较难压制
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] = IC[key][i][1]                            
                                
                                elif R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，这里需要将他压下去
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)                            
                                else:
                                    
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2
                                        
                        elif diff_result[key] > 0.85: # 这是做计划次要矛盾
                            
                            if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                ## 其实这里会陷入问题，对于isoconstraint,isoeffect,哪一个小取哪一个
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)     
                            
                            elif R[key][i][1] <= 0.75 and W[key][i][1] <= 3 and R[key][i][1] > 0 and W[key][i][1] > 0:  # 变量比较容易
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2                           
                            else:
                               
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IC[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] += R[key][i][1]     
                        
                            
                        elif diff_result[key] > 0:  # 这种属于肯定满足情况
                            
                            if R[key][i][1] == 0 and W[key][i][1] == 0.01:  # 僵尸指标，可以直接赋值isoeffect
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)    
                                        
                            elif R[key][i][1] <= 0.5 and W[key][i][1] <= 3: # 考察一下权重和敏感度
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IE[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] -= round(diff_result[key],3)/2                                
                            else:
                                
                                    if IC[key][i][1] > IE[key][i][1]: 
                                        
                                        IC[key][i][1] = IC[key][i][1]   
                                        
                                    else:
                                        
                                        IC[key][i][1] += R[key][i][1]          
        else:
            
            flag = 3  # indicate this function is not good !
            
            print('Original parameters\n')
            
            for key in IC.keys():
                
                print(key,IC[key])
            
            #################################
            ## Please write your code here ##
            #################################
            for key in R.keys():
                
                for i in range(len(R[key])):
                    
                    ### 这里不管加号多少，上调的幅度和加号成线性关系，如果是R = 0
                    ### 就不会改变
                    ## 打一个补丁
    #                if key == 'Parotids' and i == 0:
    #                    
    #                    pass    
                    
    #                else:
                        
                    if diff_result[key] < 0.6:  ## 表示这个指标压得很低，但是牺牲了靶区，可以多增加一点量来补偿靶区
                        
                        ## 如果指标压的很低，但是relative_impact很小的话，其实不会增加很大的量
                        ## 反而指标压的低，但是relative_impact很大的话，其实增加的量会比较大
                        IC[key][i][1] += R[key][i][1]
                        
                    elif diff_result[key] < 0.85: ## 表示指标压得不算太低，但是也需要补偿一些靶区
                        
                        IC[key][i][1] += R[key][i][1]/2
                        
                    else:                        ## 表示刚刚压住，需要减小一部分来补偿靶区
                         
                        IC[key][i][1] += R[key][i][1]/3
                    

        self.inf['ise'] = IE
        
        self.inf['isc'] = IC
        
        self.inf['wgt'] = W
        
        self.inf['rlp'] = R  
        
        
#        ## Check break conditions
#        for key in diff_result.keys():
#            
#            if key not in tar_res_nam and key != 'patient' and 'PTV' not in key and 'CTV' not in key and diff_result[key] < 1:
#                
#                count += 1
#        
#        if count == 15 and tar_sum == len(tar_res_nam):
#            
#            flag = count   ## set break out point 必须是靶区到达要求，危及器官压下来才可以退出
#            
#        else:
#            
#            flag = flag
        
        return self.inf,flag



    def exe1(self,tras):
        '''
          This function was mainly used for extract the dvh results for optimization 
        '''
        flag = self.read_flag()   #read flag file
        while flag == '1':        
            '''
            This time sleep is for Monaco Calculation
            '''
            time.sleep(15)    
            
            flag = self.read_flag()      
            
            print ('flag = 1,waiting for Monaco Calculation...\n')      
        
        print ('flag = {}, start adjusting optimiation parameters...\n'.format(flag))    
            
        if flag == '0':      
            
            strt_fun,strt_index,line = self.read_template()   #read template information
        
            dvh_name = self.read_dvh()   #read saved name of dvh.csv
            
            DVH = self.csv_read_to_dvh()   #from .csv file extract the DVH data
            
            dvh_new_data,pres_strt_ind = self.read_csv_zs(DVH,tras)  #1) ensure names in dvh is consistent with struct 2)read prescription
            
            dvh_inf = self.DVH_inf(dvh_new_data)  #extract Dmean and Dmax from DVH
            
            dvh_indices,diff_result = self.plan_results1(dvh_inf,dvh_new_data,pres_strt_ind)   #calcualte the ratio of calculation and prescription
           
            self.write_dvh(str(dvh_name+str(random.randint(0,10)))) # to prevent the repetition of name
            
        return strt_fun,strt_index,line,diff_result


    def exe2(self,tar_res_nam,selection,level_OARs,tras):
        '''
           This function mainly was mainly used for parameters modification
        ''' 
        strt_fun,strt_index,line,diff_result = self.exe1(tras)     
        
        self.inf = {} # to store all the information in template(isoconstraint,isoeffect,weight,relative impact,shrink margin)
        
        for i,item in enumerate(ind_loc_strt[3]):
            
            self.inf[item] = self.extract_strt_fun(strt_fun,ind_loc_strt[0][i],ind_loc_strt[1][i])
        
        
        ####================opt_packages=========================## 
        if selection == '1':
            ## 用来优化前列腺cases
            inf,flag = self.opt_prostate(diff_result,tar_res_nam)
            
        else:
            ## 用来优化头颈cases
#            level_OARs
            inf,flag = self.opt_HeadNeck(diff_result,tar_res_nam,level_OARs)
        ####================opt_packages=========================##
        
        
        #to transfer the inforamtion to struct_fun
        struct_fun = self.back_strt_fun(strt_fun,strt_index,line,self.path[-1],inf['isc'],ind_loc_strt[2][1],ind_loc_strt[0][1])             
               
        for key in inf['isc'].keys():
            
            print('########################################')
            print('Updated parameters\n')
            print(key,inf['isc'][key])   
    
    
        
        return struct_fun,flag,inf,diff_result,line


    def exe3(self,tar_res_nam,selection,level_OARs,tras):
        '''
           this function mainly execute the struct_fun's transformation
        '''
        struct_fun_updated,mark3,information,diff_result,line = self.exe2(tar_res_nam,selection,level_OARs,tras)
        
        if mark3 == 3:
            print ('Target was underdose!!\n')
            print ('===========================================================================')
            print ([(item,diff_result[item][0][1]) for item in tar_res_nam])            
            print ('===========================================================================')
            
            ## print some OARs still overdose
            
            self.show_OARs(diff_result,tar_res_nam)
            
            self.write_template(line,struct_fun_updated)
            
            # write flag to 1
            self.write_flag()
       
        elif mark3 == 2:
            print('Target has maintained...\n')
            print ('===========================================================================')
            print ([(item,diff_result[item][0][1]) for item in tar_res_nam])  
            print ('===========================================================================')
            
            ## print some OARs still overdose
            
            self.show_OARs(diff_result,tar_res_nam)
            
            self.write_template(line,struct_fun_updated)
            
            # write flag to 1
            self.write_flag()
            
        else:
            
            print('Break out of the iteration and further optimization...\n')
            print ('===========================================================================')
            print ([(item,diff_result[item][0][1]) for item in tar_res_nam])      #        print ('Three target coverage {}: {} {}: {} {}: {}'.format(tar_res_nam[0],round(95*diff_result[tar_res_nam[0]],2),tar_res_nam[1],round(95*diff_result[tar_res_nam[1]],2),tar_res_nam[2],round(95*diff_result[tar_res_nam[2]],2)))
            print ('===========================================================================')
            
            ## print some OARs still overdose
            
            self.show_OARs(diff_result,tar_res_nam)
            
            self.write_template(line,struct_fun_updated)
            
            # write flag to 1
            self.write_flag()
    
        return mark3,information,diff_result

#%%==============================%%#
    
def main():
    ## generate template HN 
    X = Temp(path_temp,csv_file,colone_path)
    strt_ind_list,tras = X.initial(struct,struct_set,path_beam,selection)
    level_OARs = X.classify(strt_ind_list)
    print('the template path is following:\n')
    print('========================\n')
    print(colone_path)
    print('========================\n')
    print('Please check the generated tempalte!!!\n')
    print('.......\n')
    F = input('If the template is ok, please enter 1; if not, please enter 0:\n')
    ## optimization 
    if F == '1':
        Y = Tool(path,ind_loc_strt,iter_path)
        Y.write_tem_name()
        Y.write_iter(iteration)
        start3 = time.time()  
    
        for k in range(iteration):
            
            fla3,inf,diff = Y.exe3(tar_res_nam,selection,level_OARs,tras)
            
            inf_iter['iteration' + str(k + 1)] = inf
            
            diff_iter['iteration' + str(k + 1)] = diff   
            
        end3 = time.time() 
        
        print('the step3 consume {} s'.format(end3 - start3))  
    
    else:
        Y = Tool(path,ind_loc_strt,iter_path)
        Y.write_iter(iteration)       
        print('Please remodificate your initial template!!\n')
    
    
#%%==============================%%#    
import os
import time
import random
import glob
import pydicom
ind_loc_strt = [[3,7,8,10,9],
[13,14,10,7,15],
['shrinkmargin=','isoconstraint=','isoeffect=','weight=','relativeimpact='],
['skg','isc','ise','wgt','rlp']]
def_path = os.getcwd()
txt_path = ''.join([def_path,'\\database\\txtfile\\file3'])
temp_path = 'C:\\Users\\Public\\Documents\\CMS\\FocalData\\MonacoTemplates\\'
path_beam = ''.join([def_path,'\\database\\txtfile\\file2\\part4(beam_arc).txt'])
path_temp = glob.glob(''.join([def_path,'\\database\\txtfile\\file1\\*.txt']))
struct_set1 = {'CTV4500': 0,'CTV6750': 0,'CTV6275': 0,'CTV4750': 0,'Metal': 0,
              'Carbon Fiber': 0,'Foam Core': 0,'PTV6750': 1,'PTV6275': 2,
              'PTV4750': 3,'PTV4500': 4,'Bladder': 5,'Rectum': 6,'Pubic Bone': 7,
              'Femoral Head R': 8,'Femoral Head L':9,'Intestine': 10,
              'Penile Bulb': 11,'patient': 100}
struct_set2 = {'GTVnd6600': 100, 'Artifact': 100, 'Stem PRV': 6,'BrainPRV':6,
              'Thyroid': 19, 'TMJ-R': 14, 'Metal': 100, 'Lung L': 100,
              'Parotids': 16, 'CTVtb': 100, 'Pituitary': 12, 'SPPRV': 4,
              'Foam Core': 100, 'Trachea': 18, 'patient': 24, 'Len all': 100,
              'Cord PRV': 4, 'CordPRV': 4,'Len L': 7, 'CTV5096': 100, 'PGTVnd6600': 100,
              'FanDown': 100, 'Larynx': 22, 'Spinal Cord': 3, 'Eye R': 100,
              'PGTVnx6996-1': 100, 'spinalcord3': 100, 'Optic Chiasm': 9,
              'TMJ-L': 13, 'PAROTIDS': 16, 'PGTVnd6996': 1, 'Lung R': 100,
              'Len R': 8, 'TM R': 14, 'Oral Cavity': 21, 'Parotid all': 16,
              'Neck': 23, 'Mid': 100, 'Mandible': 20, 'NeckPc': 100,
              'teeth': 100, 'Optic Nerve L': 10, 'Inner Ears': 15,
              'PGTVnx6996': 0, 'OralCavity2': 100, 'FanUp': 100, 'Brain Stem': 5,
              'PTV5096-1': 100, 'GTVnx6996': 100, 'PTV5096': 2, 'Eye L': 100,
              'TM L': 13, 'Carbon Fiber': 100, 'PTVtb5936': 100, 'Neck2': 100,
              'GTVnd6996': 100, 'Optic Nerve R': 11, 'Parotid R': 100, 'BSPRV': 6,
              'Oral Cavity2': 100, 'Esophagus': 17, 'Optic Nerve all': 100,
              'Parotid L': 100, 'Brain': 100}
ID = input('Please enter the patient ID:\n')
selection = input('Please enter your selection: Prostate(enter 1) & HN(enter 2)\n')
if selection == '1':
    tar_res_nam = ['PTV6750','PTV4750']
    path_struct_set = glob.glob(''.join([def_path,'\\database\\case\\prostate\\struct_file\\*.dcm']))
    stru_path= ''.join([def_path,'\\database\\case\\prostate\\struct_file\\',ID,'_StrctrSets.dcm'])
    csv_file = ''.join([def_path,'\\database\\case\\prostate\\prescription\\',ID,'.csv'])
    colone_path = ''.join([temp_path,'RTOG0815prostate1.hyp'])
    struct_set = struct_set1
else:
    tar_res_nam = ['PGTVnx6996','PGTVnd6996','PTV5096']
    path_struct_set = glob.glob(''.join([def_path,'\\database\\case\\HN\\struct_file\\*.dcm']))
    stru_path= ''.join([def_path,'\\database\\case\\HN\\struct_file\\',ID,'_StrctrSets.dcm'])
    csv_file = ''.join([def_path,'\\database\\case\\HN\\prescription\\',ID,'.csv'])
    colone_path = ''.join([temp_path,'HN2.hyp'])
    struct_set = struct_set2
  
dvh_path = ''.join(['C:\\Users\\Shelter6\\Desktop\\dvh\\',ID,'\\round4\\'])
path_ = [''.join([txt_path,'\\',item]) for item in os.listdir(txt_path) if item[-3:] == 'txt']  
path = [csv_file,stru_path,path_,dvh_path,colone_path]
struct= pydicom.read_file(stru_path,force=True)
inf_iter,diff_iter = {},{}

fla3 = 0
iteration = int(input('Please enter the wanted iterations:\n'))
iter_path = 'C:\\Users\\Shelter6\\Desktop\\HN_PK\\code\\code\\database\\txtfile\\iteration.txt'

if __name__ == '__main__':
    main()


## next task : you need to give each function a annotation
