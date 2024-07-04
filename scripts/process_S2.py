# This Python file uses the following encoding: utf-8


'''
Created on 19. okt. 2018
@author: ABL@niva.no and ELP@niva.no
'''
import os
import sys
import os.path
from os.path import exists
from os import listdir
import subprocess
from datetime import datetime
from processing import createRGB, atmcorr_c2rcc, atmcorr_acolite
#import FilClass
#import FilConfig as FilConfig
import zipfile
import shutil
import argparse
from util import S2_settings_table
import json
tmp_work_folder = r'D:\S2\work'
sensor = 'S2'
import numpy as np

def unzip_file(f):
    tmp_files = listdir(tmp_work_folder)
    if len(tmp_files) > 0:
        print ('There are more than 1 file in the folder')
        shutil.rmtree(tmp_work_folder)
        print ('Cleared the work temp directory, continue .. ')
    try: 
        zip_ref = zipfile.ZipFile(f, 'r')
        zip_ref.extractall(tmp_work_folder)
        zip_ref.close()
        unzipped_folders = listdir(tmp_work_folder)
        
        #assert len(unzipped_folders) == 1, ('there are more than 1 file in the folder D:\S3\work')
        unzipped_folder = unzipped_folders[0]
        tmpff = os.path.join(tmp_work_folder,unzipped_folder,'MTD_MSIL1C.xml')  
    except zipfile.BadZipfile:
        print ("Bad Zip file for this path, skip",f)
        unzipped_folder,tmpff = None, None
    return(unzipped_folder,tmpff) 







def createRBG():
        #fillist = []
    lst = sorted(listdir(srcdir))
    for fil in lst: 
        if fil != 'RGB':
            print ('fil != RGB',fil)
            month = int(fil[15:17])
            if (month < 3) or (month > 10):
                print ('This is a month with too high zenit angle (the sun is too low), this scene will not be processed this scene.....')
            else:
                srcfil = os.path.join(srcdir,fil)
                _,tmpff = unzip_file(srcfil)

            trgdir = r'W:\Satellite\S2\L1\zip\{}\RGB'.format(tile)
            if not os.path.exists(trgdir):
                os.makedirs(trgdir)
            if not exists(os.path.join(trgdir,fil[:-3]+ 'tif')):
                createRGB(trgdir,tmpff,sensor)

def main(to_pixelExt = False, to_createRGB = False, to_atmcorr_c2rcc = False, to_atmcorr_acolite = False):
    '''
    '''

    lst = sorted(listdir(srcdir))


    for fil in lst: 
        if fil != 'RGB':
            
            month = int(fil[15:17])
            if (month < 3) or (month > 10):
                print ('This is a month with too high zenit angle (the sun is too low), this scene will not be processed this scene.....')
            else:
                srcfil = os.path.join(srcdir,fil)
                if srcfil not in progress[roi]:
                    print ('process new file', fil)
                    unzipped_folder,tmpff = unzip_file(srcfil)
                    len_progress = len(progress[roi])
                    print ("####### processed {} of total {}".format(len_progress,len(lst)))
                    percent = (np.float64(len_progress)/np.float64(len(lst)))*100.00
                    print ("####### {} %  of {} is processed".format(percent,roi))  

                    if to_atmcorr_c2rcc:
                        trgdir = r'W:\Satellite\S2\L2\{}\{}\C2RCC\_{}m'.format(wtype,roi,resolution)
                        
                        prop = r'S2_MSI_{}m_{}.properties'.format(resolution,roi)
                        print ('source file ', tmpff)
                        print ('target dir', trgdir)  

                        #atmcorr_c2rcc(srcfil,trgdir,modul,prop,sensor)
                        atmcorr_c2rcc(tmpff,trgdir,prop,sensor)

                    if to_atmcorr_acolite:
                        print ("to_atmcorr_acolite", to_atmcorr_acolite)
                        settfil = r'D:\Prosjekt\satelitt\Kopi_import_MERIS_ftp\acoliteSetting\{}_MSI_acoliteSettings_{}.txt'.format(sensor,roi)
                        res = atmcorr_acolite(tmpff,settfil)

                    progress[roi].append(srcfil)
                    json_file.seek(0)
                    json.dump(proc_progress_file, json_file,indent = 4)

                    shutil.rmtree(os.path.join(tmp_work_folder,unzipped_folder), ignore_errors=True)

                else:
                    print ("file is already processed")





def get_params(region_id):
    roi = S2_settings_table[region_id]["name"]
    wtype = S2_settings_table[region_id]["wtype"]  
    tile = S2_settings_table[region_id]["tile"]   
    resolution = S2_settings_table[region_id]['resolution']    
    srcdir = r'W:\Satellite\S2\L1\zip\{}'.format(tile)

    return roi,wtype,tile,resolution,srcdir


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--all", required = False, action = "store_true") 
    parser.add_argument("--region", required=False) 
    args = parser.parse_args()
    process_all = args.all 



    with open('process_progress.json', "r+") as json_file:
        proc_progress_file = json.load(json_file)
        progress = proc_progress_file["Sentinel-2"]

        print (process_all, 'to process all the files ')

        if process_all:
            all_regions = S2_settings_table.keys()
            for region_id in all_regions:
                roi,wtype,tile,resolution,srcdir = get_params(region_id)
                
                main(to_atmcorr_acolite = True, to_atmcorr_c2rcc = True)
        else: 
            parser = argparse.ArgumentParser()
            parser.add_argument("--region", required=True) 
            args = parser.parse_args()
            region_id = args.region

            roi,wtype,tile,resolution,srcdir = get_params(region_id)
            srcdir = r'W:\Satellite\S2\L1\zip\{}'.format(tile)

            #main(to_atmcorr_acolite = True, to_atmcorr_c2rcc = True, to_createRGB = True)
            print (roi,wtype,tile)
            main(to_atmcorr_c2rcc=True,to_atmcorr_acolite = True) #, 

    
   
