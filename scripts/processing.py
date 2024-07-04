#class processing:
#import os, shutil
#from os import system
import os
import sys
import os.path
from os.path import exists
from os import listdir
import subprocess
from datetime import datetime
import zipfile
import shutil

D_work_d = r'D:\\Prosjekt\satelitt\\Kopi_import_MERIS_ftp'
RGB_prop_S2 = r'{}\S2_rgb_profile_standard.rgb'.format(D_work_d)
RGB_prop_S3 = r'{}\S3_rgb_profile_standard.rgb'.format(D_work_d)

cmd_path_pconvert = r'C:/Program Files/snap/bin/pconvert.exe'
cmd_path_gpt = r'C:/Program Files/snap/bin/gpt.exe '
cmd_path_acolite = r'D:\\acolite_py_win\dist\\acolite\\acolite.exe'
#cmd_path_acolite = r'python D://acolite//launch_acolite.py'


S2_atmcorr_c2rcc_step = [r'{}\S2MSI_s2resample_subset_idepix_c2rcc.xml'.format(D_work_d)]
S3_atmcorr_c2rcc_steps = [r'{}\S3OLCI_subset_idepix.xml'.format(D_work_d),
                          r'{}\S3OLCI_subset_c2rcc.xml'.format(D_work_d)]

properties_path = r'{}\properties\\'.format(D_work_d)

def call_subprocess(command_string):
    try:
        subprocess.call(command_string)
    except:
        print('\nsubprocess.call() did not work.')

def createRGB(trgdir,srcfil,sensor):
    fformat = 'png'
    if sensor == 'S2':
        RGB_prop = RGB_prop_S2
    if sensor == 'S3':
        RGB_prop = RGB_prop_S3
        #print ('\nsrc file', srcfil[:-17])
    trgfname = r'{}\\{}.{}'.format(trgdir,srcfil[:-17],fformat)

    command_string = '{} -p {} -f {} -o {} {}'.format(cmd_path_pconvert,RGB_prop,fformat, trgdir,srcfil)
   
    
    if not exists(trgfname):
        print('\nCreating RGB file', trgfname)
        call_subprocess(command_string)
    else:
        print (trgfname + ' already exist in ' + trgdir)

def OWT_class(srcfil,trgDIR,modul,prop):
    '''
    This module needs more work.
    '''
    cmd_folder='C:/Program Files/snap/bin/'
    cmd_line=os.path.join(cmd_folder, 'gpt.exe')
    wg = str(cmd_line + modul)
    Sl1cProduct = srcfil
    print(Sl1cProduct)
    targetname='OWT_' + Sl1cProduct[11:-5] + '.dim'
    trgfname=os.path.join(trgDIR,targetname)
    print (trgfname)
    if not exists(trgfname):
            print ('Running ' + modul + ' on ' + Sl1cProduct)
            cmdwget = '%s -p %s -t %s %s' %(wg, prop, trgfname, Sl1cProduct)
            print (cmdwget)    
            subprocess.call(cmdwget)
    elif exists(trgfname):
        print (trgfname + ' already exist in ' + trgDIR)

def atmcorr_c2rcc_s2(Sl1cProduct,trgDIR,prop):
    print ("in atmcorr_c2rcc_s2")
    
    targetname='C2RCC_idepix_' + Sl1cProduct[-80:-20] + '.nc'
    trgfname=os.path.join(trgDIR,targetname)
    #print (trgfname)
    
    if not exists(trgfname):
        wg = str(cmd_path_gpt + S2_atmcorr_c2rcc_step[0]) 
        print ('Running C2RCC on '  + Sl1cProduct)
        properties = properties_path + prop
        print ('properties',properties)
        cmdwget = '%s -p %s -t %s %s -f %s' %(wg, properties, trgfname, Sl1cProduct, 'NetCDF4-BEAM') #Sl1cProduct is the sourcefile that should be processed. 
        #print (cmdwget)    
        try: 
            subprocess.call(cmdwget)
        except:
            print('something went wrong')
    else: 
        print (trgfname +' already exist in ' + trgDIR)              
 
def atmcorr_c2rcc_s3(Sl1cProduct,trgDIR,prop):

    targetname_idepix = 'IdePix_' + Sl1cProduct[11:-22] + '.nc'
    targetname_c2rcc = 'C2RCC_' + Sl1cProduct[11:-22] + '.nc'
    trgfname_idepix = os.path.join(trgDIR,targetname_idepix)
    trgfname_c2rcc = os.path.join(trgDIR,targetname_c2rcc)
    properties = properties_path + prop

    ## Step 1
    if not exists(trgfname_idepix):
        wg = str(cmd_path_gpt + S3_atmcorr_c2rcc_steps[0])
        print ('\nStep1: Running atmcorr c2rcc s3 step 1 ') # + S3_atmcorr_c2rcc_steps[0] + ' on ' + Sl1cProduct)
        cmdwget = '%s -p %s -t %s %s -f %s' %(wg, properties, trgfname_idepix, Sl1cProduct, 'NetCDF4-BEAM')
        
        call_subprocess(cmdwget)

        print ('after subprocess.. ')

    elif exists(trgfname_idepix):
        print ('\n' + trgfname_idepix + ' already exist in ' + trgDIR)

    ## Step 2
    if not exists(trgfname_c2rcc):    
        wg = str(cmd_path_gpt + S3_atmcorr_c2rcc_steps[1])
        properties = properties_path + prop

        print ('\nStep2: Running atmcorr c2rcc s3 step 2' ) #+ S3_atmcorr_c2rcc_steps[1] + ' on ' + Sl1cProduct)
        cmdwget = '%s -p %s -t %s %s -f %s' %(wg, properties, trgfname_c2rcc, Sl1cProduct, 'NetCDF4-BEAM')
        call_subprocess(cmdwget)
        
    elif exists(trgfname_c2rcc):
        print ('Step2 c2rcd already exists in '+ '\n' + trgfname_c2rcc + trgDIR)


def atmcorr_c2rcc(srcfil,trgDIR,prop,sensor):
    '''
    Update explanation. Remove xtra unnessary lines below for running the script
    '''
    print ('prop',prop)
    print('\n' + srcfil)

    if sensor == 'S2':
        atmcorr_c2rcc_s2(srcfil,trgDIR,prop)
    elif sensor == 'S3':
        atmcorr_c2rcc_s3(srcfil,trgDIR,prop) 

def atmcorr_acolite(srcfil,settfil):
    srcfil = srcfil[:-15]
    cmdwget = '%s --cli --settings=%s --image=%s' %(cmd_path_acolite, settfil, srcfil)
    #print (cmdwget)
    print ('\nrunning atmcorr_acolite')
    try:   
        subprocess.call(cmdwget)
    except:
        print('\nsomething went wrong')
        return False
    return True    

def dim2nc(srcfil,trgfil):
    cmd_folder='C:/Program Files/snap/bin/'
    cmd_line=os.path.join(cmd_folder, 'gpt.exe Write')
    format = r'NetCDF4-BEAM'
    cmdwget = '%s -PformatName=%s -Pfile=%s %s' %(cmd_line, format, trgfil, srcfil)
    #print (cmdwget)   
    print ("\ncall snap gpt.exe" )
    subprocess.call(cmdwget) 

def pixelExt(properties):

    modul = r' D:\Prosjekt\satelitt\Kopi_import_MERIS_ftp\pixelExtractionGraph.xml'
    wg = str(cmd_path_gpt + modul)
    cmdwget = '%s -p %s' %(wg, properties)
    print ("\npixelExt")   
    subprocess.call(cmdwget) 

