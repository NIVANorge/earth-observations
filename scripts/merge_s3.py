''' Since Sentinel 3 files are in 2 separate netcdf files for c2rcc and idepix, 
we have to merge them into one file first (before pixelextraction) 
'''


import os 
from util import S2_settings_table, S3_settings_table
import re
import glob
import pandas as pd
import xarray as xr


for n in ['1','2','3','4','5','6','7', '8']: #[]: #S3_settings_table.keys():
    region =  S3_settings_table[n]['name']   
    category = S3_settings_table[n]['wtype']
    srcdir = r'W:\Satellite\S3\L2\NIVA\c2rcc\_300m\{}\{}'.format(category,region)
    all_files = os.listdir(srcdir)
    #print (n)
    if not os.path.exists(srcdir + r'\\Merged_S3_data'):
        os.makedirs(srcdir + r'\\Merged_S3_data')

    for f in all_files:  
        merged_path = srcdir + r'\\Merged_S3_data'+ r'\\IdePix_'+ f
        if not os.path.exists(merged_path):

            if bool(re.search('C2RCC', f)):
                #print (f)
                second_file = srcdir + r'\\IdePix'+f[5:]
                #print ('second file',second_file)
                #print ('f',f)
                #print (second_file)
                #breakpoint()
                try:
                    ds = xr.open_dataset(second_file)
                    ds2 = xr.open_dataset(srcdir + r'\\' + f)
                    dsmerged = xr.merge([ds,ds2],compat='override')
                    #merged_path = r"D:\Prosjekt\satelitt\Merged_S3_data\{}\{}".format(category,region)+ r'\\IdePix_'+ f
                    dsmerged.to_netcdf(merged_path)
                    print ('merged',merged_path)
                except Exception as e:
                    print ('caught exception', e)
                    
        else:
            pass #print ('already merged')
            
    