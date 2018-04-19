# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 12:45:57 2018

@author: Paul
"""

#%% load all packages

import temp_tool
import os
#os.chdir('C:\\Users\\Paul\\Desktop\\generate_template(HN)')
cur_path = os.getcwd()
cur_path1 = cur_path + '\\templ_elem\\'

#a = []
#for i in os.walk(cur_path):
#    a.append(i)
path = []
for item in os.listdir(cur_path1):
    path.append(cur_path1 + item)

tar_res_nam = ['PGTVnx6996','PGTVnd6996','PTV5096']

prep_name,dose_criteria = temp_tool.prep_name_gene(path,tar_res_nam)

#%% 这个程序是让物理师来打标签

OARs_nam_level=temp_tool.level_organ(prep_name,tar_res_nam)
dose_inf = temp_tool.initial()       

#%% 生成克隆般templat.hyp文件

colone_path = cur_path + '\\colone_temp\\colone_template.hyp'
template = temp_tool.generate_template(path,tar_res_nam,prep_name,OARs_nam_level,dose_criteria,dose_inf)
template[-1] = '!ISPHANTOMMATERIAL    0\n'    
temp_tool.write_colone(template,colone_path)




