import glob 
import shutil
import os


def copy_icor_to_altogether():
    '''
    Icor files are organised in a way that data from 
    each moth is in a separate folders.
    These files will be used as a source files for the pixelExtraction 

    For the pixelExtraction, we need to send a path to one folder containing all files. 
    So, this script gets all filles from all monthes and copies them into altogether folder. 
    Separate folders for each month, for each region 
    '''

    regions = ['32VNM', '32VNR', '32VPL', '33XWG']
    #for region in regions:
    #    all_header_files = glob.glob(fr"W:\Satellite\S2\L2\iCOR\V101\{region}\2019\*\*.nc")
    #    for f in all_header_files:
    #        name = os.path.basename(f)
    #        shutil.copy(f, fr"W:\Satellite\S2\L2\iCOR\V101\{region}\2019\altogether\{name}")
    #        #print (fr"W:\Satellite\S2\L2\iCOR\V101\{region}\2019\altogether\{name}")
            

    for region in regions:
        for year in ['2018','2019','2020']:
            if os.path.exists(rf"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}"):
                all_header_files = glob.glob(rf"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}\*\*.nc")
                for f in all_header_files:
                    name = os.path.basename(f)
                    
                    if not os.path.exists(fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}\altogether"):
                        os.makedirs(fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}\altogether")
                    #print ('copye')
                    if not os.path.exists(fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}\altogether\{name}"):
                        print ('copying', name)
                        shutil.copy(f, fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\{region}\{year}\altogether\{name}")   
                    else:
                        print ('exists')  
import re            
import os   
def delete_NR_files():
    # Delete S2 files with NR in path - these are redunndant files 
    allfiles = glob.glob(rf"W:\Satellite\S3\L1\zip\*\*NR*.zip*",recursive=True)
    #allfiles = glob.glob(rf"W:\Satellite\S3\L2\NIVA\c2rcc\_300m\*\*\*NR*.nc",recursive=True)
    for f in allfiles:
        print (f)
        os.remove(f)
        #break
    #print (allfiles[:4])

import xarray as xr 
#ds_disk = xr.open_dataset(fr"W:\Satellite\S2\L2\iCOR\V103\0028_NIVA\32VNM\2020\altogether\DCS4COP_DEFAULT_S2A_0028_NIVA_20200304T105931Z_32VNM_SGS_V103.nc")
#print (ds_disk.keys())
#ds_disk2 = xr.open_dataset(fr"W:\Satellite\S2\L2\Lakes\Mjosa_north\C2RCC\_60m\C2RCC_idepix_S2A_MSIL1C_20160305T110042_N0201_R094_T32VNN_20160305T110109.nc")
#print (ds_disk2.keys())
delete_NR_files()